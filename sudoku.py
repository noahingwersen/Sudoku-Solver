import pygame
pygame.init()

WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
GRAY = pygame.Color(100, 100, 100)

class Game:
    # Should be divisible by 9
    WINDOW_SIZE = (450, 450)

    def __init__(self):
        self.window = pygame.display.set_mode(self.WINDOW_SIZE)
        self.window.fill(BLACK)
        self._drawGrid()


    def _drawGrid(self):
        # Draw 8 evenly spaced lines for both x and y
        step = int(self.WINDOW_SIZE[0] / 9)
        for i in range(0 + step, self.WINDOW_SIZE[0], int(self.WINDOW_SIZE[0] / 9)):
            lineWidth = 1
            lineColor = GRAY

            # Every third line is white and a little thicker
            if i % 3 == 0:
                lineWidth = 2
                lineColor = WHITE

            pygame.draw.line(self.window, lineColor, (i, 0), (i, self.WINDOW_SIZE[0]), lineWidth)
            pygame.draw.line(self.window, lineColor, (0, i), (self.WINDOW_SIZE[0], i), lineWidth)
        
        pygame.display.update()

    
    def start(self):
        run = True
        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            pygame.display.update()

        pygame.quit()
        quit()


if __name__ == '__main__':
    sudoku = Game()
    sudoku.start()
        



