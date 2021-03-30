import pygame
import game
from draw import BOARD_PIXELS, CELL_PIXELS
import test

DIALOGUE_DIM = (400, 200)
TEXT_PADDING = 40


def run():
    def update():
        img = pygame.image.frombuffer(board.draw().tobytes(), (BOARD_PIXELS, ) * 2, 'RGB')
        window.blit(img, (0, 0))
        pygame.display.update()

    def render_fill_text():
        choose_side_text = small_font.render('Fill from', True, (0,) * 3)
        dialogue_box = pygame.draw.rect(window, (255, 255, 255), rect_pos + DIALOGUE_DIM)
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

    pygame.init()
    big_font = pygame.font.SysFont('Arial', 100, True)
    small_font = pygame.font.SysFont('Arial', 30, True)
    pygame.display.set_caption('Kamisado')
    window = pygame.display.set_mode((BOARD_PIXELS, ) * 2)
    rect_pos = (BOARD_PIXELS // 2 - DIALOGUE_DIM[0] / 2, BOARD_PIXELS // 1.3 - DIALOGUE_DIM[1] / 2)
    board = game.Board()
    #---- board setup
    def helper_recalculate_board(board):
        for x in range(game.BLEN):
            for y in range(game.BLEN):
                board.board[x][y] = (x, y) in board.players[0].stones or (x, y) in board.players[1].stones
    board.players[0].stones = [(3, 4), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    board.players[1].stones = [(2, 4), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]

    board.players[0].sumo_levels = [1, 0, 0, 0, 0, 0, 0, 0]
    board.set_color(0)

    helper_recalculate_board(board)

    #----
    update()
    while True:
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            pygame.quit()
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos[1] // CELL_PIXELS, event.pos[0] // CELL_PIXELS
            if not board.round_over:
                if board.current_color is None:
                    if pos[0] == 7:
                        board.set_color(board._Board__get_stone_color(pos))
                        update()
                else:
                    try:
                        board.perform_move(pos)
                    except game.GameException:
                        continue
                    update()
                    if board.round_over:
                        if board.winner is not None:
                            break
                        render_fill_text()
            else:
                if (rect_pos[0] < event.pos[0] < rect_pos[0] + DIALOGUE_DIM[0]) and (rect_pos[1] < event.pos[1] < rect_pos[1] + DIALOGUE_DIM[1]):
                    # Click inside box
                    board.reset(from_right=event.pos[0] > rect_pos[0] + DIALOGUE_DIM[0] // 2)
                    update()

    winner_text = big_font.render(f'{board.players[board.winner].name} has won', True, (200,) * 3)
    window.blit(winner_text, (BOARD_PIXELS / 2 - winner_text.get_width() // 2,
                              BOARD_PIXELS / 2 - winner_text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(10 * 1000)
    pygame.quit()


if __name__ == '__main__':
    run()
