from itertools import product
import math
from PIL import Image, ImageDraw
import game


CELL_PIXELS = 100
PIECE_RATIO = .8
COLOR_RATIO = .4
SHADOW_RATIO = .05

BOARD_PIXELS = CELL_PIXELS * 8
COLOR_BOUNDING = int(CELL_PIXELS / 2 * (1 - COLOR_RATIO))
PIECE_BOUNDING = int(CELL_PIXELS / 2 * (1 - PIECE_RATIO))
SHADOW_PIXELS = int(SHADOW_RATIO * CELL_PIXELS)

SUMO_SPIKE_SIZE = 7
SUMO_SPIKE_GROUP_COUNT = 4
SUMO_SPIKE_OFFSET = 18  # in degrees

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
    def bounding_box(offset, bounding):
        coords = (pos[1] * CELL_PIXELS, pos[0] * CELL_PIXELS)
        return [tuple(v + offset + bounding for v in coords),
                tuple(v + offset - bounding + CELL_PIXELS for v in coords)]

    def bounding_circle():
        circle_radius = (CELL_PIXELS - PIECE_BOUNDING - COLOR_BOUNDING) / 2
        crossing_cords = (pos[1] * CELL_PIXELS - math.sin(rotation) * circle_radius,
                          pos[0] * CELL_PIXELS - math.cos(rotation) * circle_radius)
        center_coords = tuple(v + CELL_PIXELS / 2 - SHADOW_PIXELS for v in crossing_cords)
        return [center_coords, SUMO_SPIKE_SIZE]

    img = Image.new('RGB', (BOARD_PIXELS, ) * 2)
    draw = ImageDraw.Draw(img)
    for pos in product(range(8), repeat=2):
        draw.rectangle(bounding_box(0, 0), fill=COLORS[board.get_board_color(pos)])
    for player in (0, 1):
        stones = board.players[player].stones
        for color, pos in enumerate(stones):
            draw.ellipse(bounding_box(0, PIECE_BOUNDING), fill=SHADOW_COLORS[player])
            draw.ellipse(bounding_box(-SHADOW_PIXELS, PIECE_BOUNDING), fill=PLAYER_COLORS[player])
            draw.ellipse(bounding_box(-SHADOW_PIXELS, COLOR_BOUNDING), fill=COLORS[color])
            sumo_level = board.players[player].sumo_levels[color]
            for group, spike in product(range(SUMO_SPIKE_GROUP_COUNT), range(sumo_level)):
                group_center = 2 * math.pi * group / SUMO_SPIKE_GROUP_COUNT
                starting_offset = (sumo_level - 1) * math.radians(SUMO_SPIKE_OFFSET) / 2
                spike_offset = spike * math.radians(SUMO_SPIKE_OFFSET)
                rotation = group_center - starting_offset + spike_offset
                draw.regular_polygon(bounding_circle(), 3, rotation=math.degrees(rotation),
                                     fill=PLAYER_COLORS[1-player])
    for pos in board.get_legal_moves():
        player_rgb = {
            'White': (255, 255, 255),
            'Black': (0, 0, 0)
        }[board.players[board.current_player].name]
        draw.ellipse(bounding_box(0, PIECE_BOUNDING), outline=player_rgb, width=5)
    del draw
    return img


if __name__ == '__main__':
    my_board = game.Board()
    my_board.set_color(0)
    my_board.perform_move((5, 0))
    my_board.perform_move((4, 5))
    my_board.perform_move((5, 6))
    my_board.perform_move((4, 3))
    my_board.sumo_stages = ((0, 0, 0, 0, 2, 0, 1, 0), [0] * 7 + [3])
    my_board.draw().show()
