import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    def __init__(self, y, title, xlabel, ylabel, mode, nrSim = 100):
        x = np.arange(0, nrSim, 1)

        if mode != "final":
            plt.plot(x, y, linewidth=2)
            plt.xlim(0, 100)
            plt.ylim(0.0, 1.0)
        else:
            #plt.plot(x, y, "ro")
            plt.hist(y)
            #plt.ylim(0, 100)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.show()
