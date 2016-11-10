import Lattice


def main():
    l = Lattice.Lattice(50, 100)

    l.randPopulate()
    print(l)

    l.run(10)


main()
