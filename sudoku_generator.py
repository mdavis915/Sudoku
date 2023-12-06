import math
import random


class SudokuGenerator:
    
    # class constructor to create board
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.box_length = int(math.sqrt(row_length))
        self.board = [[0 for i in range(row_length)] for i in range(row_length)]
    
    # returns a 2D python list of numbers which represents the board
    def get_board(self):
        return self.board

    # displays the board to the console
    def print_board(self):
        for row in self.board:
            print(row)

    # determines if num is contained in the specified row (horizontal) of the board
    def valid_in_row(self, row, num):
        for i in range(self.row_length):
            if self.board[row][i] == num:
                return False
        return True

    # determines if num is contained in the specified column (vertical) of the board
    def valid_in_col(self, col, num):
        for i in range(self.row_length):
            if self.board[i][col] == num:
                return False
        return True

    # determines if num is contained in the 3x3 box specified on the board
    def valid_in_box(self, row_start, col_start, num):
        for row in range(3):
            for col in range(3):
                if self.board[row_start + row][col_start + col] == num:
                    return False
        return True
    
    # Determines if it is valid to enter num at (row, col) in the board
    def is_valid(self, row, col, num):
        return(self.valid_in_row(row, num) and self.valid_in_col(col, num) and self.valid_in_box(row - row % 3, col - col % 3, num))

    # fills the specified 3x3 box with values
    def fill_box(self, row_start, col_start):
        for i in range(3):
            for j in range(3):
                while True:
                    num = self.randomNumber(self.row_length)
                    if self.valid_in_box(row_start, col_start, num):
                        break
                self.board[row_start+i][col_start+j] = num
                
    # returns a random number
    def randomNumber(self, value):
        return random.randint(1, value)
    
    # fills the three boxes along the main diagonal of the board
    def fill_diagonal(self):
        for i in range(0, self.row_length, 3):
            self.fill_box(i, i)

    # fills the remaining cells of the board
    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True
        
        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    # constructs a solution by calling fill_diagonal and fill_remaining
    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, 3)

    # removes the appropriate number of cells from the board
    def remove_cells(self):
        num = self.removed_cells
        
        while (num != 0):
            i = self.randomNumber(self.row_length) - 1
            j = self.randomNumber(self.row_length) - 1
            if (self.board[i][j] != 0):
                num -= 1
                self.board[i][j] = 0

'''
Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution
'''
def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board



