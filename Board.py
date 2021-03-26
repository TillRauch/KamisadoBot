import math
import Stone

class Board:
    board = []
    turn = 0

    def __init__(self):
        self.turn = -1
        for i in range(8):
            self.board.append([None, None, None, None, None, None, None, None])

    def setupBoard(self):
        self.board = []
        self.__init__()

        for y in range(8):
            self.board[0][7 - y] = Stone.Stone(y, 1)
            self.board[7][y] = Stone.Stone(y, -1)

    def isMoveLegal(self, fromXy, toXy, side):
        if (0 > fromXy[0] > 7 or 0 >fromXy[1] > 7 or 0 > toXy[0] > 7 or 0 > toXy[1] > 7):
            return [False, 'Position out of bounds']
        if (self.turn != side):
            return [False, 'Not your Turn']

        stone = self.board[fromXy[0]][fromXy[1]]

        if (stone == None):
            return [False, 'No Stone there']
        if (stone.side != side):
            return [False, 'Stone from wrong Side']
        if (fromXy[0] <= side * toXy[0]):
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

        return True







    def moveStone(self, fromXy, toXy, player):
        moveLegal = self.isMoveLegal(fromXy, toXy, player)
        if True:
            self.board[toXy[0]][toXy[1]] = self.board[fromXy[0]][fromXy[1]]
            self.board[fromXy[0]][fromXy[1]] = None

            self.turn *= -1
        else:
            raise Exception("Move-Error: " + moveLegal[1])

