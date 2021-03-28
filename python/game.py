import draw


class GameException(Exception):
    pass


BLEN = 8


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

    @staticmethod
    def get_color(pos):
        return Board.BOARD_COLORS[pos[0]][pos[1]]

    @staticmethod
    def get_player_name(player):
        return ('White', 'Black')[player]

    @staticmethod
    def is_in_bounds(pos):
        return all(0 <= coord < BLEN for coord in pos)

    def __init__(self):
        self.turn_count = 0
        self.current_player = 0
        self.winner = None
        self.current_color = None
        self.fst_stones = [(BLEN - 1, i) for i in range(BLEN)]
        self.snd_stones = list(reversed([(0, i) for i in range(BLEN)]))
        self.stones = (self.fst_stones, self.snd_stones)
        self.board = [[False] * BLEN for i in range(BLEN - 2)]
        self.board.insert(0, [True] * BLEN)
        self.board.append([True] * BLEN)

    def direction(self):
        return (-1, 1)[self.current_player]

    def is_occupied(self, pos):
        return self.board[pos[0]][pos[1]]

    def occupy(self, pos):
        self.board[pos[0]][pos[1]] = True

    def unoccupy(self, pos):
        self.board[pos[0]][pos[1]] = False

    def stone_order(self, player, col_direction):
        col_index = 0 if col_direction == "r" else 1

        pos_list = ([(BLEN - 1, i) for i in range(BLEN)], list(reversed([(0, i) for i in range(BLEN)])))[player]

        if col_index == 0:
            pos_list.reverse()

        if player == 0:
            col_index = 1 - col_index

        def get_value(color):
            pos = self.stones[player][color]

            row_value = (BLEN - pos[0], pos[0])[player]
            col_value = (pos[1], BLEN - pos[1])[col_index]

            return row_value * BLEN + col_value

        # index : position, value : color
        stone_order = sorted(list(range(BLEN)), key=get_value)

        pos_order = [0] * BLEN

        for i in range(BLEN):
            pos_order[stone_order[i]] = i
        # index : color, value : position

        return [pos_list[i] for i in pos_order]

    def check_move(self, start_pos, target_pos):
        assert self.is_occupied(start_pos), 'inconsistent state'
        if self.is_occupied(target_pos):
            raise GameException('No moving onto stone')
        if self.direction() * (target_pos[0] - start_pos[0]) <= 0:
            raise GameException('Incorrect forward movement')
        row_path = range(start_pos[0] + self.direction(), target_pos[0], self.direction())
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

    def set_color(self, color):
        if self.turn_count > 0:
            raise GameException('Can only set color on first turn')
        self.current_color = color

    def move_stone(self, target_pos):
        if self.current_color is None:
            raise GameException('Must set a color first')
        stone_pos = self.stones[self.current_player][self.current_color]
        self.check_move(stone_pos, target_pos)
        self.unoccupy(stone_pos)
        self.occupy(target_pos)
        self.stones[self.current_player][self.current_color] = target_pos
        self.current_color = Board.get_color(target_pos)
        self.turn_count += 1
        if target_pos[0] == (BLEN - 1) * self.current_player:
            self.winner = self.current_player
        else:
            self.current_player = 1 - self.current_player
            if not self.get_legal_moves():
                # skip move
                pos = self.stones[self.current_player][self.current_color]
                self.current_color = Board.get_color(pos)
                self.current_player = 1 - self.current_player

    def get_legal_moves(self):
        # if game over or color has not been set
        if self.winner is not None or self.current_color is None:
            return []
        stone_pos = self.stones[self.current_player][self.current_color]
        legal_moves = []
        current_pos = stone_pos
        for diag_direction in (-1, 0, 1):
            while True:
                current_pos = (current_pos[0] + self.direction(),
                               current_pos[1] + diag_direction)
                if self.is_in_bounds(current_pos) and not self.is_occupied(current_pos):
                    legal_moves.append(current_pos)
                else:
                    current_pos = stone_pos
                    break
        return legal_moves

    def draw(self):
        return draw.draw_board(self)


if __name__ == '__main__':
    pass
