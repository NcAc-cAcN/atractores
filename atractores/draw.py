import matplotlib.pyplot as plt
import numpy as np

def reconstruct_attractor(parameters, num_points=1000000):
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
    example_parameters = (-0.08193648868103298, 0.06340475958705472, [0.09830646140771782, -0.3337185519769599, -1.1301515730183844, 1.407445653218538, -1.552684827791484, 1.378677426082663, 0.12351926338523267, 0.4166790910201552, 0.5123224620137163, -0.6105167076798343, -1.260816324996434, 0.34715417348294153])

    reconstructed_x, reconstructed_y = reconstruct_attractor(example_parameters)
    plot_attractor(reconstructed_x, reconstructed_y)
