import pygame
import sys
import datetime
from points import buscar_atractores
from time import time


def plot_attractor(screen, attractor):
    min_x, max_x = min(attractor[0]), max(attractor[0])
    min_y, max_y = min(attractor[1]), max(attractor[1])

    scaled_attractor = (
        [(x - min_x) / (max_x - min_x) for x in attractor[0]],
        [(y - min_y) / (max_y - min_y) for y in attractor[1]]
    )

    for x, y in zip(scaled_attractor[0], scaled_attractor[1]):
        screen.set_at((int(x * screen.get_width()), int(y * screen.get_height())), (255, 255, 255))

def save_image(screen, filename):
    pygame.image.save(screen, filename + ".png")

def save_attractor(attractor, formula, filename):
    with open(filename + ".txt", "w") as file:
        file.write("Formula Coefficients:\n")
        file.write(" ".join(map(str, formula)) + "\n\n")
        file.write("Attractor Points:\n")
        for x, y in zip(attractor[0], attractor[1]):
            file.write(f"{x} {y}\n")
        file.write("\nParameters:\n")
        file.write(f"x: {attractor[0][0]}\n")
        file.write(f"y: {attractor[1][0]}\n")
        file.write(f"a: {attractor[2]}\n")

def display_instructions(screen, show_instructions, show_instructions_after_save, parametros):
    if show_instructions or show_instructions_after_save:
        font = pygame.font.SysFont(None, 25)
        text = font.render("Press 'N' for the next attractor", True, (255, 255, 255))
        screen.blit(text, (10, screen.get_height() - 120))
        text = font.render("Press 'S' to save the image", True, (255, 255, 255))
        screen.blit(text, (10, screen.get_height() - 100))
        text = font.render("Press 'T' to save values and formula", True, (255, 255, 255))
        screen.blit(text, (10, screen.get_height() - 80))
        text = font.render("Press 'ESC' to exit", True, (255, 255, 255))
        screen.blit(text, (10, screen.get_height() - 60))
        text = font.render("Press 'Q' to toggle instructions", True, (255, 255, 255))
        screen.blit(text, (10, screen.get_height() - 40))

        text = font.render(f"Formula: {parametros}", True, (255, 255, 255))
        screen.blit(text, (10, screen.get_height() - 20))
    else:
        font = pygame.font.SysFont(None, 25)
        text = font.render("Press 'Q' to show instructions", True, (255, 255, 255))
        screen.blit(text, (10, screen.get_height() - 40))


def main():
    pygame.init()

    # Get screen information
    screen_info = pygame.display.Info()
    width, height = screen_info.current_w, screen_info.current_h

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Chaotic Attractors')
    clock = pygame.time.Clock()

    attractors = [] 
    attractor_index = 0
    show_instructions = True
    show_instructions_after_save = False
    parametros = buscar_atractores(1)[1]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    attractors, parametros = buscar_atractores(1)
                    attractor_index = 0
                elif event.key == pygame.K_s and attractors:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    filename = f"Atractor_{timestamp}"
                    save_image(screen, filename)
                elif event.key == pygame.K_t and attractors:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    filename = f"Atractor_{timestamp}"
                    with open(filename + "param" + ".txt", "w") as file:
                        file.write("Formula Coefficients:\n")
                        file.write("".join(str(parametros)) + "\n\n")
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_q:
                    show_instructions = not show_instructions
                    show_instructions_after_save = False  

        screen.fill((0, 0, 0))
        if attractors:
            plot_attractor(screen, attractors[attractor_index])

        display_instructions(screen, show_instructions, show_instructions_after_save, parametros)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
