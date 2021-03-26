import math
from src import Stone


class Board:
    boardColors = [
        [7, 2, 1, 4, 3, 6, 5, 0],
        [6, 7, 4, 5, 2, 3, 0, 1],
        [5, 4, 7, 6, 1, 0, 3, 2],
        [4, 1, 2, 7, 0, 5, 6, 3],
        [3, 6, 5, 0, 7, 2, 1, 4],
        [2, 3, 0, 1, 6, 7, 4, 5],
        [1, 0, 3, 2, 5, 4, 7, 6],
        [0, 5, 6, 3, 4, 1, 2, 7],
    ]

    board = []
    turn = 0
    colorToMove = -1

    def __init__(self):
        self.turn = -1
        self.colorToMove = -1
        for i in range(8):
            self.board.append([None, None, None, None, None, None, None, None])

    def setupBoard(self):
        self.board = []
        self.__init__()

        for y in range(8):
            self.board[0][7 - y] = Stone.Stone(y, 1)
            self.board[7][y] = Stone.Stone(y, -1)

    def isMoveLegal(self, fromXy, toXy, side):
        if (fromXy[0] < 0 or fromXy[0] > 7 or fromXy[1] < 0 or fromXy[1] > 7 or toXy[0] < 0 or toXy[0] > 7 or toXy[1] < 0 or toXy[1] > 7):
            return [False, 'Position out of bounds']

        if (self.turn != side):
            return [False, 'Not your Turn']

        stone = self.board[fromXy[0]][fromXy[1]]

        if (stone == None):
            return [False, 'No Stone there']
        if (stone.side != side):
            return [False, 'Stone from wrong Side']
        if (self.board[toXy[0]][toXy[1]] != None):
            return [False, 'No moving onto Stone']
        if (self.colorToMove != -1 and self.colorToMove != stone.color):
            return [False, 'Wrong Color move']

        if (side * fromXy[0] >= side * toXy[0]):
            return [False, 'Incorrect forward Movement']
        if (fromXy[1] != toXy[1]):
            if (abs(fromXy[1] - toXy[1]) != abs(fromXy[0] - toXy[0])):
                return [False, 'Move not along diagonal']
        if (fromXy[1] == toXy[1]):
            # Straight Line
            for x in range(fromXy[0] + side, toXy[0], side):
                if (self.board[x][fromXy[1]] != None):
                    return [False, 'Piece in-between']
        else:
            # Diagonal Line
            for x in range(1, abs(fromXy[1] - toXy[1])):
                sign = int(math.copysign(1, toXy[1] - fromXy[1]))
                if (self.board[fromXy[0] + side * x][fromXy[1] + sign * x] != None):
                    return [False, 'Piece in-between']

        return [True, '']

    def moveStone(self, fromXy, toXy, player):
        moveLegal = self.isMoveLegal(fromXy, toXy, player)
        if moveLegal[0]:
            self.board[toXy[0]][toXy[1]] = self.board[fromXy[0]][fromXy[1]]
            self.board[fromXy[0]][fromXy[1]] = None

            self.turn *= -1
            # TODO: Rotate Board
            self.colorToMove = self.boardColors[toXy[1]][toXy[0]]
        else:
            raise Exception("Move-Error: " + moveLegal[1])

    def getStonePosition(self, color, side):
        for x in range(8):
            for y in range(8):
                stone = self.board[x][y]
                if (stone != None and stone.color == color and stone.side == side):
                    return [x, y]

    def getLegalMoves(self):
        legalMoves = []
        stonePosition = self.getStonePosition(self.colorToMove, self.turn)

        for x in range(1, (8 - stonePosition[0] if self.turn == 1 else stonePosition[0])):
            for i in range(-1, 2, 1):
                if self.isMoveLegal(stonePosition, [stonePosition[0] + self.turn * x, stonePosition[1] + i * x], self.turn)[0]:
                    legalMoves.append([stonePosition[0] + self.turn * x, stonePosition[1] + i * x])
        return legalMoves
