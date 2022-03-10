import random
import pickle
import pygame
from enum import IntEnum
from sudoku import Game, Tile

GREEN = pygame.Color(0, 255, 0)

class SolveType(IntEnum):
    eHeuristic = 0
    eLinearProgram = 1

class SudokuSolver():
    VALUE_RANGE = range(1, 10)

    def solve(self, grid: list[list[int]], method):
        self.grid = grid
        self.game = Game(self.grid)

        if method == SolveType.eHeuristic:
            self._solve_heuristic()
        elif method == SolveType.eLinearProgram:
            pass
    
    def _solve_heuristic(self):
        solved = False
        while not solved:
            self._assignPossibleValues()
            self._updateGrid()
            self._drawGrid()

            solved = True
            for row in self.grid:
                for value in row:
                    if value == 0:
                        pass
                        solved = False


    def _updateGrid(self):
        for i, row in enumerate(self.grid):
            for j, value in enumerate(row):
                if value not in self.possibleValues[i][j] and len(self.possibleValues[i][j]) == 1:
                    self.grid[i][j] = self.possibleValues[i][j][0]

    def _drawGrid(self):
        r = random.randrange(10, 255)
        g = random.randrange(10, 255)
        b = random.randrange(10, 255)
        for i, tileRow in enumerate(self.game.tiles):
            for j, tile in enumerate(tileRow):
                if tile.value not in self.possibleValues[i][j] and len(self.possibleValues[i][j]) == 1:
                    tile.value = self.possibleValues[i][j][0]
                    tile.draw(tile.position, pygame.Color(r, g, b))

    def showGrid(self):
        self.game.start()


    def _assignPossibleValues(self):
        rowValues = []
        colValues = []
        boxValues = []
        for i in range(0, 9):
            rowValues.append(self._checkRow(i))
            colValues.append(self._checkColumn(i))
            boxValues.append(self._checkBox(i))

        # 9x9 array of empty lists
        self.possibleValues =[ [ [] for _ in range(9)] for _ in range(9)]
        for i, row in enumerate(self.grid):
            for j, item in enumerate(row):
                if item == 0:
                    # Add values that are shared by row, column and box
                    boxIndex = (int(i / 3) * 3) + int(j / 3)
                    overlappingValues = list(set(rowValues[i]).intersection(colValues[j], boxValues[boxIndex]))
                    self.possibleValues[i][j].extend(overlappingValues.copy())
                else:
                    # Add known value only
                    self.possibleValues[i][j].append(item)
        

    def _checkRow(self, index: int) -> list[int]:
        '''
        Find values that don't exist in given row
        '''
        values = [v for v in self.grid[index] if v != 0]
        return self._getPossibleValues(values)

    def _checkColumn(self, index: int) -> list[int]:
        '''
        Find values that don't exist in given column
        '''
        values = [row[index] for row in self.grid if row[index] != 0]
        return self._getPossibleValues(values)

    def _checkBox(self, index: int)-> list[int]:
        '''
        Find possible values for each tile in a 3x3

         0 | 1 | 2 
        ---|---|---
         3 | 4 | 5 
        ---|---|---
         6 | 7 | 8

        '''

        xStart = int(index / 3) * 3
        yStart = (index % 3) * 3

        xRange = range(xStart, xStart + 3)
        yRange = range(yStart, yStart + 3)

        values  = []
        for x in xRange:
            for y in yRange:
                if self.grid[x][y] != 0:
                    values.append(self.grid[x][y])

        if index == 6 or index == 7 or index == 8:
            test = 'break'
        return self._getPossibleValues(values)

    def _getPossibleValues(self, values: list[int]) -> list[int]:
        '''
        Helper function to return inverse of listed values
        '''
        return [i for i in self.VALUE_RANGE if i not in values]

def main():
    with open('grid2.pickle', 'rb') as f:
        grid = pickle.load(f)
    
    solver = SudokuSolver()
    solver.solve(grid)
    solver.showGrid()


if __name__ == '__main__':
    main()