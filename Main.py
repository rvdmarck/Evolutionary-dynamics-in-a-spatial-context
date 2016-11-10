from Lattice import *


def main():
    T = 10
    R = 7
    P = 0
    S = 0

    l = Lattice(5, 5)
    l.randPopulate()
    print(l)
    printNeighbours(l.getNeighbours(0, 0))


main()
