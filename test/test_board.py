from python import game
import pytest

correctMoveTuple = [(5, 0), (1, 0)]

presetBoard = game.Board()
presetBoard.move_stone((5, 0), 0)
presetBoard.move_stone((4, 5))
presetBoard.move_stone((5, 6))
presetBoard.move_stone((4, 3))


def test_get_legal_moves():
    board = game.Board()
    board.move_stone((6, 0), 0)

    assert set(board.get_legal_moves()) == {(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2),
                                          (1, 1), (2, 0),
                                          (1, 3), (2, 4), (3, 5), (4, 6), (5, 7)}


def test_some_legal_moves():
    try:
        presetBoard.check_move(correctMoveTuple[0], correctMoveTuple[1])
    except Exception:
        pytest.fail('Legal moves raised an exception')


def test_is_in_bounds():
    assert presetBoard.is_in_bounds((1, 0))
    assert not presetBoard.is_in_bounds((8, 0))


def test_illegal_moving_onto_stone():
    with pytest.raises(Exception, match='No moving onto Stone'):
        presetBoard.check_move(correctMoveTuple[0], (0, 0))


def test_is_occupied():
    assert presetBoard.is_occupied((5, 0))
    assert not presetBoard.is_occupied((6, 0))


def test_illegal_forward_movement_first():
    with pytest.raises(Exception, match='Incorrect forward Movement'):
        presetBoard.check_move(correctMoveTuple[0], (6, 0))


def test_illegal_forward_movement_second():
    board = game.Board()
    board.move_stone((5, 0), 0)
    board.move_stone((4, 5))
    board.move_stone((5, 6))
    board.move_stone((4, 3))
    board.move_stone((3, 0))

    with pytest.raises(Exception, match='Incorrect forward Movement'):
        board.check_move((4, 3), (2, 3))


def test_illegal_diagonal_movement():
    with pytest.raises(Exception, match='Move not along diagonal'):
        presetBoard.check_move(correctMoveTuple[0], (1, 1))


def test_illegal_move_over_stone_straight():
    board = game.Board()
    board.move_stone((5, 0), 0)
    board.move_stone((1, 2))
    board.move_stone((5, 2))
    board.move_stone((1, 7))
    board.move_stone((4, 5))

    with pytest.raises(Exception, match='Piece in-between'):
        board.check_move((1, 2), (6, 2))


def test_illegal_move_over_stone_diagonal():
    board = game.Board()
    board.move_stone((5, 0), 0)
    board.move_stone((2, 3))
    board.move_stone((4, 5))

    with pytest.raises(Exception, match='Piece in-between'):
        board.check_move((2, 3), (5, 6))