from random import randint, random
from termcolor import colored
from math import floor

T = 10
R = 7
P = 0
S = 3

MOORE = "Moore"
VON_NEUMANN = "Von Neumann"

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

def randitem(l):

    # Make the probabilities add up to 1, preserving ratios
    s = sum([b for (a,b) in l])
    l2 = []
    for (a,b) in l:
        l2.append((a, b/s))

    r = random()
    for (a,b) in l2:
        if r < b:
            return a
        else:
            r -= b


class Lattice:
    def __init__(self, row, col):
        self.r = row
        self.c = col
        self.matrix = [[0 for x in range(self.c)] for y in range(self.r)]
        self.coopHistory = []
        self.total = row*col

    def __repr__(self):
        toprint = ""
        for i in range(self.r):
            for j in range(self.c):
                if self.matrix[i][j][0] == "C":
                    #toprint += str('\x1b[0;30;44m' + self.matrix[i][j] + '\x1b[0m')
                    toprint += colored(str(self.matrix[i][j]), 'blue', attrs=['reverse'])
                else:
                    #toprint += str('\x1b[0;30;41m' + self.matrix[i][j] + '\x1b[0m')
                    toprint += colored(str(self.matrix[i][j]), 'red', attrs=['reverse', 'blink'])
                if j != self.c - 1:
                    toprint += ""  # separator
            toprint += "\n"
        return toprint

    def getNeighbours(self, i, j, mode = MOORE):
        neighbours = []

        if mode == MOORE:
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
        elif mode == VON_NEUMANN:
            if i == self.r - 1:
                neighbours.append(self.matrix[0][j]) #Bot
            else:
                neighbours.append(self.matrix[i + 1][j])  # Bot
            if j == self.c - 1:
                neighbours.append(self.matrix[i][0])  # Right
            else:
                neighbours.append(self.matrix[i][j + 1])  # Right
            neighbours.append(self.matrix[i - 1][j])  # Top
            neighbours.append(self.matrix[i][j - 1])  # Left
        return neighbours

    def set(self, value, i, j):
        self.matrix[i][j] = value

    def randPopulate(self):
        for i in range(self.r):
            for j in range(self.c):
                self.matrix[i][j] = chr(randint(67, 68))

    def computePayoffFor(self, i, j, mode = MOORE):
        neighbours = self.getNeighbours(i, j, mode)
        sumPayoffs = 0
        for neighbour in neighbours:
            sumPayoffs += computePayoff(self.matrix[i][j], neighbour[0])
        return sumPayoffs

    def computeAllPayoffs(self, mode = MOORE):
        for i in range(self.r):
            for j in range(self.c):
                self.matrix[i][j] = (self.matrix[i][j], self.computePayoffFor(i, j, mode))

    def selectBestAction(self, i, j, mode = MOORE):
        neighbours = self.getNeighbours(i, j, mode)
        neighbours.append(self.matrix[i][j])
        maxPayoff = 0
        for neighbour in neighbours:
            if neighbour[1] >= maxPayoff:
                maxPayoff = neighbour[1]
                nextAction = (neighbour[0],)
        self.matrix[i][j] = self.matrix[i][j] + nextAction

    def selectRandomAction(self, i, j, mode = MOORE):
        neighbours = self.getNeighbours(i, j, mode)
        targetNeighbour = neighbours[randint(0, len(neighbours)-1)]
        p = (1 + ((targetNeighbour[1]-self.matrix[i][j][1]) /  (len(neighbours)*10)))/2

        r = randint(0,100)
        r = r/100
        if(r <= p):
            take = True
        else:
            take = False

        if take:
            self.matrix[i][j] = self.matrix[i][j] + (targetNeighbour[0],)
        else:
            self.matrix[i][j] = self.matrix[i][j] + (self.matrix[i][j][0],)


    def selectAllBestAction(self, game, mode = MOORE):
        for i in range(self.r):
            for j in range(self.c):
                if game == "prisoners":
                    self.selectBestAction(i, j, mode)
                elif game == "snowdrift":
                    self.selectRandomAction(i, j, mode)

    def applyActions(self):
        for i in range(self.r):
            for j in range(self.c):
                self.matrix[i][j] = self.matrix[i][j][2]

    def run(self, round, mode, toPrint=False, neighborhood = MOORE):
        if(toPrint):
            print(self)
        self.computeCoopLevel()
        for i in range(round):
            self.computeAllPayoffs(neighborhood)
            self.selectAllBestAction("snowdrift", neighborhood)
            self.applyActions()
            y = self.matrix
            self.computeCoopLevel()
            if mode == "any":
                if i == 0 or i == 1 or i == 5 or i == 10 or i == 20 or i == 50:
                    print(str(i)+": "+str(self.coopHistory[len(self.coopHistory)-1]*100)+"%")
                    print(self)
            elif mode == "final":
                if i == 100:
                    print(str(i) + ": " + str(self.coopHistory[len(self.coopHistory) - 1] * 100) + "%")

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



