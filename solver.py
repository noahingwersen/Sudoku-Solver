import random
import pickle
import pygame
import pulp
from sudoku import Game

class SudokuSolver():
    INDEX_RANGE = range(0, 9)
    VALUE_RANGE = range(1, 10)

    def __init__(self, grid):
        self.grid = grid
        self.game = Game(self.grid)

    def showGrid(self, color: pygame.Color):
        self._drawGrid(color)
        self.game.start()
    
    def _drawGrid(self, color: pygame.Color):
        for i, tileRow in enumerate(self.game.tiles):
            for j, tile in enumerate(tileRow):
                if tile.value != self.grid[i][j]:
                    tile.value = self.grid[i][j]
                    tile.draw(tile.position, color)

class HeuristicSolver(SudokuSolver):
    def __init__(self, grid):
        super().__init__(grid)
        self.game.setTitle("Heuristic Solver")
    
    def solve(self):
        solved = False
        while not solved:
            self._assignPossibleValues()
            self._updateGrid()

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
    
    def _assignPossibleValues(self):
        rowValues = []
        colValues = []
        boxValues = []
        for i in self.INDEX_RANGE:
            rowValues.append(self._checkRow(i))
            colValues.append(self._checkColumn(i))
            boxValues.append(self._checkBox(i))

        # 9x9 array of empty lists
        self.possibleValues =[ [ [] for _ in self.INDEX_RANGE] for _ in self.INDEX_RANGE]
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

        return self._getPossibleValues(values)

    def _getPossibleValues(self, values: list[int]) -> list[int]:
        '''
        Helper function to return inverse of listed values
        '''
        return [i for i in self.VALUE_RANGE if i not in values]

class LinearSolver(SudokuSolver):

    def __init__(self, grid):
        super().__init__(grid)
        self.game.setTitle('Linear Solver')
    
    def solve(self):
        self._setupProblem()
        self._defineConstraints()
        self._initializeGrid()
        self.problem.solve()

        self._updateGrid()

    
    def _setupProblem(self):
        self.problem = pulp.LpProblem('SudokuSolver')
        objective = pulp.lpSum(0)
        self.problem.setObjective(objective)

    def _defineConstraints(self):
        rows    = self.INDEX_RANGE
        columns = self.INDEX_RANGE
        boxes   = self.INDEX_RANGE
        values  = self.VALUE_RANGE

        decisionVariables = pulp.LpVariable.dicts(
            "tileValue", 
            (rows, columns, values), 
            cat='Binary'
        )
        self.decisionVariables = decisionVariables

        # Each tile can only have one value
        for row in self.INDEX_RANGE:
            for col in self.INDEX_RANGE:
                self.problem.addConstraint(
                    pulp.LpConstraint(
                        e = pulp.lpSum([decisionVariables[row][col][value] for value in values]),
                        sense = pulp.LpConstraintEQ,
                        rhs = 1,
                        name = f'valueConstraint{row}{col}'
                    )
                )

        # Each row must contain values 1-9
        for row in rows:
            for val in values:
                self.problem.addConstraint(
                    pulp.LpConstraint(
                        e = pulp.lpSum([decisionVariables[row][col][val]*val for col in columns]),
                        sense = pulp.LpConstraintEQ,
                        rhs = val,
                        name = f'rowConstraint{row}{val}'
                    )
                )

        # Each column must contain values 1-9
        for col in columns:
            for val in values:
                self.problem.addConstraint(
                    pulp.LpConstraint(
                        e = pulp.lpSum([decisionVariables[row][col][val]*val for row in rows]),
                        sense = pulp.LpConstraintEQ,
                        rhs = val,
                        name = f'columnConstraint{col}{val}'   
                    )
                )

        # Each 3x3 box must contain values 1-9
        for box in boxes:
            boxRow = int(box / 3)
            boxCol = int(box % 3)
            for val in values:
                self.problem.addConstraint(
                    pulp.LpConstraint(
                        e = pulp.lpSum([decisionVariables[boxRow * 3 + row][boxCol * 3 + col][val]*val  for col in range(0,3) for row in range(0,3)]),
                        sense = pulp.LpConstraintEQ,
                        rhs = val,
                        name = f'boxConstraint{box}{val}'
                    )
                )

    def _initializeGrid(self):
        values = self.VALUE_RANGE
        
        # Set inital grid as constraint
        for i in self.INDEX_RANGE:
            for j in self.INDEX_RANGE:
                if self.grid[i][j] != 0:
                    self.problem.addConstraint(
                        pulp.LpConstraint(
                            e = pulp.lpSum([self.decisionVariables[i][j][val] * val for val in values]),
                            sense = pulp.LpConstraintEQ,
                            rhs = self.grid[i][j],
                            name = f'inputGrid{i}{j}'
                        )
                    )
    
    def _updateGrid(self):
        rows    = self.INDEX_RANGE
        columns = self.INDEX_RANGE
        values  = self.VALUE_RANGE

        for row in rows:
            for col in columns:
                for val in values:
                    if pulp.value(self.decisionVariables[row][col][val]):
                        self.grid[row][col] = val

def main():
    with open('grid2.pickle', 'rb') as f:
        grid = pickle.load(f)
    
   # hSolver = HeuristicSolver(grid)


    lSolver = LinearSolver(grid)
    lSolver.solve()
    lSolver.showGrid(pygame.Color(0, 255, 0))


if __name__ == '__main__':
    main()