import time

import Lattice

nrSim = 100
nrRoundsPerSim = 100

def run(rounds, averageCoop, finalCoop):
    for i in range(rounds):

        print("ROUND : "+str(i))
        start_time = time.time()
        l = Lattice.Lattice(50, 50)
        l.randPopulate()
        l.run(nrRoundsPerSim, "final")
        for j in range(len(l.coopHistory)):
            averageCoop[j] += l.coopHistory[j]
        finalCoop.append(l.coopHistory[nrRoundsPerSim-1])
        print("--- %s seconds ---" % (time.time() - start_time))
    for i in range(len(averageCoop)):
        averageCoop[i] /= nrSim


def main():

    averageCoop = [0] * nrRoundsPerSim
    finalCoop = []

    l = Lattice.Lattice(50, 50)
    l.randPopulate()
    l.run(100, "any", True)

    #run(nrSim, averageCoop, finalCoop)

    #p = Plotter.Plotter(averageCoop, "Cooperation level over time, averaged over 100 simulations", "Round", "Cooperation level", "notFinal")
    #p = Plotter.Plotter(finalCoop, "Distribution of the final cooperation levels", "Final Cooperation Level", "Number of Simulations", "final", nrSim)


main()
