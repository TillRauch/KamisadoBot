from PIL import Image, ImageDraw
import game


BOARD_PIXELS = 800
PIECE_RATIO = 0.9
COLOR_RATIO = 0.35
CELL_PIXELS = BOARD_PIXELS / 8
BOUNDING_PIXELS = CELL_PIXELS * (1 - PIECE_RATIO)
COLOR_PIXELS = BOUNDING_PIXELS * (1 / COLOR_RATIO)
SHADOW_PIXELS = 5

PLAYER_COLORS = [(255, 255, 255, 255), (0, 0, 0, 255)]
SHADOW_COLORS = [(80, 80, 80, 255), (120, 120, 120, 255)]
COLORS = [
    (87, 37, 0, 255),  # Braun
    (0, 162, 95, 255),  # Grün
    (240, 60, 70, 255),  # Rot
    (255, 222, 0, 255),  # Gelb
    (239, 128, 179, 255),  # Pink
    (124, 66, 153, 255),  # Lila
    (0, 120, 200, 255),  # Blau
    (245, 132, 40, 255)  # Orange
]


def draw_board(board):
    def tuple_add(tup, constant):
        return tuple(v + constant for v in tup)

    def draw_ellipse(constant_offset, variable_offset, fill_color, custom_kwargs=None):
        if custom_kwargs is None:
            custom_kwargs = {}
        coords = (pos[1] * CELL_PIXELS, pos[0] * CELL_PIXELS)
        bounding_box = [tuple_add(coords, constant_offset + variable_offset),
                        tuple_add(coords, constant_offset - variable_offset + CELL_PIXELS)]
        draw.ellipse(bounding_box, fill=fill_color, **custom_kwargs)

    def draw_stone(player):
        draw_ellipse(0, BOUNDING_PIXELS, SHADOW_COLORS[player])
        draw_ellipse(-SHADOW_PIXELS, BOUNDING_PIXELS, PLAYER_COLORS[player])
        draw_ellipse(-SHADOW_PIXELS, COLOR_PIXELS, COLORS[color])
    img = Image.new('RGBA', (BOARD_PIXELS, BOARD_PIXELS))
    draw = ImageDraw.Draw(img)
    for row in range(8):
        for col in range(8):
            draw.rectangle([(row * CELL_PIXELS, col * CELL_PIXELS),
                            ((row + 1) * CELL_PIXELS, (col + 1) * CELL_PIXELS)],
                           fill=COLORS[board.BOARD_COLORS[col][row]], width=0)
    for color, pos in enumerate(board.fst_stones):
        draw_stone(0)
    for color, pos in enumerate(board.snd_stones):
        draw_stone(1)
    for pos in board.get_legal_moves():
        kwargs = {
            'outline': (255, 255, 255, 255),
            'width': 5
        }
        draw_ellipse(0, BOUNDING_PIXELS, None, custom_kwargs=kwargs)
    del draw
    return img


if __name__ == '__main__':
    my_board = game.Board()
    my_board.move_stone((5, 0), 0)
    my_board.move_stone((4, 5))
    my_board.move_stone((5, 6))
    my_board.move_stone((4, 3))
    draw_board(my_board).show()
