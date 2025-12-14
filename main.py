import argparse
import math
import sys
from pathlib import Path
from typing import List, Optional, Tuple

from PIL import Image

from points import (
    buscar_atractores,
    load_metadata,
    save_metadata
)


def scale_points(
    x_list: List[float],
    y_list: List[float],
    width: int,
    height: int,
    margin: int = 10
) -> Tuple[List[int], List[int]]:
    min_x, max_x = min(x_list), max(x_list)
    min_y, max_y = min(y_list), max(y_list)

    range_x = max_x - min_x if max_x != min_x else 1
    range_y = max_y - min_y if max_y != min_y else 1

    effective_width = width - 2 * margin
    effective_height = height - 2 * margin

    scaled_x = [
        int(margin + (x - min_x) / range_x * effective_width)
        for x in x_list
    ]
    scaled_y = [
        int(margin + (y - min_y) / range_y * effective_height)
        for y in y_list
    ]

    return scaled_x, scaled_y


def calculate_density_map(
    scaled_x: List[int],
    scaled_y: List[int],
    width: int,
    height: int,
    radius: int = 5
) -> List[List[float]]:
    density = [[0.0 for _ in range(width)] for _ in range(height)]
    
    for x, y in zip(scaled_x, scaled_y):
        if 0 <= x < width and 0 <= y < height:
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        dist = math.sqrt(dx * dx + dy * dy)
                        if dist <= radius:
                            weight = 1.0 - (dist / radius)
                            density[ny][nx] += weight
    
    return density


def density_to_color(density: float, max_density: float) -> Tuple[int, int, int]:
    if max_density == 0:
        return (255, 255, 255)
    
    normalized = density / max_density
    
    if normalized < 0.25:
        t = normalized / 0.25
        r = int(0)
        g = int(0 + t * 255)
        b = int(255)
    elif normalized < 0.5:
        t = (normalized - 0.25) / 0.25
        r = int(0)
        g = int(255)
        b = int(255 - t * 255)
    elif normalized < 0.75:
        t = (normalized - 0.5) / 0.25
        r = int(0 + t * 255)
        g = int(255)
        b = int(0)
    else:
        t = (normalized - 0.75) / 0.25
        r = int(255)
        g = int(255 - t * 255)
        b = int(0)
    
    return (min(255, max(0, r)), min(255, max(0, g)), min(255, max(0, b)))


def generate_image(
    attractor: Tuple[List[float], List[float]],
    width: int = 1920,
    height: int = 1080,
    color: Optional[Tuple[int, int, int]] = None,
    background: Tuple[int, int, int] = (0, 0, 0),
    density_coloring: bool = False,
    density_radius: int = 5
) -> Image.Image:
    x_list, y_list = attractor
    img = Image.new("RGB", (width, height), background)
    pixels = img.load()

    scaled_x, scaled_y = scale_points(x_list, y_list, width, height)

    if density_coloring:
        density_map = calculate_density_map(scaled_x, scaled_y, width, height, density_radius)
        max_density = max(max(row) for row in density_map) if density_map else 1
        
        for x, y in zip(scaled_x, scaled_y):
            if 0 <= x < width and 0 <= y < height:
                density = density_map[y][x]
                pixel_color = density_to_color(density, max_density)
                pixels[x, y] = pixel_color
    else:
        default_color = color if color is not None else (255, 255, 255)
        for x, y in zip(scaled_x, scaled_y):
            if 0 <= x < width and 0 <= y < height:
                pixels[x, y] = default_color

    return img


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera y visualiza atractores caóticos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s --output atractor
  %(prog)s --seed "mi_semilla" --width 3840 --height 2160
  %(prog)s --load-metadata outputs/atractor_metadata.json
        """
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default="atractor",
        help="Nombre base para los archivos de salida (sin extensión)"
    )

    parser.add_argument(
        "-s", "--seed",
        type=str,
        default=None,
        help="Semilla para reproducibilidad"
    )

    parser.add_argument(
        "-w", "--width",
        type=int,
        default=1920,
        help="Ancho de la imagen en píxeles (default: 1920)"
    )

    parser.add_argument(
        "--height",
        type=int,
        default=1080,
        help="Alto de la imagen en píxeles (default: 1080)"
    )

    parser.add_argument(
        "-i", "--iterations",
        type=int,
        default=10000,
        help="Número máximo de iteraciones (default: 10000)"
    )

    parser.add_argument(
        "-l", "--min-lyapunov",
        type=float,
        default=10.0,
        help="Valor mínimo del exponente de Lyapunov (default: 10.0)"
    )

    parser.add_argument(
        "--load-metadata",
        type=str,
        default=None,
        help="Cargar semilla desde archivo de metadatos"
    )

    parser.add_argument(
        "--no-image",
        action="store_true",
        help="No generar imagen, solo metadatos"
    )

    parser.add_argument(
        "--density-color",
        action="store_true",
        help="Colorear puntos basándose en la densidad local"
    )

    parser.add_argument(
        "--density-radius",
        type=int,
        default=5,
        help="Radio para calcular densidad local (default: 5)"
    )

    return parser.parse_args()


def main() -> int:
    args = parse_arguments()

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    encoded_seed_param = None
    seed_param = args.seed

    if args.load_metadata:
        try:
            metadata_path = Path(args.load_metadata)
            if not metadata_path.is_absolute():
                metadata_path = output_dir / metadata_path
            metadata = load_metadata(metadata_path)
            encoded_seed_param = metadata["seed"]
        except (FileNotFoundError, KeyError) as e:
            print(f"Error: No se pudo cargar metadatos: {e}", file=sys.stderr)
            return 1

    try:
        attractors, parametros, encoded_seed = buscar_atractores(
            n=1,
            seed=seed_param,
            encoded_seed=encoded_seed_param,
            max_iterations=args.iterations,
            min_lyapunov=args.min_lyapunov
        )

        attractor = attractors[0]
        num_points = len(attractor[0])

        base_path = output_dir / args.output

        if not args.no_image:
            img = generate_image(
                attractor,
                width=args.width,
                height=args.height,
                density_coloring=args.density_color,
                density_radius=args.density_radius
            )
            img_path = base_path.with_suffix(".png")
            img.save(img_path)
            print(f"Imagen guardada: {img_path}")

        metadata_path = base_path.with_name(f"{base_path.name}_metadata.json")
        save_metadata(
            metadata_path,
            parametros,
            encoded_seed,
            num_points
        )
        print(f"Metadatos guardados: {metadata_path}")

        print(f"Semilla codificada: {encoded_seed}")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
