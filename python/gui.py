import pygame
import game
import draw
board = game.Board()
board.move_stone((6, 0), 0)

pygame.init()
window = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Kamisado")
run = True
image = pygame.image.frombuffer(draw.draw_board(board).tobytes(), (800, 800), "RGBA")

while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_pixels, y_pixels = event.pos
            x_pos = y_pixels // 100
            y_pos = x_pixels // 100

            if (x_pos, y_pos) in board.get_legal_moves():

                board.move_stone((x_pos, y_pos))

                image = pygame.image.frombuffer(draw.draw_board(board).tobytes(), (800, 800), "RGBA")

    window.fill((0, 0, 0))

    window.blit(image, (0, 0))
    pygame.display.update()
pygame.quit()