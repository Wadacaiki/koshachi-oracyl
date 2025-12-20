import pygame
from button import Button, TextInput


class AuthMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background = None
        self.buttons = []
        self.text_inputs = []
        self.current_mode = None
        self.load_background()
        self.create_buttons()

    def load_background(self):
        try:
            self.background = pygame.image.load("assets/bg_menu.png")
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except Exception:
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((30, 30, 60))

    def create_buttons(self):
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2

        if not self.current_mode:
            # Основные кнопки регистрации/входа
            register_btn = Button(center_x - 100, center_y - 50, "Регистрация", lambda: self.set_mode('register'))
            login_btn = Button(center_x - 100, center_y + 20, "Вход", lambda: self.set_mode('login'))
            exit_btn = Button(20, self.screen_height - 70, "Выход", lambda: "exit")
            self.buttons = [register_btn, login_btn, exit_btn]
            self.text_inputs = []
        else:
            # Поля ввода и кнопка подтверждения
            nickname_input = TextInput(center_x - 150, center_y - 60, 300, 40, "Ник")
            password_input = TextInput(center_x - 150, center_y, 300, 40, "Пароль")
            confirm_btn = Button(center_x - 100, center_y + 60, "Подтвердить", lambda: "confirm")
            back_btn = Button(center_x - 100, center_y + 130, "Назад", lambda: self.set_mode(None))
            exit_btn = Button(20, self.screen_height - 70, "Выход", lambda: "exit")

            self.text_inputs = [nickname_input, password_input]
            self.buttons = [confirm_btn, back_btn, exit_btn]

    def set_mode(self, mode):
        self.current_mode = mode
        self.create_buttons()
        return None

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # Заголовок
        font = pygame.font.SysFont("Arial", 48)
        title = font.render("Кошачий оракул", True, (255, 255, 255))
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 100))

        for button in self.buttons:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(screen)

        for text_input in self.text_inputs:
            text_input.draw(screen)

    def handle_event(self, event):
        for button in self.buttons:
            result = button.handle_event(event)
            if result:
                return result

        for text_input in self.text_inputs:
            text_input.handle_event(event)

        return None

    def get_credentials(self):
        if len(self.text_inputs) >= 2:
            return self.text_inputs[0].text, self.text_inputs[1].text
        return "", ""
