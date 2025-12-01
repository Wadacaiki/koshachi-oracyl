import pygame
import sys
from menu import MainMenu
from settings import SettingsMenu
from auth import AuthMenu
from game import Game

# Константы
WIDTH, HEIGHT = 1200, 800
FPS = 60


def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rusty Lake - Тайны Пирамиды")
    clock = pygame.time.Clock()

    # Создаем экраны
    auth_menu = AuthMenu(WIDTH, HEIGHT)
    main_menu = MainMenu(WIDTH, HEIGHT)
    settings_menu = SettingsMenu(WIDTH, HEIGHT)
    game = None

    current_screen = "auth"  # auth, main, settings, game

    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            result = None
            if current_screen == "auth":
                result = auth_menu.handle_event(event)
            elif current_screen == "main":
                result = main_menu.handle_event(event)
            elif current_screen == "settings":
                result = settings_menu.handle_event(event)
            elif current_screen == "game" and game:
                # Обработка событий игры происходит внутри game.run()
                pass

            if result:
                if result == "exit":
                    running = False
                elif result == "play":
                    game = Game(WIDTH, HEIGHT)
                    current_screen = "game"
                elif result == "settings":
                    current_screen = "settings"
                elif result == "main_menu":
                    current_screen = "main"
                elif result == "confirm":
                    username, password = auth_menu.get_credentials()
                    if username and password:
                        current_screen = "main"
                elif result == "back":
                    current_screen = "main"

        # Отрисовка текущего экрана
        screen.fill((50, 50, 50))

        if current_screen == "auth":
            auth_menu.draw(screen)
        elif current_screen == "main":
            main_menu.draw(screen)
        elif current_screen == "settings":
            settings_menu.draw(screen)
        elif current_screen == "game" and game:
            game_result = game.run(screen)
            if game_result == "main_menu":
                current_screen = "main"
            elif game_result == "exit":
                running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()