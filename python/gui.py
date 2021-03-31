from itertools import product

import pygame
import game
from draw import BOARD_PIXELS, CELL_PIXELS

BOX_DIM = 400, 200
TEXT_PADDING = 40


def __make_occupy_consistent(board):
    for row, col in product(range(game.BLEN), repeat=2):
        occupied = any((row, col) in player.stones for player in (board.fst_player, board.snd_player))
        board.occupied[row][col] = occupied


def run():
    def update_image():
        img = pygame.image.frombuffer(board.draw().tobytes(), (BOARD_PIXELS, ) * 2, 'RGB')
        window.blit(img, (0, 0))
        pygame.display.update()

    def render_fill_text():
        choose_side_text = small_font.render('Fill from', True, (0,) * 3)
        dialogue_box = pygame.draw.rect(window, (255, 255, 255), box_top_left + BOX_DIM)
        window.blit(choose_side_text, (dialogue_box.centerx - choose_side_text.get_width() // 2,
                                       dialogue_box.centery - choose_side_text.get_height() // 2 - dialogue_box.height // 3))

        left_text = small_font.render('Left', True, (0,) * 3)
        right_text = small_font.render('Right', True, (0,) * 3)
        window.blit(left_text,
                    (dialogue_box.left + TEXT_PADDING, dialogue_box.centery - left_text.get_height() // 2))
        window.blit(right_text,
                    (dialogue_box.right - right_text.get_width() - TEXT_PADDING,
                     dialogue_box.centery - right_text.get_height() // 2))
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
            render_fill_text()

    def handle_round():
        if board.current_color is None:
            if pos[0] == 7:
                board.set_color(board.current_player.stones.index(pos))
                update_image()
        else:
            print(pos)
            try:
                board.perform_move(pos)
            except game.GameException:
                pass
            update_image()
            if board.round_over:
                handle_round_end()

    pygame.init()
    big_font = pygame.font.SysFont('Arial', 100, True)
    small_font = pygame.font.SysFont('Arial', 30, True)
    pygame.display.set_caption('Kamisado')
    window = pygame.display.set_mode((BOARD_PIXELS, ) * 2)
    box_top_left = BOARD_PIXELS // 2 - BOX_DIM[0] / 2, BOARD_PIXELS // 1.3 - BOX_DIM[1] / 2

    board = game.Board()
    board.fst_player.stones = [(3, 4), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    board.snd_player.stones = [(2, 4), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]
    board.fst_player.sumo_levels = [1, 0, 0, 0, 0, 0, 0, 0]
    board.set_color(0)
    __make_occupy_consistent(board)

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
