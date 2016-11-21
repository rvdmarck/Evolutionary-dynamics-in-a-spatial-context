import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    def __init__(self, y, title, xlabel, ylabel, mode, nrSim = 100):
        x = np.arange(0, nrSim, 1)
        plots = []
        if mode != "final":
            if type(y) == type([]):
                for coopLvl in y:
                    plots.append(plt.plot(x,coopLvl, linewidth = 2))
                plots = tuple(plots)
                plt.legend((plots),("4x4 Lattice", "8x8 Lattice", "12x12 Lattice", "20x20 Lattice"), loc='upper right', shadow=True)
            else:
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
