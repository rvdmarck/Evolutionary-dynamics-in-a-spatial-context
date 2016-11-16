from random import randint


T = 10
R = 7
P = 0
S = 0


def printNeighbours(neighbours):
    print(str(neighbours[5]) + "  ,  " + str(neighbours[6]) + "  ,  " + str(neighbours[2]) + "\n" + str(
        neighbours[7]) + "  ,  X  ,  " + str(neighbours[3]) + "\n" + str(neighbours[0]) + "  ,  " + str(
        neighbours[1]) + "  ,  " + str(neighbours[4]))


def computePayoff(player1, player2):
    if player1 == "C":
        if player2 == "C":
            return R
        if player2 == "D":
            return S
    if player1 == "D":
        if player2 == "C":
            return T
        if player2 == "D":
            return P


class Lattice:
    def __init__(self, row, col):
        self.r = row
        self.c = col
        self.matrix = [[0 for x in range(self.c)] for y in range(self.r)]
        self.coopHistory = []
        self.total = row*col

    def __repr__(self):
        # return '\n'.join([''.join(['{:4}'.format(item) for item in self.r]) for self.r in self.matrix])
        toprint = ""
        for i in range(self.r):
            for j in range(self.c):
                if self.matrix[i][j][0] == "C":
                    toprint += str('\x1b[0;30;44m' + self.matrix[i][j] + '\x1b[0m')
                else:
                    toprint += str('\x1b[0;30;41m' + self.matrix[i][j] + '\x1b[0m')
                if j != self.c - 1:
                    toprint += ""  # separator
            toprint += "\n"
        return toprint

    def getNeighbours(self, i, j):
        neighbours = []

        if 0 <= i < self.r and 0 <= j < self.c:
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
            elif i == self.r - 1:
                neighbours.append(self.matrix[0][j + 1])  # Bot-Right
            elif j == self.c - 1:
                neighbours.append(self.matrix[i + 1][0])  # Bot-Right
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

    def computePayoffFor(self, i, j):
        neighbours = self.getNeighbours(i, j)
        sumPayoffs = 0
        for neighbour in neighbours:
            sumPayoffs += computePayoff(self.matrix[i][j], neighbour[0])
        return sumPayoffs

    def computeAllPayoffs(self):
        for i in range(self.r):
            for j in range(self.c):
                self.matrix[i][j] = (self.matrix[i][j], self.computePayoffFor(i, j))

    def selectBestAction(self, i, j):
        neighbours = self.getNeighbours(i, j)
        neighbours.append(self.matrix[i][j])
        maxPayoff = 0
        for neighbour in neighbours:
            if neighbour[1] >= maxPayoff:
                maxPayoff = neighbour[1]
                nextAction = (neighbour[0],)
        self.matrix[i][j] = self.matrix[i][j] + nextAction

    def selectAllBestAction(self):
        for i in range(self.r):
            for j in range(self.c):
                self.selectBestAction(i, j)

    def applyActions(self):
        for i in range(self.r):
            for j in range(self.c):
                self.matrix[i][j] = self.matrix[i][j][2]

    def run(self, round, mode, toPrint=False):
        for i in range(round):
            self.computeAllPayoffs()
            self.selectAllBestAction()
            self.applyActions()
            y = self.matrix
            self.computeCoopLevel()
            if mode == "any":
                if i == 0 or i == 1 or i == 5 or i == 10 or i == 20 or i == 50:
                    print(str(i)+": "+str(self.coopHistory[len(self.coopHistory)-1]*100)+"%")
            elif mode == "final":
                if i == 100:
                    print(str(i) + ": " + str(self.coopHistory[len(self.coopHistory) - 1] * 100) + "%")

            #self.computeVariance()
            if(toPrint):
                print(self)

    def computeCoopLevel(self):
        coopLvl = 0
        for i in range(self.r):
            for j in range(self.c):
                if self.matrix[i][j] == "C":
                    coopLvl += 1
        self.coopHistory.append(coopLvl / self.total)
        return coopLvl / self.total


"""
    def computeVariance(self):
        if len(self.coopHistory) > 10:
            print(statistics.pvariance(self.coopHistory[10:]))
"""
