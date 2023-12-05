import copy
import pygame
import sys
from cell import Cell
from sudoku_generator import generate_sudoku

# Define constants
WIDTH = 540
HEIGHT = 600
LINE_WIDTH = 13
SQUARE_SIZE = 180
BG_COLOR = (0, 0, 139)
LINE_COLOR = (237, 150, 36)
RED = (255, 0, 0)


class Board:
    def __init__(self, width, height, screens, difficulty):
        self.width = width
        self.height = height
        self.screen = screens
        self.difficulty = difficulty

        # Determined how many cells will be removed based on the difficulty selected.
        if self.difficulty == "Easy":
            removed_cell = 30
        elif self.difficulty == "Medium":
            removed_cell = 40
        else:
            removed_cell = 50

        # Defines 3 different lists containing the 2D board, the solution for the sudoku, and the state of the
        # original board when the game is first started.
        self.board, self.solution = generate_sudoku(9, removed_cell)
        self.original_board = copy.deepcopy(self.board)
        self.cells = [
            Cell(self.board[i][j], i, j, self.screen)
            for i in range(0, 9)
            for j in range(0, 9)
        ]

    def draw(self):
        # Draws horizontal lines of Sudoku Grid
        for i in range(1, 3):
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (0, i * SQUARE_SIZE),
                (WIDTH, i * SQUARE_SIZE),
                LINE_WIDTH,
            )

        # Draws vertical lines of Sudoku Grid
        for i in range(1, 3):
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (i * SQUARE_SIZE, 0),
                (i * SQUARE_SIZE, WIDTH),
                LINE_WIDTH,
            )

        # Draws each cell of the sudoku board from the cell list containing Cell objects.
        for i in self.cells:
            i.draw()

    def select(self, row, col):
        # Makes sure any previously selected cell will be unselected when a new cell is selected.
        for i in self.cells:
            i.selected = False
            i.draw()

        # Marks the cell at (row, col) in the board as the current selected cell. This cell is denoted in red.
        for i in self.cells:
            if i.row == row and i.col == col:
                i.selected = True
                i.draw()

    # If a tuple of (x,y) coordinates is within the displayed board, this function returns a tuple of the
    # (row, col) of the cell which was clicked. Otherwise, this function returns None.
    def click(self, x, y):
        row = y // 60
        col = x // 60
        i = (row, col)

        if (8 >= row >= 0) and (8 >= col >= 0):
            return i
        else:
            return None

    def clear(self):
        # Clears the cell value of the cell that is currently being selected. Note: The user can only clear the value
        # and sketch value of a cell if they are filled by themselves and is not a cell that has been randomly
        # generated (value was already given at the beginning).
        for i in self.cells:
            if i.selected and self.original_board[i.row][i.col] == 0:
                i.set_cell_values(0)
                i.draw()
        self.update_board()

    # Sets the sketched value of the current selected cell equal to user entered value. It will be displayed in the
    # top-left corner of the cell using the draw() function.
    def sketch(self, value):
        for i in self.cells:
            if i.selected and self.original_board[i.row][i.col] == 0 and not i.value:
                i.set_sketched_value(value)

    # Sets the value of the current selected cell equal to user entered value. Called when the user presses the Enter
    # key. This will only be done if the selected cell was originally blank or equal to 0.
    def place_number(self, value=None):
        for i in self.cells:
            if i.selected and self.original_board[i.row][i.col] == 0:
                i.set_cell_values(value or i.sketched_value)
                i.sketched_value = 0
                i.draw()
        self.update_board()

    # Resets all cells in the board to their original values.
    def reset_to_original(self):
        original_cells = [
            Cell(self.original_board[i][j], i, j, self.screen)
            for i in range(0, 9)
            for j in range(0, 9)
        ]

        for i in range(0, len(original_cells)):
            self.cells[i].set_cell_values(original_cells[i].value)
            self.cells[i].set_sketched_value(original_cells[i].sketched_value)
            self.cells[i].selected = False
            self.cells[i].draw()

        self.update_board()

    # Returns a Boolean value indicating whether the board is full or not.
    def is_full(self):
        self.update_board()

        for i in range(0, 9):
            for j in range(0, 9):
                if self.board[i][j] == 0:
                    return False
        return True

    # Updates the underlying 2D board with the values in all cells.
    def update_board(self):
        count = 0
        for i in range(0, 9):
            for j in range(0, 9):
                self.board[i][j] = self.cells[count].value
                count += 1

    # Finds an empty cell and returns its row and col as a tuple (x, y).
    def find_empty(self):
        self.update_board()

        for i in range(0, 9):
            for j in range(0, 9):
                if self.board[i][j] == 0:
                    return i, j

    # Check whether the Sudoku board is solved correctly.
    def check_board(self):
        if not self.is_full():
            return False

        for i in range(0, 9):
            for j in range(0, 9):
                if self.board[i][j] != self.solution[i][j]:
                    return False

        return True


# Used to test the board class:

# # Initialize Pygame
# pygame.init()
#
# # Create the screen
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Sudoku")
#
# # Create a sample Sudoku board
# sample_board = Board(540, 600, screen, "Hard")
# print(sample_board.board)
# sample_board.select(0,0)
# sample_board.select(0,3)
# sample_board.place_number(9)
# sample_board.select(0, 0)
# sample_board.place_number(1)
# print(sample_board.board)
#
# # sample_board.select(0, 0)
# # sample_board.select(8, 8)
# # sample_board.place_number(10)
# # sample_board.update_board()
# # print(sample_board.solution)
# # print(sample_board.board)
# # print(sample_board.original_board)
# # print(sample_board.is_full())
# # print(sample_board.check_board())
# # sample_board.select(8, 8)
# # sample_board.clear()
# # x, y = sample_board.find_empty()
# # print(x, y)
# # sample_board.select(x, y)
# # sample_board.place_number(4)
# #
# # print(sample_board.board)
# # # sample_board.reset_to_original()
# # Main loop
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#
#         # Check for mouse click events
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if event.button == 1:  # Left mouse button
#                 # Get the mouse position
#                 mouse_x, mouse_y = event.pos
#                 sample_board.reset_to_original()
#
#
#     # Clear the screen
#     screen.fill(BG_COLOR)
#
#     # Draw the sample board
#     sample_board.draw()
#
#     # Update the display
#     pygame.display.flip()
