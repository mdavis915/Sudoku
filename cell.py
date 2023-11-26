import pygame
import sys

# Define constants
WIDTH = 540
HEIGHT = 600
LINE_WIDTH = 2
SQUARE_SIZE = 60
BG_COLOR = (0, 0, 139)
LINE_COLOR = (255, 165, 0)
RED = (255, 0, 0)

# Define the Cell class
class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.set_sketched_value = value
        self.selected = False

    def set_cell_values(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.set_sketched_value = value

    def draw(self):
        cell_size = SQUARE_SIZE
        chip_font = pygame.font.Font(None, 60)

        # Draw cell outline
        pygame.draw.rect(self.screen, LINE_COLOR, (self.col * cell_size, self.row * cell_size, cell_size, cell_size), LINE_WIDTH)

        # Draw the selected cell in red
        if self.selected:
            pygame.draw.rect(self.screen, RED, (self.col * cell_size, self.row * cell_size, cell_size, cell_size), LINE_WIDTH)

        # Draw the cell value
        if self.value:
            chip_surf = chip_font.render(str(self.value), 1, LINE_COLOR)
            chip_rect = chip_surf.get_rect(
                center=(self.col * cell_size + cell_size // 2, self.row * cell_size + cell_size // 2 + 3))
            self.screen.blit(chip_surf, chip_rect)

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("sample sudoku cell")

# Create a sample cell
sample_cell = Cell(1, 0, 0, screen)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check for mouse click events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Get the mouse position
                mouse_x, mouse_y = event.pos

                # Check if the mouse is within the boundaries of the sample cell
                if (sample_cell.col * SQUARE_SIZE <= mouse_x < (sample_cell.col + 1) * SQUARE_SIZE and
                        sample_cell.row * SQUARE_SIZE <= mouse_y < (sample_cell.row + 1) * SQUARE_SIZE):
                    sample_cell.selected = not sample_cell.selected

    # Clear the screen
    screen.fill(BG_COLOR)

    # Draw the sample cell
    sample_cell.draw()

    # Update the display
    pygame.display.flip()

