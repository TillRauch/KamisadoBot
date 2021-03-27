from itertools import product


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

    def __init__(self):
        self.turn_count = 0
        self.current_player = 0
        self.current_color = None
        self.fst_stones = [(7, i) for i in range(8)]
        self.snd_stones = [(0, i) for i in range(8)]
        self.snd_stones.reverse()
        self.stones = (self.fst_stones, self.snd_stones)
        self.board = [[False] * 8 for i in range(6)]
        self.board.insert(0, [True] * 8)
        self.board.append([True] * 8)

    def is_in_bounds(self, pos):
        return all(0 <= coord < len(self.board) for coord in pos)

    def direction(self):
        return -1 if self.current_player == 0 else 1

    def is_occupied(self, pos):
        return self.board[pos[0]][pos[1]]

    def occupy(self, pos):
        self.board[pos[0]][pos[1]] = True

    def unoccupy(self, pos):
        self.board[pos[0]][pos[1]] = False

    def check_move(self, start_pos, target_pos):
        assert self.is_occupied(start_pos), 'inconsistent state'
        if self.is_occupied(target_pos):
            raise Exception('No moving onto Stone')
        if self.direction() * (target_pos[0] - start_pos[0]) <= 0:
            raise Exception('Incorrect forward Movement')
        row_path = range(start_pos[0] + self.direction(), target_pos[0], self.direction())
        # if line straight
        if start_pos[1] == target_pos[1]:
            col_path = [start_pos[1]] * len(row_path)
        else:
            if abs(start_pos[1] - target_pos[1]) != abs(start_pos[0] - target_pos[0]):
                raise Exception('Move not along diagonal')
            diag_direction = 1 if target_pos[1] > start_pos[1] else -1
            col_path = range(start_pos[1] + diag_direction, target_pos[1], diag_direction)
        if any(self.board[row][col] for row, col in zip(row_path, col_path)):
            raise Exception('Piece in-between')

    def move_stone(self, target_pos, color=None):
        if color is None:
            color = self.current_color
        else:
            assert self.turn_count == 0  # or color == self.current_color
        stone_pos = self.stones[self.current_player][color]
        self.check_move(stone_pos, target_pos)
        self.unoccupy(stone_pos)
        self.occupy(target_pos)
        self.stones[self.current_player][color] = target_pos
        self.current_player = 1 - self.current_player
        self.current_color = self.BOARD_COLORS[target_pos[0]][target_pos[1]]
        self.turn_count += 1

    def get_legal_moves(self):
        legal_moves = []
        if self.turn_count == 0:
            return [(row, col) for row, col in product(range(1, 7), range(8))]
        stone_pos = self.stones[self.current_player][self.current_color]
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


if __name__ == '__main__':
    pass
