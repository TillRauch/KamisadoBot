import pygame
import game
from draw import BOARD_PIXELS, CELL_PIXELS


def run():
    def draw_board():
        image = pygame.image.frombuffer(board.draw().tobytes(), (BOARD_PIXELS, ) * 2, 'RGB')
        window.blit(image, (0, 0))
        pygame.display.update()

    board = game.Board()
    # board.set_color(3)
    # board.move_stone((3, 3))
    # board.move_stone((4, 0))
    pygame.init()
    window = pygame.display.set_mode((BOARD_PIXELS, ) * 2)
    pygame.display.set_caption('Kamisado')
    draw_board()
    while board.winner is None:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[1] // CELL_PIXELS, event.pos[0] // CELL_PIXELS)
            if board.current_color is None:
                if pos[0] == 7:
                    board.set_color(pos[1])
                    draw_board()
            if pos in board.get_legal_moves():
                board.move_stone(pos)
                draw_board()
    font = pygame.font.SysFont('Arial', 100)
    text = font.render(f'{board.get_player_name(board.winner)} has won', True, (200, ) * 3)
    window.blit(text, (BOARD_PIXELS / 2 - text.get_width() // 2,
                       BOARD_PIXELS / 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2 * 1000)
    pygame.quit()


if __name__ == '__main__':
    run()
