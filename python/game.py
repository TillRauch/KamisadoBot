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

    def __str__(self):
        return self.name

    def get_points(self):
        return sum(Board.SUMO_STATS['points'][lvl] for lvl in self.sumo_levels)

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

    SUMO_STATS = {
        'range': [BLEN, 5, 3, 1, 0],
        'power': list(range(5)),
        'points': [0, 1, 3, 7, 15]
    }

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
        self.occupied = Board.get_start_board()
        self.fst_player = Player('White', [(BLEN - 1, i) for i in range(BLEN)])
        self.snd_player = Player('Black', [(0, i) for i in reversed(range(BLEN))])
        self.current_player = self.fst_player

    def __other_player(self):
        return self.snd_player if self.current_player == self.fst_player else self.fst_player

    def __direction(self):
        return 1 if self.current_player.start_row == 0 else -1

    def __next_pos(self, pos):
        return pos[0] + self.__direction(), pos[1]

    def __previous_pos(self, pos):
        return pos[0] - self.__direction(), pos[1]

    def __is_occupied(self, pos):
        return self.occupied[pos[0]][pos[1]]

    def __occupy(self, pos):
        self.occupied[pos[0]][pos[1]] = True

    def __unoccupy(self, pos):
        self.occupied[pos[0]][pos[1]] = False

    def __move_stone(self, owner, color, target_pos):
        self.__unoccupy(owner.stones[color])
        owner.stones[color] = target_pos
        self.__occupy(target_pos)

    def __check_path(self, start_pos, target_pos):
        assert self.__is_occupied(start_pos), 'inconsistent state'
        if self.__is_occupied(target_pos):
            raise GameException('Cannot move onto stone')
        if self.__direction() * (target_pos[0] - start_pos[0]) <= 0:
            raise GameException('Can only move forward')
        row_path = range(start_pos[0] + self.__direction(), target_pos[0], self.__direction())
        # if line straight
        if start_pos[1] == target_pos[1]:
            col_path = [start_pos[1]] * len(row_path)
        else:
            if abs(start_pos[1] - target_pos[1]) != abs(start_pos[0] - target_pos[0]):
                raise GameException('Can only move straight or diagonally')
            diag_direction = 1 if target_pos[1] > start_pos[1] else -1
            col_path = range(start_pos[1] + diag_direction, target_pos[1], diag_direction)
        if any(self.occupied[row][col] for row, col in zip(row_path, col_path)):
            raise GameException('Cannot move through pieces')

    def __check_sumo(self, target_pos):
        sumo_level = self.current_player.sumo_levels[self.current_color]
        sumo_power = Board.SUMO_STATS['power'][sumo_level]
        push_pos = target_pos
        while self.__is_occupied(push_pos):
            if push_pos in self.current_player.stones:
                raise GameException('Sumo cannot push own stone')
            if abs(push_pos[0] - target_pos[0]) >= sumo_power:
                raise GameException('Sumo is pushing too many stones')
            other = self.__other_player()
            if other.sumo_levels[other.stones.index(push_pos)] >= sumo_level:
                raise GameException('Sumo cannot push same strength sumo')
            push_pos = self.__next_pos(push_pos)
            if not self.is_in_bounds(push_pos):
                raise GameException('Sumo cannot push off the board')
        return push_pos

    def __sumo_cascade(self, sumo_pos, end_pos):
        def move_sumo(player, pos):
            self.__move_stone(player, player.stones.index(pos), self.__next_pos(pos))
        assert not self.__is_occupied(end_pos)
        stone_pos = self.__previous_pos(end_pos)
        while stone_pos != sumo_pos:
            move_sumo(self.__other_player(), stone_pos)
            stone_pos = self.__previous_pos(stone_pos)
        move_sumo(self.current_player, sumo_pos)

    def __process_round_winner(self, winner):
        self.round_over = True
        winner.sumo_levels[self.current_color] += 1
        if winner.get_points() >= self.winning_points:
            self.winner = winner

    def set_color(self, color):
        if self.turn_count > 0:
            raise GameException('Can only set color on first turn')
        self.current_color = color

    def perform_move(self, target_pos):
        def set_current_color_and_player():
            self.current_color = Board.get_board_color(target_pos)
            self.current_player = self.__other_player()
        if self.current_color is None:
            raise GameException('Must set a color first')
        if not self.is_in_bounds(target_pos):
            raise GameException('Cannot move stone out of bounds')
        sumo_level = self.current_player.sumo_levels[self.current_color]
        stone_pos = self.current_player.stones[self.current_color]
        try:
            self.__check_path(stone_pos, target_pos)
        except GameException as e:
            is_one_step_move = target_pos[0] - stone_pos[0] == self.__direction()
            if sumo_level > 0 and is_one_step_move and stone_pos[1] == target_pos[1]:
                target_pos = self.__check_sumo(target_pos)
                self.__sumo_cascade(stone_pos, target_pos)
            else:
                raise e
        else:
            if abs(target_pos[0] - stone_pos[0]) > Board.SUMO_STATS['range'][sumo_level]:
                raise GameException('Move exceeds max range')
            self.__move_stone(self.current_player, self.current_color, target_pos)
            if target_pos[0] == self.__other_player().start_row:
                self.__process_round_winner(self.current_player)
                self.turn_count += 1
                return
        self.turn_count += 1  # player 0 made this move
        set_current_color_and_player()  # now current player is 1
        if not self.get_legal_moves():  # then skip move
            target_pos = self.current_player.stones[self.current_color]
            set_current_color_and_player()  # now current player is 0
            if not self.get_legal_moves():  # deadlock, causing player 0 loses, player 1 wins
                self.__process_round_winner(self.__other_player())

    def get_legal_moves(self):
        if self.round_over or self.current_color is None:
            return []
        sumo_level = self.current_player.sumo_levels[self.current_color]
        max_range = Board.SUMO_STATS['range'][sumo_level]
        start_pos = self.current_player.stones[self.current_color]
        legal_moves = []
        for diag_direction in (-1, 0, 1):
            for step in range(1, max_range + 1):
                pos = (start_pos[0] + step * self.__direction(),
                       start_pos[1] + step * diag_direction)
                if not Board.is_in_bounds(pos):
                    break
                if self.__is_occupied(pos):
                    sumo_level = self.current_player.sumo_levels[self.current_color]
                    if sumo_level > 0 and step == 1 and diag_direction == 0:
                        try:
                            self.__check_sumo(pos)
                        except GameException:
                            pass
                        else:
                            legal_moves.append(pos)
                    break
                legal_moves.append(pos)
        return legal_moves

    def reset(self, from_right):
        if not self.round_over:
            raise GameException('Round must be over to reset board')
        self.fst_player.reset_stones(flip_col_order=from_right)
        self.snd_player.reset_stones(flip_col_order=not from_right)
        self.current_player = self.fst_player
        self.turn_count = 0
        self.winner = None
        self.current_color = None
        self.occupied = Board.get_start_board()
        self.round_over = False

    def draw(self):
        return draw.draw_board(self)


if __name__ == '__main__':
    board = Board()
