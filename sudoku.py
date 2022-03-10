import pickle
from turtle import pos
import pygame
pygame.init()

WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
GRAY = pygame.Color(100, 100, 100)

class Game:
    # Should be divisible by 9
    WINDOW_SIZE = (450, 450)
    STEP = int(WINDOW_SIZE[0] / 9)
    TEXT_BUFFER = 10

    def __init__(self, grid):
        self.window = pygame.display.set_mode(self.WINDOW_SIZE)
        self.window.fill(BLACK)
        self.grid = grid
        self._drawLines()
        self._drawNumbers(grid)


    def _drawLines(self):
        # Draw 8 evenly spaced lines for both x and y
        for i in range(0 + self.STEP, self.WINDOW_SIZE[0], self.STEP):
            lineWidth = 1
            lineColor = GRAY

            # Every third line is white and a little thicker
            if i % 3 == 0:
                lineWidth = 2
                lineColor = WHITE

            pygame.draw.line(self.window, lineColor, (i, 0), (i, self.WINDOW_SIZE[0]), lineWidth)
            pygame.draw.line(self.window, lineColor, (0, i), (self.WINDOW_SIZE[0], i), lineWidth)
        
        pygame.display.update()

    def _drawNumbers(self, array):
        self.tiles = []
        for i, row in enumerate(array):
            tileRow = []
            for j, value in enumerate(row):
                tile = Tile(self.window, value)
                tile.draw((j * self.STEP + self.TEXT_BUFFER, i * self.STEP))
                tileRow.append(tile)

            self.tiles.append(tileRow)
    
    def setTitle(self, title: str):
        pygame.display.set_caption(title)
    
    def start(self):
        run = True
        while run:

            for event in pygame.event.get():
                # Quit the game if the user hits 'x'
                if event.type == pygame.QUIT:
                    run = False
            
            pygame.display.update()

        pygame.quit()
        quit()

class Tile():
    '''
    Represents a number for each grid spot
    '''
    FONT = pygame.font.SysFont('arial', 45)

    def __init__(self, window: pygame.Surface, value: int):
        self.window = window
        self.value = value
    
    def draw(self, position: tuple, color=WHITE):
        self.position = position
        if self.value != 0:
            text = self.FONT.render(str(self.value), True, color)
            self.window.blit(text, self.position)



if __name__ == '__main__':
    with open('grid1.pickle', 'rb') as f:
        grid1 = pickle.load(f)

    sudoku = Game(grid1)
    sudoku.start()
        



