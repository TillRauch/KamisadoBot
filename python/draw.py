from itertools import product
from PIL import Image, ImageDraw
import game


CELL_PIXELS = 100
PIECE_RATIO = .8
COLOR_RATIO = .4
SHADOW_RATIO = .05

BOARD_PIXELS = CELL_PIXELS * 8
COLOR_BOUNDING = int(CELL_PIXELS / 2 * (1 - COLOR_RATIO))
PIECE_BOUNDING = int(CELL_PIXELS / 2 * (1 - PIECE_RATIO))
SHADOW_PIXELS = CELL_PIXELS * SHADOW_RATIO

PLAYER_COLORS = [(255, 255, 255), (0, 0, 0)]
SHADOW_COLORS = [(80, 80, 80), (120, 120, 120)]
COLORS = [
    (87, 37, 0),  # Braun
    (0, 162, 95),  # Grün
    (240, 60, 70),  # Rot
    (255, 222, 0),  # Gelb
    (239, 128, 179),  # Pink
    (124, 66, 153),  # Lila
    (0, 120, 200),  # Blau
    (245, 132, 40)  # Orange
]


def draw_board(board):
    def tuple_add(tup, constant):
        return tuple(v + constant for v in tup)

    def bounding_box(offset, bounding):
        coords = (pos[1] * CELL_PIXELS, pos[0] * CELL_PIXELS)
        return [tuple_add(coords, offset + bounding),
                tuple_add(coords, offset - bounding + CELL_PIXELS)]

    img = Image.new('RGB', (BOARD_PIXELS, BOARD_PIXELS))
    draw = ImageDraw.Draw(img)
    for pos in product(range(8), repeat=2):
        draw.rectangle(bounding_box(0, 0), fill=COLORS[board.get_color(pos)], width=0)
    for player, player_stones in enumerate(board.stones):
        for color, pos in enumerate(player_stones):
            draw.ellipse(bounding_box(0, PIECE_BOUNDING), fill=SHADOW_COLORS[player])
            draw.ellipse(bounding_box(-SHADOW_PIXELS, PIECE_BOUNDING), fill=PLAYER_COLORS[player])
            draw.ellipse(bounding_box(-SHADOW_PIXELS, COLOR_BOUNDING), fill=COLORS[color])
    for pos in board.get_legal_moves():
        draw.ellipse(bounding_box(0, PIECE_BOUNDING), fill=None, outline=(255,) * 3, width=5)
    del draw
    return img


if __name__ == '__main__':
    my_board = game.Board()
    my_board.set_color(0)
    my_board.move_stone((5, 0))
    my_board.move_stone((4, 5))
    my_board.move_stone((5, 6))
    my_board.move_stone((4, 3))
    my_board.draw().show()
