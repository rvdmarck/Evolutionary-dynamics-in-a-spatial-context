from random import randint

import numpy as np

T = 10
R = 7
P = 0
S = 0
COOPERATE = 67
DEFECT = 68

def printNeighbours(neighbours):
    print(str(neighbours[5]) + "  ,  " + str(neighbours[6]) + "  ,  " + str(neighbours[2]) + "\n" + str(
        neighbours[7]) + "  ,  X  ,  " + str(neighbours[3]) + "\n" + str(neighbours[0]) + "  ,  " + str(
        neighbours[1]) + "  ,  " + str(neighbours[4]))


def computePayoff(player1, player2):
    if player1 == COOPERATE:
        if player2 == COOPERATE:
            return R
        if player2 == DEFECT:
            return S
    if player1 == DEFECT:
        if player2 == COOPERATE:
            return T
        if player2 == DEFECT:
            return P


class Lattice:
    def __init__(self, row, col):
        self.r = row
        self.c = col
        self.matrix = np.zeros((row,col))
        self.payoffMatrix = np.zeros((row, col))
        self.coopHistory = []
        self.total = row*col
        self.neighbours = np.zeros((8))
        self.payoffNeighbours = np.zeros((9))

    def __repr__(self):
        toprint = ""
        for i in range(self.r):
            for j in range(self.c):
                if self.matrix[i][j] == COOPERATE:
                    toprint += str('\x1b[0;30;44m' + chr(COOPERATE) + '\x1b[0m')
                else:
                    toprint += str('\x1b[0;30;41m' + chr(DEFECT) + '\x1b[0m')
                if j != self.c - 1:
                    toprint += ""  # separator
            toprint += "\n"
        return toprint

    def getNeighbours(self, i, j):
        self.neighbours = np.zeros((8))

        if 0 <= i < self.r and 0 <= j < self.c:
            if i == self.r - 1:
                self.neighbours[0] = self.matrix[0][j - 1]
                self.neighbours[1] = self.matrix[0][j]
            else:
                self.neighbours[0] = self.matrix[i + 1][j - 1]
                self.neighbours[1] = self.matrix[i + 1][j]

            if j == self.c - 1:
                self.neighbours[2] = self.matrix[i - 1][0]
                self.neighbours[3] = self.matrix[i][0]
            else:
                self.neighbours[2] = self.matrix[i - 1][j + 1]
                self.neighbours[3] = self.matrix[i][j + 1]
            if i == self.r - 1 and j == self.c - 1:
                self.neighbours[4] = self.matrix[0][0]
            elif i == self.r - 1:
                self.neighbours[4] = self.matrix[0][j + 1]
            elif j == self.c - 1:
                self.neighbours[4] = self.matrix[i + 1][0]
            else:
                self.neighbours[4] = self.matrix[i + 1][j + 1]

            self.neighbours[5] = self.matrix[i - 1][j - 1]
            self.neighbours[6] = self.matrix[i - 1][j]
            self.neighbours[7] = self.matrix[i][j - 1]

    def getNeighboursPayoff(self, i, j):
        self.payoffNeighbours = np.zeros((9))

        if 0 <= i < self.r and 0 <= j < self.c:
            if i == self.r - 1:
                self.payoffNeighbours[0] = self.payoffMatrix[0][j - 1]
                self.payoffNeighbours[1] = self.payoffMatrix[0][j]
            else:
                self.payoffNeighbours[0] = self.payoffMatrix[i + 1][j - 1]
                self.payoffNeighbours[1] = self.payoffMatrix[i + 1][j]
            if j == self.c - 1:
                self.payoffNeighbours[2] = self.payoffMatrix[i - 1][0]
                self.payoffNeighbours[3] = self.payoffMatrix[i][0]
            else:
                self.payoffNeighbours[2] = self.payoffMatrix[i - 1][j + 1]
                self.payoffNeighbours[3] = self.payoffMatrix[i][j + 1]
            if i == self.r - 1 and j == self.c - 1:
                self.payoffNeighbours[4] = self.payoffMatrix[0][0]
            elif i == self.r - 1:
                self.payoffNeighbours[4] = self.payoffMatrix[0][j + 1]
            elif j == self.c - 1:
                self.payoffNeighbours[4] = self.payoffMatrix[i + 1][0]
            else:
                self.payoffNeighbours[4] = self.payoffMatrix[i + 1][j + 1]

            self.payoffNeighbours[5] = self.payoffMatrix[i - 1][j - 1]
            self.payoffNeighbours[6] = self.payoffMatrix[i - 1][j]
            self.payoffNeighbours[7] = self.payoffMatrix[i][j - 1]
            self.payoffNeighbours[8] = self.payoffMatrix[i][j]

    def randPopulate(self):
        count = 0
        for elt in self.matrix.flat:
            self.matrix[count//self.c][count%self.c] = randint(COOPERATE, DEFECT)
            count += 1

    def computePayoffFor(self, i, j):
        self.getNeighbours(i, j)
        sumPayoffs = 0
        for neighbour in self.neighbours:
            sumPayoffs += computePayoff(self.matrix[i][j], neighbour)
        return sumPayoffs

    def computeAllPayoffs(self):
        count = 0
        for elt in self.matrix.flat:
            row = count//self.c
            col = count%self.c
            self.payoffMatrix[row][col] = self.computePayoffFor(row, col)
            count += 1

    def selectBestAction(self, i, j):
        self.getNeighboursPayoff(i,j)
        maxNeighbourPayoffIndex = self.payoffNeighbours.argmax()
        if maxNeighbourPayoffIndex != 8:
            self.matrix[i][j] = self.neighbours[maxNeighbourPayoffIndex]

    def selectAllBestAction(self):
        count = 0
        for elt in self.matrix.flat:
            self.selectBestAction(count//self.c, count%self.c)
            count += 1

    def run(self, round, mode, toPrint=False):
        if (toPrint):
            print(self)
        for i in range(round):
            self.computeAllPayoffs()
            self.selectAllBestAction()
            self.computeCoopLevel()
            if mode == "any":
                if i == 0 or i == 1 or i == 5 or i == 10 or i == 20 or i == 50:
                    print(str(i)+": "+str(self.coopHistory[len(self.coopHistory)-1]*100)+"%")
            elif mode == "final":
                if i == 100:
                    print(str(i) + ": " + str(self.coopHistory[len(self.coopHistory) - 1] * 100) + "%")

            if(toPrint):
                print(self)

    def computeCoopLevel(self):
        coopLvl = 0
        for i in range(self.r):
            for j in range(self.c):
                if self.matrix[i][j] == COOPERATE:
                    coopLvl += 1
        self.coopHistory.append(coopLvl / self.total)
        return coopLvl / self.total

