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

    SUMO_ABILITIES = ((BLEN, 0), (5, 1), (3, 2), (1, 3))  # (max_range , power)

    @staticmethod
    def get_board_color(pos):
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
        self.winner_history = []
        self.current_color = None
        self.sumo_stages = ([0] * BLEN, [0] * BLEN)
        self.stones = [[(BLEN - 1, i) for i in range(BLEN)],
                       [(0, i) for i in reversed(range(BLEN))]]
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

    def get_stone_color(self, pos):
        if not self.is_occupied(pos):
            raise GameException('Position is not occupied')

        for player in (0, 1):
            if pos in self.stones[player]:
                return self.stones[player].index(pos)

    def reset_stones(self, from_right=False):
        def flip_stones(flip_row=False, flip_col=False):
            return [(pos[0] * (1, -1)[flip_row],
                     pos[1] * (1, -1)[flip_col]) for pos in self.stones[player]]
        for player in (0, 1):
            stones = flip_stones(flip_row=not bool(player), flip_col=from_right)
            sorted_colors = sorted(range(BLEN), key=stones.__getitem__)
            if from_right:
                sorted_colors.reverse()
            start_row = (BLEN - 1, 0)[player]
            for place, color in enumerate(sorted_colors):
                self.stones[player][color] = start_row, place
            from_right = not from_right

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
        move_length = abs(start_pos[0] - target_pos[0])

        print(move_length)
        print(self.SUMO_ABILITIES[self.sumo_stages[self.current_player][self.get_stone_color(start_pos)]][0])

        if move_length > self.SUMO_ABILITIES[self.sumo_stages[self.current_player][self.get_stone_color(start_pos)]][0]:
            raise GameException('Move exceeds max range')

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
        self.current_color = Board.get_board_color(target_pos)
        self.turn_count += 1
        if target_pos[0] == (BLEN - 1) * self.current_player:
            self.winner = self.current_player
            self.reset_board(self.get_stone_color(target_pos))
        else:
            self.current_player = 1 - self.current_player
            if not self.get_legal_moves():
                # skip move
                pos = self.stones[self.current_player][self.current_color]
                self.current_color = Board.get_board_color(pos)
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
                    # Is this pythonic? Help.
                    try:
                        self.check_move(stone_pos, current_pos)
                        legal_moves.append(current_pos)
                    except:
                        pass
                else:
                    current_pos = stone_pos
                    break
        return legal_moves

    def reset_board(self, winning_stone_color):
        # TODO User Input
        self.reset_stones(from_right=True)
        self.winner_history.append(self.winner)
        self.sumo_stages[self.winner][winning_stone_color] += 1
        self.current_player = 0
        self.turn_count = 0
        self.winner = None
        self.current_color = None
        self.board = [[False] * BLEN for i in range(BLEN - 2)]
        self.board.insert(0, [True] * BLEN)
        self.board.append([True] * BLEN)




    def draw(self):
        return draw.draw_board(self)


if __name__ == '__main__':
    pass
