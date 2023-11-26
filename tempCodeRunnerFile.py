import pygame

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False
        self.sketched_value = 0

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        chip_font = pygame.font.Font(None, 60)

        # Draw the cell outline
        pygame.draw.rect(
            self.screen, (255, 0, 0) if self.selected else (0, 0, 0),
            pygame.Rect(self.col * 60, self.row * 60, 60, 60), 2
        )

        # Draw the value if it's not 0
        if self.value != 0:
            chip_surf = chip_font.render(str(self.value), 1, (0, 0, 0))
            chip_rect = chip_surf.get_rect(
                center=(self.col * 60 + 30, self.row * 60 + 30)
            )
            self.screen.blit(chip_surf, chip_rect)

        # Draw the sketched value if it's not 0
        if self.sketched_value != 0:
            sketch_surf = chip_font.render(str(self.sketched_value), 1, (128, 128, 128))
            sketch_rect = sketch_surf.get_rect(
                topleft=(self.col * 60 + 5, self.row * 60 + 5)
            )
            self.screen.blit(sketch_surf, sketch_rect)
