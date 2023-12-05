import pygame, sys
from board import *


def draw_button(screen, font, text, padding=(0, 0), offset=(0, 0)):
    text = font.render(text, 1, BG_COLOR)

    surface = pygame.Surface(
        (
            max(text.get_size()[0] + padding[0], font.get_height() ** 1.5),
            text.get_size()[1] + padding[1],
        )
    )
    surface.fill(LINE_COLOR)
    surface.blit(text, (padding[0] // 2, padding[1] // 2))

    rectangle = surface.get_rect(
        center=(WIDTH // 2 + offset[0], HEIGHT // 2 + offset[1])
    )

    screen.blit(surface, rectangle)

    return rectangle


def draw_game_start(screen):
    # Set base screen settings
    title_font = pygame.font.Font(None, 100)
    button_font = pygame.font.Font(None, 50)

    screen.fill(BG_COLOR)

    # Draw title
    title_surface = title_font.render("Sudoku", 1, LINE_COLOR)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
    screen.blit(title_surface, title_rect)

    # Draw difficulty buttons
    easy_rect = draw_button(screen, button_font, "Easy", (45, 30), (0, 0))
    medium_rect = draw_button(screen, button_font, "Medium", (45, 30), (0, 100))
    hard_rect = draw_button(screen, button_font, "Hard", (45, 30), (0, 200))

    pygame.display.flip()

    # Return difficult based on button pressed
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos):
                    return "Easy"
                if medium_rect.collidepoint(event.pos):
                    return "Medium"
                if hard_rect.collidepoint(event.pos):
                    return "Hard"


def draw_game_main(screen, difficulty):
    # Set base screen settings
    button_font = pygame.font.Font(None, 30)

    screen.fill(BG_COLOR)

    # Create board object
    board = Board(WIDTH, HEIGHT, screen, difficulty)
    board.draw()

    # Draw buttons
    reset_rect = draw_button(screen, button_font, "Reset", (50, 20), (-150, 270))
    restart_rect = draw_button(screen, button_font, "Restart", (50, 20), (0, 270))
    exit_rect = draw_button(screen, button_font, "Exit", (50, 20), (150, 270))

    pygame.display.flip()

    selected_row, selected_col = 0, 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if reset_rect.collidepoint(event.pos):
                        board.reset_to_original()
                        pygame.display.flip()
                    elif restart_rect.collidepoint(event.pos):
                        return False, None
                    elif exit_rect.collidepoint(event.pos):
                        sys.exit()
                    else:
                        selected_cell = board.click(*event.pos)
                        if selected_cell:
                            selected_row, selected_col = selected_cell
                            board.select(selected_row, selected_col)
                            pygame.display.flip()
            if event.type == pygame.KEYDOWN:
                # Handle arrow keys
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    if event.key == pygame.K_LEFT:
                        selected_col = (selected_col - 1) % 9
                    elif event.key == pygame.K_RIGHT:
                        selected_col = (selected_col + 1) % 9
                    elif event.key == pygame.K_UP:
                        selected_row = (selected_row - 1) % 9
                    elif event.key == pygame.K_DOWN:
                        selected_row = (selected_row + 1) % 9

                    # Update the selection
                    board.select(selected_row, selected_col)
                    pygame.display.flip()

                # Set sketched number
                elif event.unicode.isnumeric():
                    board.sketch(int(event.unicode))
                    board.draw()
                    pygame.display.flip()
                # Enter sketched number into cell
                elif event.key == pygame.K_RETURN:
                    board.place_number()
                    pygame.display.flip()

                    # Check for win condition
                    if board.is_full():
                        return True, board.check_board()
                # Remove number in cell
                elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    board.clear()
                    pygame.display.flip()



def draw_game_won(screen):
    # Set base screen settings
    title_font = pygame.font.Font(None, 100)
    button_font = pygame.font.Font(None, 50)

    screen.fill(BG_COLOR)

    # Draw title
    title_surface = title_font.render("Game Won!", 1, LINE_COLOR)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
    screen.blit(title_surface, title_rect)

    # Draw button
    exit_rect = draw_button(screen, button_font, "Exit", (45, 30), (0, 0))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_rect.collidepoint(event.pos):
                    sys.exit()


def draw_game_over(screen):
    # Set base screen settings
    title_font = pygame.font.Font(None, 100)
    button_font = pygame.font.Font(None, 50)

    screen.fill(BG_COLOR)

    # Draw title
    title_surface = title_font.render("Game Over :(", 1, LINE_COLOR)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
    screen.blit(title_surface, title_rect)

    # Draw button
    restart_rect = draw_button(screen, button_font, "Restart", (45, 30), (0, 0))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    return


def main():
    # Loop until player exits
    while True:
        game_over = False
        win = False

        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # Loop until game is over
        while not game_over:
            difficulty = draw_game_start(screen)

            game_over, win = draw_game_main(screen, difficulty)

        if win:
            draw_game_won(screen)
        else:
            draw_game_over(screen)


if __name__ == "__main__":
    main()
