import unittest
from ..src import Board
from ..src import Stone

class TestBoard(unittest.TestCase):

    correctMoveTuple = [[5, 0], [1, 0], -1]

    def test_someLegalMoves(self):
        board = Board.Board()
        board.setupBoard()

        board.moveStone([7, 0], [5, 0], -1)
        board.moveStone([0, 1], [4, 5], 1)
        board.moveStone([7, 6], [5, 6], -1)
        board.moveStone([0, 3], [4, 3], 1)

        self.assertEquals(board.isMoveLegal(self.correctMoveTuple[0],
                                            self.correctMoveTuple[1],
                                            self.correctMoveTuple[2],
                                            ), [True, ''])

    def test_illegalMove_OutOfBounds(self):
        board = Board.Board()
        board.setupBoard()

        board.moveStone([7, 0], [5, 0], -1)
        board.moveStone([0, 1], [4, 5], 1)
        board.moveStone([7, 6], [5, 6], -1)
        board.moveStone([0, 3], [4, 3], 1)

        self.assertEquals(board.isMoveLegal([8, 0],
                                            self.correctMoveTuple[1],
                                            self.correctMoveTuple[2],
                                            ), [False, 'Position out of bounds'])

    def test_illegalMove_WrongTurn(self):
        board = Board.Board()
        board.setupBoard()

        board.moveStone([7, 0], [5, 0], -1)
        board.moveStone([0, 1], [4, 5], 1)
        board.moveStone([7, 6], [5, 6], -1)
        board.moveStone([0, 3], [4, 3], 1)

        self.assertEquals(board.isMoveLegal(self.correctMoveTuple[0],
                                            self.correctMoveTuple[1],
                                            1), [False, 'Not your Turn'])

    def test_illegalMove_NoPieceThere(self):
        board = Board.Board()
        board.setupBoard()

        board.moveStone([7, 0], [5, 0], -1)
        board.moveStone([0, 1], [4, 5], 1)
        board.moveStone([7, 6], [5, 6], -1)
        board.moveStone([0, 3], [4, 3], 1)

        self.assertEquals(board.isMoveLegal([3, 3],
                                            self.correctMoveTuple[1],
                                            self.correctMoveTuple[2],
                                            ), [False, 'No Stone there'])

    def test_illegalMove_WrongSidePiece(self):
        board = Board.Board()
        board.setupBoard()

        board.moveStone([7, 0], [5, 0], -1)
        board.moveStone([0, 1], [4, 5], 1)
        board.moveStone([7, 6], [5, 6], -1)
        board.moveStone([0, 3], [4, 3], 1)

        self.assertEquals(board.isMoveLegal([4, 3],
                                            self.correctMoveTuple[1],
                                            self.correctMoveTuple[2],
                                            ), [False, 'Stone from wrong Side'])

    def test_illegalMove_WrongColorMove(self):
        board = Board.Board()
        board.setupBoard()

        board.moveStone([7, 0], [5, 0], -1)
        board.moveStone([0, 1], [4, 5], 1)
        board.moveStone([7, 6], [5, 6], -1)
        board.moveStone([0, 3], [4, 3], 1)

        self.assertEquals(board.isMoveLegal([7, 1],
                                            [6, 1],
                                            self.correctMoveTuple[2],
                                            ), [False, 'Wrong Color move'])


if __name__ == '__main__':
    unittest.main()