from itertools import product
import math
from PIL import Image, ImageDraw
import game
from numpy import linspace


CELL_PIXELS = 100
PIECE_RATIO = .8
COLOR_RATIO = .4
SHADOW_RATIO = .05

BOARD_PIXELS = CELL_PIXELS * 8
COLOR_BOUNDING = int(CELL_PIXELS / 2 * (1 - COLOR_RATIO))
PIECE_BOUNDING = int(CELL_PIXELS / 2 * (1 - PIECE_RATIO))
SHADOW_PIXELS = int(SHADOW_RATIO * CELL_PIXELS)

SPIKE_GROUPS = 4
SPIKE_SIZE = 7
SPIKE_OFFSET = 18  # in degrees


player_colors = {
    'White': {
        'stone': (255, ) * 3,
        'shadow': (80, ) * 3,
        'complement': (0, ) * 3
    },
    'Black': {
        'stone': (0, ) * 3,
        'shadow': (120, ) * 3,
        'complement': (255, ) * 3
    }
}


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
    def bounding_box(offset, bounding):
        coords = (pos[1] * CELL_PIXELS, pos[0] * CELL_PIXELS)
        return [tuple(v + offset + bounding for v in coords),
                tuple(v + offset - bounding + CELL_PIXELS for v in coords)]

    def bounding_circle(rotation):
        circle_radius = (CELL_PIXELS - PIECE_BOUNDING - COLOR_BOUNDING) / 2
        cell_center = bounding_box(CELL_PIXELS / 2 - SHADOW_PIXELS, 0)[0]
        triangle_coords = (cell_center[0] - math.sin(rotation) * circle_radius,
                           cell_center[1] - math.cos(rotation) * circle_radius)
        return [triangle_coords, SPIKE_SIZE]

    def draw_spikes():
        sumo_level = player.sumo_levels[color]
        max_spike_offset = (sumo_level - 1) * math.radians(SPIKE_OFFSET) / 2
        for base_rotation in linspace(0, 2 * math.pi, SPIKE_GROUPS, endpoint=False):
            for spike_offset in linspace(-max_spike_offset, max_spike_offset, sumo_level):
                rotation = base_rotation + spike_offset
                draw.regular_polygon(bounding_circle(rotation), 3, rotation=math.degrees(rotation),
                                     fill=player_colors[player.name]['complement'])

    img = Image.new('RGB', (BOARD_PIXELS, ) * 2)
    draw = ImageDraw.Draw(img)
    for pos in product(range(8), repeat=2):
        draw.rectangle(bounding_box(0, 0), fill=COLORS[board.get_board_color(pos)])
    for player in (board.fst_player, board.snd_player):
        pcolors = player_colors[player.name]
        for color, pos in enumerate(player.stones):
            draw.ellipse(bounding_box(0, PIECE_BOUNDING), fill=pcolors['shadow'])
            draw.ellipse(bounding_box(-SHADOW_PIXELS, PIECE_BOUNDING), fill=pcolors['stone'])
            draw.ellipse(bounding_box(-SHADOW_PIXELS, COLOR_BOUNDING), fill=COLORS[color])
            draw_spikes()
    for pos in board.get_legal_moves():
        indicator_color = player_colors[board.current_player.name]['stone']
        draw.ellipse(bounding_box(0, PIECE_BOUNDING), outline=indicator_color, width=5)
    del draw
    return img


if __name__ == '__main__':
    my_board = game.Board()
    my_board.set_color(0)
    my_board.perform_move((5, 0))
    my_board.perform_move((4, 5))
    my_board.perform_move((5, 6))
    my_board.perform_move((4, 3))
    my_board.fst_player.sumo_levels = [0, 0, 0, 0, 2, 0, 1, 0]
    my_board.snd_player.sumo_levels = [0] * 7 + [3]
    my_board.draw().show()
