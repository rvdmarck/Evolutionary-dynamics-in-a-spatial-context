import Lattice
import time
import Plotter

nrSim = 100
nrRoundsPerSim = 99
size = 50
sim = 3

MOORE = "Moore"
VON_NEUMANN = "Von Neumann"

mode = MOORE

def run(rounds, averageCoop, finalCoop):
    for i in range(rounds):

        print("SIMULATION : "+str(i))
        start_time = time.time()
        l = Lattice.Lattice(size, size)
        l.randPopulate()
        l.run(nrRoundsPerSim, "final", neighborhood = mode)
        for j in range(len(l.coopHistory)):
            averageCoop[j] += l.coopHistory[j]
        finalCoop.append(l.coopHistory[nrRoundsPerSim-1])
        print("--- %s seconds ---" % (time.time() - start_time))
    for i in range(len(averageCoop)):
        averageCoop[i] /= nrSim


def main():

    averageCoop = [0] * (nrRoundsPerSim+1)
    finalCoop = []

    if sim == 1 :
        l = Lattice.Lattice(size, size)
        l.randPopulate()
        l.run(100, "any", True, neighborhood = mode)
    elif sim == 2 :
        run(nrSim, averageCoop, finalCoop)

        p = Plotter.Plotter(averageCoop, "Cooperation level over time, averaged over 100 simulations", "Round", "Cooperation level", "notFinal")
        p = Plotter.Plotter(finalCoop, "Distribution of the final cooperation levels", "Final Cooperation Level", "Number of Simulations", "final", nrSim)
    elif sim == 3 :
        global size
        averageCoops = []
        size = 4
        run(nrSim, averageCoop, finalCoop)
        averageCoops.append(averageCoop)
        averageCoop = [0] * (nrRoundsPerSim + 1)
        finalCoop = []

        size = 8
        run(nrSim, averageCoop, finalCoop)
        averageCoops.append(averageCoop)
        averageCoop = [0] * (nrRoundsPerSim + 1)
        finalCoop = []

        size = 12
        run(nrSim, averageCoop, finalCoop)
        averageCoops.append(averageCoop)
        averageCoop = [0] * (nrRoundsPerSim + 1)
        finalCoop = []

        size = 20
        run(nrSim, averageCoop, finalCoop)
        averageCoops.append(averageCoop)
        averageCoop = [0] * (nrRoundsPerSim + 1)
        finalCoop = []

        p = Plotter.Plotter(averageCoops, "Cooperation level over time, averaged over 100 simulations", "Round",
                            "Cooperation level", "notFinal")

main()
