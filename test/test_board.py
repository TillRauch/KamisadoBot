from itertools import product

import pytest
import game


@pytest.fixture
def preset_board():
    board = game.Board()
    board.set_color(0)
    board.perform_move((5, 0))
    board.perform_move((4, 5))
    board.perform_move((5, 6))
    board.perform_move((4, 3))
    return board


def __make_occupy_consistent(board):
    for row, col in product(range(game.BLEN), repeat=2):
        occupied = any((row, col) in player.stones for player in (board.fst_player, board.snd_player))
        board.occupied[row][col] = occupied


def test_get_legal_moves():
    board = game.Board()
    board.set_color(0)
    board.perform_move((6, 0))
    assert set(board.get_legal_moves()) == {(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2),
                                            (1, 1), (2, 0),
                                            (1, 3), (2, 4), (3, 5), (4, 6), (5, 7)}


def test_some_legal_moves(preset_board):
    try:
        preset_board.perform_move((1, 0))
    except game.GameException:
        pytest.fail('Legal move raised an BoardException')


def test_is_in_bounds(preset_board):
    assert preset_board.is_in_bounds((1, 0))
    assert not preset_board.is_in_bounds((8, 0))


def test_illegal_moving_onto_stone(preset_board):
    with pytest.raises(game.GameException, match='Cannot move onto stone'):
        preset_board.perform_move((0, 0))


def test_illegal_forward_movement_first(preset_board):
    with pytest.raises(game.GameException, match='Can only move forward'):
        preset_board.perform_move((6, 0))


def test_illegal_forward_movement_second():
    board = game.Board()
    board.set_color(0)
    board.perform_move((5, 0))
    board.perform_move((4, 5))
    board.perform_move((5, 6))
    board.perform_move((4, 3))
    board.perform_move((3, 0))
    with pytest.raises(game.GameException, match='Can only move forward'):
        board.perform_move((2, 3))


def test_illegal_diagonal_movement(preset_board):
    with pytest.raises(game.GameException, match='Can only move straight or diagonally'):
        preset_board.perform_move((1, 1))


def test_illegal_move_over_stone_straight():
    board = game.Board()
    board.set_color(0)
    board.perform_move((5, 0))
    board.perform_move((1, 2))
    board.perform_move((5, 2))
    board.perform_move((1, 7))
    board.perform_move((4, 5))
    with pytest.raises(game.GameException, match='Cannot move through pieces'):
        board.perform_move((6, 2))


def test_illegal_move_over_stone_diagonal():
    board = game.Board()
    board.set_color(0)
    board.perform_move((5, 0))
    board.perform_move((2, 3))
    board.perform_move((4, 5))
    with pytest.raises(game.GameException, match='Cannot move through pieces'):
        board.perform_move((5, 6))


def test_illegal_move_too_long_white():
    board = game.Board()
    board.set_color(0)
    board.fst_player.sumo_levels[0] = 1
    with pytest.raises(game.GameException, match='Move exceeds max range'):
        board.perform_move((1, 0))


def test_sumo_move_just_in_range():
    board = game.Board()
    board.set_color(0)
    board.fst_player.sumo_levels[0] = 1
    try:
        board.perform_move((2, 0))
    except game.GameException:
        pytest.fail('Legal moves raised an BoardException')


def test_illegal_move_too_long_black():
    board = game.Board()
    board.set_color(0)
    board.perform_move((6, 1))
    board.snd_player.sumo_levels[0] = 1
    with pytest.raises(game.GameException, match='Move exceeds max range'):
        board.perform_move((6, 7))


def test_reset_stones_from_left():
    board = game.Board()
    board.fst_player.stones = [(7, 0), (7, 1), (7, 2), (6, 0), (6, 1), (6, 2), (0, 0), (1, 0)]
    board.snd_player.stones = [(0, 7), (0, 6), (1, 7), (1, 6), (0, 5), (0, 4), (0, 3), (0, 2)]

    board.round_over = True
    board.reset(from_right=False)
    assert board.fst_player.stones == [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 7), (7, 6)]
    assert board.snd_player.stones == [(0, 7), (0, 6), (0, 1), (0, 0), (0, 5), (0, 4), (0, 3), (0, 2)]


def test_reset_stones_from_right():
    board = game.Board()
    board.fst_player.stones = [(7, 0), (7, 1), (7, 2), (6, 0), (6, 1), (6, 2), (0, 0), (1, 0)]
    board.snd_player.stones = [(0, 7), (0, 6), (1, 7), (1, 6), (0, 5), (0, 4), (0, 3), (0, 2)]

    board.round_over = True
    board.reset(from_right=True)
    assert board.fst_player.stones == [(7, 5), (7, 6), (7, 7), (7, 2), (7, 3), (7, 4), (7, 0), (7, 1)]
    assert board.snd_player.stones == [(0, 5), (0, 4), (0, 7), (0, 6), (0, 3), (0, 2), (0, 1), (0, 0)]


def test_illegal_sumo_own_stone():
    board = game.Board()
    board.fst_player.stones = [(4, 4), (3, 4), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    board.snd_player.stones = [(0, 7), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]
    __make_occupy_consistent(board)

    board.fst_player.sumo_levels[0] = 1
    board.set_color(0)

    with pytest.raises(game.GameException, match='Sumo cannot push own stone'):
        board.perform_move((3, 4))


def test_illegal_sumo_push_off_board():
    board = game.Board()
    board.fst_player.stones = [(2, 7), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    board.snd_player.stones = [(0, 7), (1, 7), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]
    __make_occupy_consistent(board)

    board.fst_player.sumo_levels[0] = 2
    board.set_color(0)

    with pytest.raises(game.GameException, match='Sumo cannot push off the board'):
        board.perform_move((1, 7))


def test_illegal_sumo_cant_push_other_sumo():
    board = game.Board()
    board.fst_player.stones = [(4, 3), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    board.snd_player.stones = [(3, 3), (0, 4), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]
    __make_occupy_consistent(board)

    board.fst_player.sumo_levels[0] = 1
    board.snd_player.sumo_levels[0] = 1
    board.set_color(0)

    with pytest.raises(game.GameException, match='Sumo cannot push same strength sumo'):
        board.perform_move((3, 3))


def test_sumo_push_weaker_sumo():
    board = game.Board()
    board.fst_player.stones = [(4, 3), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    board.snd_player.stones = [(3, 3), (0, 4), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]
    __make_occupy_consistent(board)

    board.fst_player.sumo_levels[0] = 2
    board.snd_player.sumo_levels[0] = 1
    board.set_color(0)
    board.perform_move((3, 3))

    assert board.fst_player.stones == [(3, 3), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    assert board.snd_player.stones == [(2, 3), (0, 4), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]


def test_sumo_max_off_board():
    board = game.Board()
    board.fst_player.stones = [(4, 7), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    board.snd_player.stones = [(1, 7), (2, 7), (3, 7), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]
    __make_occupy_consistent(board)

    board.fst_player.sumo_levels[0] = 3
    board.set_color(0)
    board.perform_move((3, 7))

    assert board.fst_player.stones == [(3, 7), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    assert board.snd_player.stones == [(0, 7), (1, 7), (2, 7), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]
    assert board.current_color == 0  # Braun


def test_single_sumo():
    board = game.Board()
    board.fst_player.stones = [(4, 4), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    board.snd_player.stones = [(3, 4), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]
    __make_occupy_consistent(board)

    board.fst_player.sumo_levels[0] = 1
    board.set_color(0)
    board.perform_move((3, 4))

    assert board.fst_player.stones == [(3, 4), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    assert board.snd_player.stones == [(2, 4), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]
    assert board.current_player == board.snd_player
    assert board.current_color == 5  # Lila


def test_double_sumo():
    board = game.Board()
    board.fst_player.stones = [(4, 4), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    board.snd_player.stones = [(3, 4), (2, 4), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]
    __make_occupy_consistent(board)

    board.fst_player.sumo_levels[0] = 2
    board.set_color(0)
    board.perform_move((3, 4))

    assert board.fst_player.stones == [(3, 4), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    assert board.snd_player.stones == [(2, 4), (1, 4), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]
    assert board.current_player == board.snd_player
    assert board.current_color == 6  # Blau


def test_rare_crash():
    board = game.Board()
    board.fst_player.stones = [(3, 4), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    board.snd_player.stones = [(2, 4), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]
    board.fst_player.sumo_levels = [1, 0, 0, 0, 0, 0, 0, 0]
    board.set_color(0)
    __make_occupy_consistent(board)
    move_list = [(2, 4), (4, 1), (2, 2), (2, 0), (5, 1),
                 (1, 3), (4, 2), (1, 6), (1, 4)]
    for move in move_list:
        board.perform_move(move)
    board.perform_move((4, 3))
