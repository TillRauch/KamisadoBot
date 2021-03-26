import unittest
from ..src import Board

class TestBoard(unittest.TestCase):

    correctMoveTuple = [[5, 0], [1, 0], -1]

    presetBoard = Board.Board()
    presetBoard.setupBoard()
    presetBoard.moveStone([7, 0], [5, 0], -1)
    presetBoard.moveStone([0, 1], [4, 5], 1)
    presetBoard.moveStone([7, 6], [5, 6], -1)
    presetBoard.moveStone([0, 3], [4, 3], 1)

    def test_getLegalMoves(self):
        board = Board.Board()
        board.setupBoard()

        board.moveStone([7, 0], [6, 0], -1)

        self.assertCountEqual(board.getLegalMoves(), [[1, 2], [2, 2], [3, 2], [4, 2], [5, 2], [6, 2],
                                                      [1, 1], [2, 0],
                                                      [1, 3], [2, 4], [3, 5], [4, 6], [5, 7]
                                                      ])

    def test_someLegalMoves(self):

        self.assertEqual(self.presetBoard.isMoveLegal(self.correctMoveTuple[0],
                                            self.correctMoveTuple[1],
                                            self.correctMoveTuple[2],
                                            ), [True, ''])

    def test_illegalMove_OutOfBounds(self):

        self.assertEqual(self.presetBoard.isMoveLegal([8, 0],
                                            self.correctMoveTuple[1],
                                            self.correctMoveTuple[2],
                                            ), [False, 'Position out of bounds'])

    def test_illegalMove_Turn(self):

        self.assertEqual(self.presetBoard.isMoveLegal(self.correctMoveTuple[0],
                                            self.correctMoveTuple[1],
                                            1), [False, 'Not your Turn'])

    def test_illegalMove_PieceThere(self):

        self.assertEqual(self.presetBoard.isMoveLegal([3, 3],
                                            self.correctMoveTuple[1],
                                            self.correctMoveTuple[2],
                                            ), [False, 'No Stone there'])

    def test_illegalMove_SidePiece(self):

        self.assertEqual(self.presetBoard.isMoveLegal([4, 3],
                                            self.correctMoveTuple[1],
                                            self.correctMoveTuple[2],
                                            ), [False, 'Stone from wrong Side'])

    def test_illegalMove_ColorMove(self):

        self.assertEqual(self.presetBoard.isMoveLegal([7, 1],
                                            [6, 1],
                                            self.correctMoveTuple[2],
                                            ), [False, 'Wrong Color move'])

    def test_illegalMove_WrongForwardMovementBottom(self):

        self.assertEqual(self.presetBoard.isMoveLegal(self.correctMoveTuple[0],
                                            [6, 0],
                                            self.correctMoveTuple[2],
                                            ), [False, 'Incorrect forward Movement'])

    def test_illegalMove_WrongForwardMovementTop(self):
        board = Board.Board()
        board.setupBoard()

        board.moveStone([7, 0], [5, 0], -1)
        board.moveStone([0, 1], [4, 5], 1)
        board.moveStone([7, 6], [5, 6], -1)
        board.moveStone([0, 3], [4, 3], 1)
        board.moveStone(self.correctMoveTuple[0], [3, 2], self.correctMoveTuple[2])

        self.assertEqual(board.isMoveLegal([4, 5],
                                            [2, 5],
                                            1,
                                            ), [False, 'Incorrect forward Movement'])

    def test_illegalMove_DiagonalMove(self):

        self.assertEqual(self.presetBoard.isMoveLegal(self.correctMoveTuple[0],
                                           [1, 1],
                                           self.correctMoveTuple[2],
                                           ), [False, 'Move not along diagonal'])

    def test_illegalMove_MoveOverPieceStraight(self):
        board = Board.Board()
        board.setupBoard()

        board.moveStone([7, 0], [5, 0], -1)
        board.moveStone([0, 1], [1, 2], 1)
        board.moveStone([7, 4], [5, 2], -1)
        board.moveStone([0, 7], [1, 7], 1)
        board.moveStone([7, 5], [4, 5], -1)

        self.assertEqual(board.isMoveLegal([1, 2],
                                           [6, 2],
                                           1,
                                           ), [False, 'Piece in-between'])

    def test_illegalMove_MoveOverPieceDiagonal(self):
        board = Board.Board()
        board.setupBoard()

        board.moveStone([7, 0], [5, 0], -1)
        board.moveStone([0, 1], [2, 3], 1)
        board.moveStone([7, 2], [4, 5], -1)

        self.assertEqual(board.isMoveLegal([2, 3],
                                           [5, 6],
                                           1, ), [False, 'Piece in-between'])


if __name__ == '__main__':
    unittest.main()