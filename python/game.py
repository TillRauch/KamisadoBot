import draw


class GameException(Exception):
    pass


BLEN = 8


class Player:
    def __init__(self, name, stones):
        self.name = name
        self.stones = stones
        self.start_row = stones[0][0]
        self.sumo_levels = [0] * BLEN

    def get_points(self):
        return sum(Board.SUMO_STATS[lvl]['points'] for lvl in self.sumo_levels)

    def reset_stones(self, flip_col_order):
        def flip_stones(flip_row=False, flip_col=False):
            return [(pos[0] * (1, -1)[flip_row],
                     pos[1] * (1, -1)[flip_col]) for pos in self.stones]
        stones = flip_stones(flip_row=self.start_row > 0, flip_col=flip_col_order)
        sorted_colors = sorted(range(BLEN), key=stones.__getitem__)
        if flip_col_order:
            sorted_colors.reverse()
        for place, color in enumerate(sorted_colors):
            self.stones[color] = self.start_row, place


class Board:
    BOARD_COLORS = [
        [7, 6, 5, 4, 3, 2, 1, 0],
        [2, 7, 4, 1, 6, 3, 0, 5],
        [1, 4, 7, 2, 5, 0, 3, 6],
        [4, 5, 6, 7, 0, 1, 2, 3],
        [3, 2, 1, 0, 7, 6, 5, 4],
        [6, 3, 0, 5, 2, 7, 4, 1],
        [5, 0, 3, 6, 1, 4, 7, 2],
        [0, 1, 2, 3, 4, 5, 6, 7]
    ]

    SUMO_STATS = [{
        'range': BLEN,
        'power': 0,
        'points': 0
    }, {
        'range': 5,
        'power': 1,
        'points': 1
    }, {
        'range': 3,
        'power': 2,
        'points': 3
    }, {
        'range': 1,
        'power': 3,
        'points': 7
    }, {
        'range': 0,
        'power': 0,
        'points': 15
    }]

    @staticmethod
    def get_start_board():
        return [[True] * BLEN] + [[False] * BLEN for i in range(BLEN - 2)] + [[True] * BLEN]

    @staticmethod
    def get_board_color(pos):
        return Board.BOARD_COLORS[pos[0]][pos[1]]

    @staticmethod
    def is_in_bounds(pos):
        return all(0 <= coord < BLEN for coord in pos)

    def __init__(self, winning_points=3):
        self.winning_points = winning_points
        self.turn_count = 0
        self.round_over = False
        self.winner = None
        self.current_color = None
        self.board = Board.get_start_board()
        fst_player = Player('White', [(BLEN - 1, i) for i in range(BLEN)])
        snd_player = Player('Black', [(0, i) for i in reversed(range(BLEN))])
        self.players = (fst_player, snd_player)
        self.current_player = 0

    def __direction(self):
        return (-1, 1)[self.current_player]

    def __is_occupied(self, pos):
        return self.board[pos[0]][pos[1]]

    def __occupy(self, pos):
        self.board[pos[0]][pos[1]] = True

    def __unoccupy(self, pos):
        self.board[pos[0]][pos[1]] = False

    def __get_stone_color(self, pos):
        if not self.__is_occupied(pos):
            raise GameException('Position is not occupied')
        try:
            return self.players[0].stones.index(pos)
        except ValueError:
            return self.players[1].stones.index(pos)

    def __check_path_clear(self, start_pos, target_pos):
        assert self.__is_occupied(start_pos), 'inconsistent state'
        if self.__is_occupied(target_pos):
            raise GameException('No moving onto stone')
        if self.__direction() * (target_pos[0] - start_pos[0]) <= 0:
            raise GameException('Incorrect forward movement')
        row_path = range(start_pos[0] + self.__direction(), target_pos[0], self.__direction())
        # if line straight
        if start_pos[1] == target_pos[1]:
            col_path = [start_pos[1]] * len(row_path)
        else:
            if abs(start_pos[1] - target_pos[1]) != abs(start_pos[0] - target_pos[0]):
                raise GameException('Move not along diagonal')
            diag_direction = 1 if target_pos[1] > start_pos[1] else -1
            col_path = range(start_pos[1] + diag_direction, target_pos[1], diag_direction)
        if any(self.board[row][col] for row, col in zip(row_path, col_path)):
            raise GameException('Piece in-between')

    def __process_round_winner(self, winner):
        self.round_over = True
        self.players[winner].sumo_levels[self.current_color] += 1
        if self.players[winner].get_points() >= self.winning_points:
            self.winner = winner

    def __sumo_cascade(self, start_pos, length):
        current_pos = (start_pos[0] + self.__direction() * length, start_pos[1])
        assert not self.__is_occupied(current_pos)
        self.__occupy(current_pos)
        while current_pos != start_pos:
            next_pos = (current_pos[0] - self.__direction(), current_pos[1])
            self.__move_stone(next_pos, current_pos)
            current_pos = next_pos
        self.__unoccupy(start_pos)


    def __move_stone(self, stone_pos, target_pos): # hard move onto new position, no fucks given
        stone_owner = bool(stone_pos in self.players[1].stones)
        stone_color = self.__get_stone_color(stone_pos)
        self.__unoccupy(stone_pos)
        self.__occupy(target_pos)
        self.players[stone_owner].stones[stone_color] = target_pos

    def set_color(self, color):
        if self.turn_count > 0:
            raise GameException('Can only set color on first turn')
        self.current_color = color


    def perform_move(self, target_pos):
        def set_current_color_and_player():
            self.current_color = Board.get_board_color(target_pos)
            self.current_player = 1 - self.current_player  # now current player is 1
        if self.current_color is None:
            raise GameException('Must set a color first')
        stone_pos = self.players[self.current_player].stones[self.current_color]
        move_length = abs(target_pos[0] - stone_pos[0])
        sumo_level = self.players[self.current_player].sumo_levels[self.current_color]
        sumo_strength = Board.SUMO_STATS[sumo_level]['power']

        if sumo_level > 0 and move_length == 1 and stone_pos[1] == target_pos[1]:  # sumo style move
            forward_step = 1
            while forward_step <= sumo_strength + 1:
                push_pos = (stone_pos[0] + self.__direction() * forward_step, stone_pos[1])
                if not self.is_in_bounds(push_pos):
                    raise GameException('Sumo cannot push off the board')
                if not self.__is_occupied(push_pos):
                    break
                if forward_step == sumo_strength + 1:
                    raise GameException('Sumo needs to push onto empty cell')
                if push_pos in self.players[self.current_player].stones:
                    raise GameException('Sumo cannot push own stone')
                forward_step += 1
            print(stone_pos, forward_step)
            self.__sumo_cascade(stone_pos, forward_step)
            target_pos = (stone_pos[0] + self.__direction() * forward_step, stone_pos[1])
            # TODO: Fix this shit
            set_current_color_and_player()
            return

        else:
            self.__check_path_clear(stone_pos, target_pos)
            if move_length > Board.SUMO_STATS[sumo_level]['range']:
                raise GameException('Move exceeds max range')
            self.__move_stone(stone_pos, target_pos)


        self.turn_count += 1  # player 0 made this move
        if target_pos[0] == (BLEN - 1) * self.current_player:
            self.__process_round_winner(self.current_player)
        else:
            set_current_color_and_player()  # now current player is 1
            if not self.get_legal_moves():
                # skip move
                target_pos = self.players[self.current_player].stones[self.current_color]
                set_current_color_and_player()  # now current player is 0
                if not self.get_legal_moves():  # deadlock, causing player 0 loses, player 1 wins
                    self.__process_round_winner(1 - self.current_player)

    def get_legal_moves(self):
        # if game over or color has not been set
        if self.winner is not None or self.current_color is None:
            return []
        sumo_level = self.players[self.current_player].sumo_levels[self.current_color]
        max_range = Board.SUMO_STATS[sumo_level]['range']
        start_pos = self.players[self.current_player].stones[self.current_color]
        legal_moves = []
        for diag_direction in (-1, 0, 1):
            for step in range(1, max_range + 1):
                pos = (start_pos[0] + step * self.__direction(),
                       start_pos[1] + step * diag_direction)
                if not self.is_in_bounds(pos) or self.__is_occupied(pos):
                    break
                legal_moves.append(pos)
        return legal_moves

    def reset(self, from_right):
        if not self.round_over:
            raise GameException('Round must be over to reset board')
        self.players[0].reset_stones(flip_col_order=from_right)
        self.players[1].reset_stones(flip_col_order=not from_right)
        self.current_player = 0
        self.turn_count = 0
        self.winner = None
        self.current_color = None
        self.board = Board.get_start_board()
        self.round_over = False

    def draw(self):
        return draw.draw_board(self)


if __name__ == '__main__':
    pass
