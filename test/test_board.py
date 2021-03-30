import pytest
import game

correctMoveTuple = [(5, 0), (1, 0)]

presetBoard = game.Board()
presetBoard.set_color(0)
presetBoard.perform_move((5, 0))
presetBoard.perform_move((4, 5))
presetBoard.perform_move((5, 6))
presetBoard.perform_move((4, 3))


def helper_recalculate_board(board):
    for x in range(game.BLEN):
        for y in range(game.BLEN):
            board.board[x][y] = (x, y) in board.players[0].stones or (x, y) in board.players[1].stones

def test_get_legal_moves():
    board = game.Board()
    board.set_color(0)
    board.perform_move((6, 0))

    assert set(board.get_legal_moves()) == {(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2),
                                            (1, 1), (2, 0),
                                            (1, 3), (2, 4), (3, 5), (4, 6), (5, 7)}


def test_some_legal_moves():
    try:
        presetBoard._Board__check_path_clear(correctMoveTuple[0], correctMoveTuple[1])
    except game.GameException:
        pytest.fail('Legal moves raised an BoardException')


def test_is_in_bounds():
    assert presetBoard.is_in_bounds((1, 0))
    assert not presetBoard.is_in_bounds((8, 0))


def test_illegal_moving_onto_stone():
    with pytest.raises(game.GameException, match='No moving onto stone'):
        presetBoard._Board__check_path_clear(correctMoveTuple[0], (0, 0))


def test_is_occupied():
    assert presetBoard._Board__is_occupied((5, 0))
    assert not presetBoard._Board__is_occupied((6, 0))


def test_illegal_forward_movement_first():
    with pytest.raises(game.GameException, match='Incorrect forward movement'):
        presetBoard._Board__check_path_clear(correctMoveTuple[0], (6, 0))


def test_illegal_forward_movement_second():
    board = game.Board()
    board.set_color(0)
    board.perform_move((5, 0))
    board.perform_move((4, 5))
    board.perform_move((5, 6))
    board.perform_move((4, 3))
    board.perform_move((3, 0))

    with pytest.raises(game.GameException, match='Incorrect forward movement'):
        board._Board__check_path_clear((4, 3), (2, 3))


def test_illegal_diagonal_movement():
    with pytest.raises(game.GameException, match='Move not along diagonal'):
        presetBoard._Board__check_path_clear(correctMoveTuple[0], (1, 1))


def test_illegal_move_over_stone_straight():
    board = game.Board()
    board.set_color(0)
    board.perform_move((5, 0))
    board.perform_move((1, 2))
    board.perform_move((5, 2))
    board.perform_move((1, 7))
    board.perform_move((4, 5))

    with pytest.raises(game.GameException, match='Piece in-between'):
        board._Board__check_path_clear((1, 2), (6, 2))


def test_illegal_move_over_stone_diagonal():
    board = game.Board()
    board.set_color(0)
    board.perform_move((5, 0))
    board.perform_move((2, 3))
    board.perform_move((4, 5))

    with pytest.raises(game.GameException, match='Piece in-between'):
        board._Board__check_path_clear((2, 3), (5, 6))


def test_illegal_move_too_long_white():
    board = game.Board()
    board.set_color(0)

    board.players[0].sumo_levels[0] = 1

    with pytest.raises(game.GameException, match='Move exceeds max range'):
        board.perform_move((1, 0))


def test_sumo_move_just_in_range():
    board = game.Board()
    board.set_color(0)

    board.players[0].sumo_levels[0] = 1

    try:
        board.perform_move((2, 0))
    except game.GameException:
        pytest.fail('Legal moves raised an BoardException')


def test_illegal_move_too_long_black():
    board = game.Board()
    board.set_color(0)
    board.perform_move((6, 1))

    board.players[1].sumo_levels[0] = 1

    with pytest.raises(game.GameException, match='Move exceeds max range'):
        board.perform_move((6, 7))

def test_reset_stones_from_left():
    board = game.Board()

    board.players[0].stones = [(7, 0), (7, 1), (7, 2), (6, 0), (6, 1), (6, 2), (0, 0), (1, 0)]
    board.players[1].stones = [(0, 7), (0, 6), (1, 7), (1, 6), (0, 5), (0, 4), (0, 3), (0, 2)]

    board.round_over = True
    board.reset(from_right=False)
    assert board.players[0].stones == [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 7), (7, 6)]
    assert board.players[1].stones == [(0, 7), (0, 6), (0, 1), (0, 0), (0, 5), (0, 4), (0, 3), (0, 2)]


def test_reset_stones_from_right():
    board = game.Board()

    board.players[0].stones = [(7, 0), (7, 1), (7, 2), (6, 0), (6, 1), (6, 2), (0, 0), (1, 0)]
    board.players[1].stones = [(0, 7), (0, 6), (1, 7), (1, 6), (0, 5), (0, 4), (0, 3), (0, 2)]

    board.round_over = True
    board.reset(from_right=True)
    assert board.players[0].stones == [(7, 5), (7, 6), (7, 7), (7, 2), (7, 3), (7, 4), (7, 0), (7, 1)]
    assert board.players[1].stones == [(0, 5), (0, 4), (0, 7), (0, 6), (0, 3), (0, 2), (0, 1), (0, 0)]

def test_illegal_sumo_own_stone():
    board = game.Board()
    board.players[0].stones = [(4, 4), (3, 4), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    board.players[1].stones = [(0, 7), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]

    board.players[0].sumo_levels = [1, 0, 0, 0, 0, 0, 0, 0]
    board.set_color(0)
    helper_recalculate_board(board)

    with pytest.raises(game.GameException, match='Sumo cannot push own stone'):
        board.perform_move((3, 4))



def test_single_sumo():
    board = game.Board()
    board.players[0].stones = [(4, 4), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    board.players[1].stones = [(3, 4), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]

    board.players[0].sumo_levels = [1, 0, 0, 0, 0, 0, 0, 0]
    board.set_color(0)

    helper_recalculate_board(board)
    board.perform_move((3, 4))

    assert board.players[0].stones == [(3, 4), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    assert board.players[1].stones == [(2, 4), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]
    assert board.current_player == 1
    assert board.current_color == 5  # Lila

def test_double_sumo():
    board = game.Board()
    board.players[0].stones = [(4, 4), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    board.players[1].stones = [(3, 4), (2, 4), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]

    board.players[0].sumo_levels = [2, 0, 0, 0, 0, 0, 0, 0]
    board.set_color(0)

    helper_recalculate_board(board)
    board.perform_move((3, 4))

    assert board.players[0].stones == [(3, 4), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    assert board.players[1].stones == [(2, 4), (1, 4), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]
    assert board.current_player == 1
    assert board.current_color == 6  # Lila
