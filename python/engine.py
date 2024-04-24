import game
import time
from copy import deepcopy
from itertools import product


def __make_occupy_consistent(board):
    for row, col in product(range(game.BLEN), repeat=2):
        occupied = any((row, col) in player.stones for player in (board.fst_player, board.snd_player))
        board.occupied[row][col] = occupied


def do_move(board: game.Board, target_pos: (int, int)):
    was_sumo_move = False
    sumo_pos = ((0, 0), (0, 0))
    old_color = board.current_color
    old_player = board.current_player
    someone_won = False
    winner_info = None
    was_deadlock = False


    def set_current_color_and_player():
        board.current_color = game.Board.get_board_color(target_pos)
        board.current_player = board._Board__other_player()

    if board.current_color is None:
        raise game.GameException('Must set a color first')
    if not board.is_in_bounds(target_pos):
        raise game.GameException('Cannot move stone out of bounds')
    sumo_level = board.current_player.sumo_levels[board.current_color]
    stone_pos = board.current_player.stones[board.current_color]

    try:
        board._Board__check_path(stone_pos, target_pos)
    except game.GameException as e:
        is_one_step_move = target_pos[0] - stone_pos[0] == board._Board__direction()
        if sumo_level > 0 and is_one_step_move and stone_pos[1] == target_pos[1]:
            target_pos = board._Board__check_sumo(target_pos)
            was_sumo_move = True
            sumo_pos = (stone_pos, target_pos)
            board._Board__sumo_cascade(stone_pos, target_pos)
        else:
            raise e
    else:
        if abs(target_pos[0] - stone_pos[0]) > game.Board.SUMO_STATS['range'][sumo_level]:
            raise game.GameException('Move exceeds max range')
        board._Board__move_stone(board.current_player, board.current_color, target_pos)
        if target_pos[0] == board._Board__other_player().start_row:
            someone_won = True
            winner_info = (board.current_player, board.current_color)
            board._Board__process_round_winner(board.current_player)
            board.turn_count += 1
            return [old_color, old_player, stone_pos, was_sumo_move, sumo_pos, someone_won, winner_info, was_deadlock]
    board.turn_count += 1  # player 0 made this move
    set_current_color_and_player()  # now current player is 1
    if not board.get_legal_moves():  # then skip move
        target_pos = board.current_player.stones[board.current_color]
        set_current_color_and_player()  # now current player is 0
        if not board.get_legal_moves():  # deadlock, causing player 0 loses, player 1 wins
            was_deadlock = True
            target_pos = board.current_player.stones[board.current_color]
            set_current_color_and_player()
            someone_won = True
            winner_info = (board.current_player, board.current_color)
            board._Board__process_round_winner(board.current_player)
    return [old_color, old_player, stone_pos, was_sumo_move, sumo_pos, someone_won, winner_info, was_deadlock]

def undo_move(board: game.Board, move_info):
    board.turn_count -= 1
    board.current_color = move_info[0]
    board.current_player = move_info[1]
    board.winner = None
    board.round_over = False

    if move_info[5]:  # someone won
        winner_info = move_info[6]
        winner_info[0].sumo_levels[winner_info[1]] -= 1

    if move_info[3]: # was_sumo_move
        sumo_pos = move_info[4]
        board._Board__sumo_cascade(sumo_pos[1], sumo_pos[0])
    else:
        board._Board__move_stone(board.current_player, board.current_color, move_info[2])


class Engine:

    INF = 9999
    END_SCORE = 1000
    current_best_move = (10, 10)
    max_depth = 100
    current_depth = 1
    positions_evaluated = 0
    start_time = 0

    @staticmethod
    def has_winning_move(board: game.Board, player, color=None):
        previous_player = board.current_player
        board.current_player = player
        winning_row = board._Board__other_player().start_row
        has_winning_move = any(map(lambda x: x[0] == winning_row, board.get_legal_moves(color)))
        board.current_player = previous_player
        return has_winning_move

    @staticmethod
    def winning_stone_count(board: game.Board, player: game.Player):
        return len(list(filter(lambda x: Engine.has_winning_move(board, player, color=x), range(8))))

    @staticmethod
    def available_colors_count(board: game.Board, player: game.Player, color):
        previous_player = board.current_player
        board.current_player = player
        total_available = set({})
        for move_pos in board.get_legal_moves(color):
            total_available.add(game.Board.get_board_color(move_pos))

        board.current_player = previous_player
        return len(total_available)

    @staticmethod
    def avg_color_diversity(board, player):
        return sum(Engine.available_colors_count(board, player, color) for color in range(8)) / 8

    def get_move(self, current_board: game.Board, time_to_calc):
        self.start_time = time.time() * 1000
        while time.time() * 1000 - self.start_time < time_to_calc - 50:
            if self.current_depth >= self.max_depth:
                break
            eval_score = self.search(current_board, self.current_depth, 0, -self.INF, self.INF)
            self.current_depth += 1

        board_copy = deepcopy(current_board)
        board_copy.perform_move(self.current_best_move)
        if self.sees_win(eval_score):
            debug = ["Win in " + str(self.win_in(eval_score) - 1) + " half-moves for " + "me" if eval_score > 0 else "you"]
        else:
            debug = ["evaluation-score: " + str(-eval_score)]
        debug += [str(self.positions_evaluated) + " evaluted positions",
                     "to a depth of " + str(self.current_depth)]

        return self.current_best_move, debug

    def search(self, board: game.Board, depth, wurzel_abs, alpha, beta):
        if depth == 0:
            self.positions_evaluated += 1
            return self.score_position(board)
        if wurzel_abs > 0:
            alpha = max(alpha, -self.END_SCORE + wurzel_abs)
            beta = min(beta, self.END_SCORE - wurzel_abs)
            if alpha >= beta:
                return alpha

        if board.round_over:
            return -self.END_SCORE + wurzel_abs
        if wurzel_abs > 0 and alpha >= beta:
            return alpha

        current_piece_pos = board.current_player.stones[board.current_color]
        possible_moves = board.get_legal_moves()
        sorted_moves = reversed(sorted(possible_moves, key=lambda x: abs(x[0]-current_piece_pos[0])))
        for move in sorted_moves:
            print('         ' * (self.current_depth-depth) + str(depth) + ' - Evaluating move' + str(move))
            move_info = do_move(board, move)
            if (move_info[1] == board.current_player and not board.round_over) or move_info[7]:
                evaluation = self.search(board, depth - 1, wurzel_abs + 1, alpha, beta)
            else:
                print(move_info[7])
                evaluation = -self.search(board, depth - 1, wurzel_abs + 1, -beta, -alpha)

            print(evaluation)

            undo_move(board, move_info)

            if evaluation >= beta:
                return beta
            if evaluation > alpha:
                alpha = evaluation

                if wurzel_abs == 0:
                    self.current_best_move = move

        return alpha

    def score_position(self, board: game.Board):
        if self.has_winning_move(board, board.current_player):
            return self.INF

        winning_stone_diff = self.winning_stone_count(board, board.current_player) - self.winning_stone_count(board, board._Board__other_player())
        color_div_diff = self.avg_color_diversity(board, board.current_player) - self.avg_color_diversity(board, board._Board__other_player())
        return winning_stone_diff + color_div_diff

    def sees_win(self, evaluation):
        if self.END_SCORE - abs(evaluation) < self.max_depth:
            return True
        else:
            return False

    def win_in(self, evaluation):
        return self.END_SCORE - abs(evaluation)


if __name__ == '__main__':
    board = game.Board()
    engine = Engine()

    board.set_color(3)
    board.perform_move((3, 3))
    board.perform_move((4, 0))
    board.draw().show()

    print(engine.get_move(board))
