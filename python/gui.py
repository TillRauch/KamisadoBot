import pygame
import game


def run():
    def draw_board():
        image = pygame.image.frombuffer(board.draw().tobytes(), (800, 800), 'RGB')
        window.blit(image, (0, 0))
        pygame.display.update()
    board = game.Board()
    # board.set_color(3)
    # board.move_stone((3, 3))
    # board.move_stone((4, 0))
    pygame.init()
    window = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Kamisado')
    draw_board()
    while board.winner is None:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos[1] // 100, event.pos[0] // 100
            if board.current_color is None:
                if pos[0] == 7:
                    board.set_color(pos[1])
                    draw_board()
            if pos in board.get_legal_moves():
                board.move_stone(pos)
                draw_board()
    winner_color = ('White', 'Black')[board.winner]
    font = pygame.font.SysFont('Arial', 100)
    text = font.render(f'{winner_color} has won', True, (200, ) * 3)
    window.blit(text, (400 - text.get_width() // 2, 400 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2 * 1000)
    pygame.quit()


if __name__ == '__main__':
    run()
