import pygame
from pygame.locals import *
from client.static_variables import GAME_NAME, GAME_MAIN_FONT, BLACK, BLUE, WHITE, \
    YELLOW, SCREEN_WIDTH, SCREEN_HEIGHT
from .layout.text_functions import text_format

# Game Initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Game Framerate
clock = pygame.time.Clock()
FPS = 30


# Main Menu
def main_menu():
    menu = True
    selected = "start"

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        print("Start")
                    if selected == "quit":
                        pygame.quit()
                        quit()

        # Main Menu UI
        screen.fill(BLUE)
        title = text_format(GAME_NAME, GAME_MAIN_FONT, 90, YELLOW)
        if selected == "start":
            text_start = text_format("START", GAME_MAIN_FONT, 75, WHITE)
        else:
            text_start = text_format("START", GAME_MAIN_FONT, 75, BLACK)
        if selected == "quit":
            text_quit = text_format("QUIT", GAME_MAIN_FONT, 75, WHITE)
        else:
            text_quit = text_format("QUIT", GAME_MAIN_FONT, 75, BLACK)

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        # Main Menu Text
        screen.blit(title, (SCREEN_WIDTH / 2 - (title_rect[2] / 2), 80))
        screen.blit(text_start, (SCREEN_WIDTH / 2 - (start_rect[2] / 2), 300))
        screen.blit(text_quit, (SCREEN_WIDTH / 2 - (quit_rect[2] / 2), 360))
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Python - Pygame Simple Main Menu Selection")


if __name__ == "__main__":
    main_menu()
    pygame.quit()
    quit()