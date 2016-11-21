import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    def __init__(self, y, title, xlabel, ylabel, mode, nrSim = 100):
        x = np.arange(0, nrSim, 1)
        plots = ()
        legends = ["4x4 Lattice", "8x8 Lattice", "12x12 Lattice", "20x20 Lattice"]
        if mode != "final":
            if type(y) == type([]):
                for i in range(len(y)):
                    plt.plot(x,y[i], linewidth = 2, label = legends[i]),
                plt.legend()
            else:
                plt.plot(x, y, linewidth=2)
            plt.xlim(0, 100)
            plt.ylim(0.0, 1.0)
        else:
            plt.hist(y)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.show()
