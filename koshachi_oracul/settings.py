import pygame
from button import Button


class SettingsMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background = None
        self.buttons = []
        self.music_enabled = True
        self.current_music = "original"
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

        original_btn = Button(center_x - 100, center_y - 100, "Оригинал", lambda: self.set_music("original"))
        egypt_btn = Button(center_x - 100, center_y - 30, "Египетская", lambda: self.set_music("egypt"))
        prayer_btn = Button(center_x - 100, center_y + 40, "Молитва", lambda: self.set_music("prayer"))
        toggle_btn = Button(center_x - 50, center_y + 110, "", self.toggle_music, 100, 40)
        exit_btn = Button(20, self.screen_height - 70, "Выход", lambda: "exit")

        self.buttons = [original_btn, egypt_btn, prayer_btn, toggle_btn, exit_btn]

    def set_music(self, music_type):
        self.current_music = music_type
        if self.music_enabled:
            self.play_music()
        return None

    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            self.play_music()
        else:
            pygame.mixer.music.stop()
        return None

    def play_music(self):
        try:
            music_file = f"assets/{self.current_music}.mp3"
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)  # Зациклить музыку
        except:
            print(f"Не удалось загрузить музыку: {music_file}")

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # Отображение текущего состояния музыки
        font = pygame.font.SysFont("Arial", 24)
        music_text = f"Музыка: {'🔊' if self.music_enabled else '🔇'}"
        text_surface = font.render(music_text, True, (255, 255, 255))
        screen.blit(text_surface, (self.screen_width // 2 + 60, self.screen_height // 2 + 115))

        for button in self.buttons:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(screen)

    def handle_event(self, event):
        for button in self.buttons:
            result = button.handle_event(event)
            if result:
                return result
        return None