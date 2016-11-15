import Lattice
import time
import Plotter

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

    # l = Lattice.Lattice(50, 50)
    # l.randPopulate()
    # l.run(100, "any")

    run(nrSim, averageCoop, finalCoop)

    print(len(finalCoop))
    p = Plotter.Plotter(averageCoop, "Round", "Cooperation level", "notFinal")
    p = Plotter.Plotter(finalCoop, "Simulation Number", "Final Cooperation Level", "final", nrSim)


main()
