import pygame
from button import Button


class PyramidPuzzle:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background = None
        self.current_puzzle = None  # "brick" или "domofon"
        self.domofon_code = []
        self.brick_numbers = {1: "2", 2: "9", 3: "0", 4: "5"}
        self.load_background()

    def load_background(self):
        try:
            self.background = pygame.image.load("assets/Pyramid.png")
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except:
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((50, 50, 50))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # Домофон
        try:
            domofon_img = pygame.image.load("assets/domofon.png")
            domofon_img = pygame.transform.scale(domofon_img, (80, 80))
            screen.blit(domofon_img, (self.screen_width // 2 + 100, self.screen_height - 200))
        except:
            pygame.draw.rect(screen, (50, 50, 50), (self.screen_width // 2 + 100, self.screen_height - 200, 80, 80))

        # Кирпичи (размещены на пирамиде)
        brick_positions = [
            (400, 300),  # кирпич 1
            (450, 280),  # кирпич 2
            (500, 320),  # кирпич 3
            (550, 290)  # кирпич 4
        ]

        for i, pos in enumerate(brick_positions):
            try:
                brick_img = pygame.image.load(f"assets/kirpich{i + 1}.png")
                brick_img = pygame.transform.scale(brick_img, (60, 40))
                screen.blit(brick_img, pos)
            except:
                pygame.draw.rect(screen, (150, 100, 50), (pos[0], pos[1], 60, 40))

        # Если активна головоломка, рисуем ее поверх
        if self.current_puzzle == "domofon":
            self.draw_domofon_puzzle(screen)
        elif self.current_puzzle == "brick":
            self.draw_brick_puzzle(screen)

    def draw_domofon_puzzle(self, screen):
        # Затемнение фона
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        try:
            domofon_img = pygame.image.load("assets/domofon_blizhe.png")
            domofon_img = pygame.transform.scale(domofon_img, (400, 300))
            screen.blit(domofon_img, (self.screen_width // 2 - 200, self.screen_height // 2 - 150))
        except:
            pygame.draw.rect(screen, (50, 50, 50),
                             (self.screen_width // 2 - 200, self.screen_height // 2 - 150, 400, 300))

        # Отображение введенного кода
        font = pygame.font.SysFont("Arial", 36)
        code_display = " ".join(self.domofon_code) if self.domofon_code else "_ _ _ _"
        text_surface = font.render(code_display, True, (255, 255, 255))
        screen.blit(text_surface, (self.screen_width // 2 - text_surface.get_width() // 2, self.screen_height // 2))

        # Кнопка назад
        back_btn = Button(self.screen_width // 2 - 50, self.screen_height // 2 + 100, "Назад",
                          lambda: self.set_puzzle(None))
        back_btn.check_hover(pygame.mouse.get_pos())
        back_btn.draw(screen)

    def draw_brick_puzzle(self, screen, brick_num=1):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont("Arial", 72)
        text = self.brick_numbers.get(brick_num, "?")
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface,
                    (self.screen_width // 2 - text_surface.get_width() // 2,
                     self.screen_height // 2 - text_surface.get_height() // 2))

    def set_puzzle(self, puzzle_type, data=None):
        self.current_puzzle = puzzle_type
        self.current_puzzle_data = data
        if puzzle_type is None:
            self.domofon_code = []

    def handle_event(self, event):
        if self.current_puzzle:
            return self.handle_puzzle_event(event)
        else:
            return self.handle_room_event(event)

    def handle_puzzle_event(self, event):
        if self.current_puzzle == "domofon":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if "".join(self.domofon_code) == "2905":
                        return "pyramid_solved"  # Загадка решена!
                    else:
                        self.domofon_code = []
                elif event.key == pygame.K_BACKSPACE:
                    self.domofon_code = self.domofon_code[:-1] if self.domofon_code else []
                elif event.unicode.isdigit() and len(self.domofon_code) < 4:
                    self.domofon_code.append(event.unicode)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                back_btn = Button(self.screen_width // 2 - 50, self.screen_height // 2 + 100, "Назад",
                                  lambda: self.set_puzzle(None))
                if back_btn.rect.collidepoint(event.pos):
                    self.set_puzzle(None)

        elif self.current_puzzle == "brick":
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                self.set_puzzle(None)

        return None

    def handle_room_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Проверяем домофон
            domofon_rect = pygame.Rect(self.screen_width // 2 + 100, self.screen_height - 200, 80, 80)
            if domofon_rect.collidepoint(x, y):
                self.set_puzzle("domofon")
                return None

            # Проверяем кирпичи
            brick_positions = [
                (400, 300, 60, 40),  # кирпич 1
                (450, 280, 60, 40),  # кирпич 2
                (500, 320, 60, 40),  # кирпич 3
                (550, 290, 60, 40)  # кирпич 4
            ]

            for i, (bx, by, bw, bh) in enumerate(brick_positions):
                if bx <= x <= bx + bw and by <= y <= by + bh:
                    self.set_puzzle("brick", i + 1)
                    return None

        return None