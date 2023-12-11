import matplotlib.pyplot as plt
import numpy as np

def reconstruct_attractor(parameters, num_points=100000):
    x, y, a = parameters
    x_list = [x]
    y_list = [y]

    for _ in range(num_points):
        xnew = a[0] + a[1]*x + a[2]*x*x + a[3]*y + a[4]*y*y + a[5]*x*y
        ynew = a[6] + a[7]*x + a[8]*x*x + a[9]*y + a[10]*y*y + a[11]*x*y

        x = xnew
        y = ynew

        x_list.append(x)
        y_list.append(y)

    return x_list, y_list

def plot_attractor(x_list, y_list):
    plt.plot(x_list, y_list, '.', markersize=1)
    plt.title('Reconstructed Attractor')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

if __name__ == "__main__":
    example_parameters = (-0.05342833805223057, -0.2781575473630731, [-0.043349822442591446, -0.9455905374580484, 0.6823994501175155, -1.6217569294854495, 1.277158558465271, 0.8330176565804801, 0.03411114195130782, 0.4030699762526133, -0.8222069454059691, -0.7784502357206833, -0.014090997777962855, 0.18514583743319912])

    reconstructed_x, reconstructed_y = reconstruct_attractor(example_parameters)
    plot_attractor(reconstructed_x, reconstructed_y)
