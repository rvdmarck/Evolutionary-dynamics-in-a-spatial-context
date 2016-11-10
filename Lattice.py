# import numpy as np
from random import randint

def printNeighbours(neighbours):
    print(str(neighbours[5]) + "  ,  " + str(neighbours[6]) + "  ,  " + str(neighbours[2]) + "\n" + str(
        neighbours[7]) + "  ,  X  ,  " + str(neighbours[3]) + "\n" + str(neighbours[0]) + "  ,  " + str(
        neighbours[1]) + "  ,  " + str(neighbours[4]))


class Lattice:
    def __init__(self, row, col):
        self.r = row
        self.c = col
        self.matrix = [[0 for x in range(self.c)] for y in range(self.r)]

    def __repr__(self):
        # return '\n'.join([''.join(['{:4}'.format(item) for item in self.r]) for self.r in self.matrix])
        toprint = ""
        for i in range(self.r):
            for j in range(self.c):
                toprint += str(self.matrix[i][j])
                if j != self.c - 1:
                    toprint += "  ,  "
            toprint += "\n"
        return toprint

    def getNeighbours(self, i, j):
        neighbours = []

        if 0 <= i < self.r and 0 <= j < self.c:  # normal case
            if i == self.r - 1:
                neighbours.append(self.matrix[0][j - 1])  # Bot-Left
                neighbours.append(self.matrix[0][j])  # Bot
            else:
                neighbours.append(self.matrix[i + 1][j - 1])  # Bot-Left
                neighbours.append(self.matrix[i + 1][j])  # Bot

            if j == self.c - 1:
                neighbours.append(self.matrix[i - 1][0])  # Top-Right
                neighbours.append(self.matrix[i][0])  # Right
            else:
                neighbours.append(self.matrix[i - 1][j + 1])  # Top-Right
                neighbours.append(self.matrix[i][j + 1])  # Right
            if i == self.r - 1 and j == self.c - 1:
                neighbours.append(self.matrix[0][0])  # Bot-Right
            else:
                neighbours.append(self.matrix[i + 1][j + 1])  # Bot-Right

            neighbours.append(self.matrix[i - 1][j - 1])  # Top-Left
            neighbours.append(self.matrix[i - 1][j])  # Top
            neighbours.append(self.matrix[i][j - 1])  # Left

        return neighbours

    def set(self, value, i, j):
        self.matrix[i][j] = value

    def randPopulate(self):
        for i in range(self.r):
            for j in range(self.c):
                self.matrix[i][j] = chr(randint(67, 68))
