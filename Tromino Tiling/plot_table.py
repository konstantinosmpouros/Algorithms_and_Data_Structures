import matplotlib.pyplot as plt
import numpy as np


def plot(table):
    length = len(table)

    # Create a dictionary to map color codes to actual colors
    color_mapping = {
        'R': 'red',
        'B': 'blue',
        'G': 'green',
        'X': 'black'
    }

    # Replace the codes in the 2D list with actual colors
    table = [[color_mapping[code] for code in row] for row in table]

    # Create a figure and a subplot
    fig, ax = plt.subplots()
    ax.set_xlim(0, length)
    ax.set_ylim(0, length)
    ax.set_xticks(np.arange(0, length, 1))
    ax.set_yticks(np.arange(0, length, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True)

    # Color each cell according to the color table
    for i in range(length):
        for j in range(length):
            ax.add_patch(plt.Rectangle((j, i), 1, 1, color=table[i][j]))

    plt.gca().invert_yaxis()  # Invert Y axis so (0,0) is at the top left
    plt.show()
