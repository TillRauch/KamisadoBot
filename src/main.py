from PIL import Image, ImageDraw
from src import Board

board = Board.Board()
board.setupBoard()

board.moveStone([7, 0], [5, 0], -1)
board.moveStone([0, 1], [4, 5], 1)
board.moveStone([7, 6], [5, 6], -1)
board.moveStone([0, 3], [4, 3], 1)


boardSize = 800
pieceRatio = 0.9
colorRatio = 0.35
cellSize = boardSize / 8
pieceBounding = cellSize * (1 - pieceRatio)
colorBounding = pieceBounding * (1/colorRatio)

shadowOffset = 5

sideColors = {
    -1: (255, 255, 255, 255),
    1: (0, 0, 0, 255)
}

shadowColors = {
    -1: (80, 80, 80, 255),
    1: (120, 120, 120, 255)
}

pieceColor = (255, 0, 0, 255)

colorPalette = {
    0: (87, 37, 0, 255),  # Braun
    1: (0, 162, 95, 255),  # Grün
    2: (240, 60, 70, 255),  # Rot
    3: (255, 222, 0, 255),  # Gelb
    4: (239, 128, 179, 255),  # Pink
    5: (124, 66, 153, 255),  # Lila
    6: (0, 120, 200, 255),  # Blau
    7: (245, 132, 40, 255),  # Orange
}


def setAlpha(color, alpha):
    return (color[0], color[1], color[2], alpha)

img = Image.new('RGBA', (boardSize, boardSize))
draw = ImageDraw.Draw(img)

for x in range(8):
    for y in range(8):
        draw.rectangle([(x*cellSize, y*cellSize), ((x+1)*cellSize, (y+1)*cellSize)], fill=colorPalette[board.boardColors[x][y]], width=0)
        if (board.board[y][x] != None):
            stone = board.board[y][x]
            draw.ellipse([(x*cellSize + pieceBounding, y*cellSize + pieceBounding), ((x+1)*cellSize - pieceBounding, (y+1)*cellSize - pieceBounding)], fill=shadowColors[stone.side])
            draw.ellipse([(x*cellSize + pieceBounding - shadowOffset, y*cellSize + pieceBounding - shadowOffset), ((x+1)*cellSize - pieceBounding - shadowOffset, (y+1)*cellSize - pieceBounding - shadowOffset)], fill=sideColors[stone.side])
            draw.ellipse([(x*cellSize + colorBounding - shadowOffset, y*cellSize + colorBounding - shadowOffset), ((x+1)*cellSize - colorBounding - shadowOffset, (y+1)*cellSize - colorBounding - shadowOffset)], fill=colorPalette[stone.color])

for legalMove in board.getLegalMoves():
    y, x = legalMove
    draw.ellipse([(x*cellSize + pieceBounding, y*cellSize + pieceBounding), ((x+1)*cellSize - pieceBounding, (y+1)*cellSize - pieceBounding)], outline=(255, 255, 255, 255), fill=None, width=5)
del draw
img.save('test_image.png')
