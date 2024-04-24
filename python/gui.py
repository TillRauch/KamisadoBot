from itertools import product

import pygame
import game
from draw import BOARD_PIXELS, CELL_PIXELS
import engine as e

BOX_DIM = 400, 200
DEBUG_FIELD_WIDTH = 400
DEBUG_FONT_SIZE = 20
TEXT_PADDING = 40
PLAY_WITH_BOT = False
BOT_CALCULATING_TIME = 1000



def __make_occupy_consistent(board):
    for row, col in product(range(game.BLEN), repeat=2):
        occupied = any((row, col) in player.stones for player in (board.fst_player, board.snd_player))
        board.occupied[row][col] = occupied


def run():
    def update_image():
        img = pygame.image.frombuffer(board.draw().tobytes(), (BOARD_PIXELS, ) * 2, 'RGB')
        window.blit(img, (0, 0))
        pygame.display.update()

    def render_debug_text(player, text):
        height_pos = 0 if player == board.snd_player else BOARD_PIXELS - DEBUG_FONT_SIZE * len(text)
        pygame.draw.rect(window, (255, 255, 255), ((0, 0), (BOARD_PIXELS + DEBUG_FIELD_WIDTH, BOARD_PIXELS)))
        for index, text_bite in enumerate(text):
            text_obj = debug_font.render(text_bite, True, (0, 0, 0))
            window.blit(text_obj, (BOARD_PIXELS + 10, height_pos + index * DEBUG_FONT_SIZE))
        pygame.display.update()

    def render_fill_menu():
        text = small_font.render('Fill from', True, (0, 0, 0))
        box = pygame.draw.rect(window, (255, 255, 255), box_top_left + BOX_DIM)
        window.blit(text, (box.centerx - text.get_width() // 2,
                           box.centery - text.get_height() // 2 - box.height // 3))
        left_text = small_font.render('Left', True, (0, 0, 0))
        right_text = small_font.render('Right', True, (0, 0, 0))
        left_text_coords = box.left + TEXT_PADDING, box.centery - left_text.get_height() // 2
        right_text_coords = (box.right - right_text.get_width() - TEXT_PADDING,
                             box.centery - right_text.get_height() // 2)
        window.blit(left_text, left_text_coords)
        window.blit(right_text, right_text_coords)
        pygame.display.update()

    def handle_round_end():
        if board.winner is not None:
            winner_text = big_font.render(f'{board.winner.name} has won', True, (200,) * 3)
            window.blit(winner_text,
                        (BOARD_PIXELS / 2 - winner_text.get_width() // 2,
                         BOARD_PIXELS / 2 - winner_text.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(5 * 1000)
        else:
            render_fill_menu()

    def handle_round():
        if board.current_color is None:
            if pos[0] == 7:
                board.set_color(board.current_player.stones.index(pos))
                update_image()
        else:
            try:
                board.perform_move(pos)
            except game.GameException:
                pass
            if board.round_over:
                handle_round_end()
            if PLAY_WITH_BOT:
                engine = e.Engine()
                move = engine.get_move(board, BOT_CALCULATING_TIME)
                board.perform_move(move[0])
                render_debug_text(BOT_PLAYER, move[1])
            update_image()

    pygame.init()
    big_font = pygame.font.SysFont('Arial', 100, True)
    small_font = pygame.font.SysFont('Arial', 30, True)
    debug_font = pygame.font.SysFont('courier', DEBUG_FONT_SIZE, True)
    pygame.display.set_caption('Kamisado')
    window = pygame.display.set_mode((BOARD_PIXELS + DEBUG_FIELD_WIDTH, BOARD_PIXELS))
    box_top_left = BOARD_PIXELS // 2 - BOX_DIM[0] / 2, BOARD_PIXELS // 1.3 - BOX_DIM[1] / 2

    board = game.Board()
    BOT_PLAYER = board.snd_player

    update_image()
    event = pygame.event.Event(0)
    while event.type != pygame.QUIT and board.winner is None:
        event = pygame.event.wait()
        if event.type != pygame.MOUSEBUTTONDOWN:
            continue
        pos = event.pos[1] // CELL_PIXELS, event.pos[0] // CELL_PIXELS
        if not board.round_over:
            handle_round()
        elif all(box_top_left[i] < event.pos[i] < box_top_left[i] + BOX_DIM[i] for i in (0, 1)):
            # Click inside box
            board.reset(from_right=event.pos[0] > box_top_left[0] + BOX_DIM[0] // 2)
            update_image()
    pygame.quit()


if __name__ == '__main__':
    run()
