import pygame
from button import Button


class MainMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background = None
        self.buttons = []
        self.load_background()
        self.create_buttons()

    def load_background(self):
        try:
            self.background = pygame.image.load("assets/bg_menu.png")
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except:
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((50, 50, 50))

    def create_buttons(self):
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2

        play_btn = Button(center_x - 100, center_y - 50, "Играть", lambda: "play")
        settings_btn = Button(center_x - 100, center_y + 20, "Настройки", lambda: "settings")
        exit_btn = Button(20, self.screen_height - 70, "Выход", lambda: "exit")

        self.buttons = [play_btn, settings_btn, exit_btn]

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        for button in self.buttons:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(screen)

    def handle_event(self, event):
        for button in self.buttons:
            result = button.handle_event(event)
            if result:
                return result
        return None