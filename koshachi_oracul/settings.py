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
            self.background.fill((40, 40, 80))

    def create_buttons(self):
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2

        original_btn = Button(center_x - 100, center_y - 100, "Оригинал", lambda: self.set_music("original"))
        egypt_btn = Button(center_x - 100, center_y - 30, "Египетская", lambda: self.set_music("egypt"))
        prayer_btn = Button(center_x - 100, center_y + 40, "Молитва", lambda: self.set_music("prayer"))

        # Кнопка переключения музыки ВКЛ/ВЫКЛ
        toggle_text = "Музыка: ВКЛ" if self.music_enabled else "Музыка: ВЫКЛ"
        toggle_btn = Button(center_x - 100, center_y + 110, toggle_text, self.toggle_music)

        # Кнопка "Назад" в главное меню - слева снизу
        back_btn = Button(20, self.screen_height - 70, "Назад", lambda: "main_menu")

        # Кнопка "Выход" - справа снизу
        exit_btn = Button(self.screen_width - 250, self.screen_height - 70, "Выход", lambda: "exit")

        self.buttons = [original_btn, egypt_btn, prayer_btn, toggle_btn, back_btn, exit_btn]

    def set_music(self, music_type):
        self.current_music = music_type
        if self.music_enabled:
            self.play_music()
        return None

    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        # Обновляем текст кнопки
        self.create_buttons()  # Пересоздаем кнопки с новым текстом
        if self.music_enabled:
            self.play_music()
        else:
            pygame.mixer.music.stop()
        return None

    def play_music(self):
        try:
            music_file = f"assets/{self.current_music}.mp3"
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)
        except:
            pass

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # Заголовок
        font = pygame.font.SysFont("Arial", 48)
        title = font.render("Настройки", True, (255, 255, 255))
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 100))

        for button in self.buttons:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(screen)

    def handle_event(self, event):
        for button in self.buttons:
            result = button.handle_event(event)
            if result:
                return result
        return None