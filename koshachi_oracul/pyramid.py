import pygame


class PyramidPuzzle:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Домофон (маленький на фоне)
        self.DOMOFON_WIDTH = 80
        self.DOMOFON_HEIGHT = 80
        self.DOMOFON_X = self.screen_width // 2 + 130
        self.DOMOFON_Y = self.screen_height - 200

        # Кирпичи
        self.BRICK_WIDTH = 160
        self.BRICK_HEIGHT = 70
        self.BRICK_POSITIONS = [
            (300, 590),  # кирпич 1
            (350, 380),  # кирпич 2
            (600, 320),  # кирпич 3
            (750, 480),  # кирпич 4
        ]

        # Увеличенный домофон
        self.DOMOFON_CLOSE_WIDTH = 400
        self.DOMOFON_CLOSE_HEIGHT = 300
        self.DOMOFON_CLOSE_X = self.screen_width // 2 - 200
        self.DOMOFON_CLOSE_Y = self.screen_height // 2 - 150

        self.background = None
        self.current_puzzle = None   # None / "domofon" / "brick"
        self.current_puzzle_data = None  # номер кирпича
        self.domofon_code = []
        self.brick_numbers = {1: "2", 2: "9", 3: "0", 4: "5"}

        self.load_background()

    def load_background(self):
        try:
            self.background = pygame.image.load("assets/Pyramid.png")
            self.background = pygame.transform.scale(
                self.background, (self.screen_width, self.screen_height)
            )
        except:
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((50, 50, 50))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # Домофон
        try:
            domofon_img = pygame.image.load("assets/domofon.png")
            domofon_img = pygame.transform.scale(
                domofon_img, (self.DOMOFON_WIDTH, self.DOMOFON_HEIGHT)
            )
            screen.blit(domofon_img, (self.DOMOFON_X, self.DOMOFON_Y))
        except:
            pygame.draw.rect(
                screen,
                (50, 50, 50),
                (self.DOMOFON_X, self.DOMOFON_Y, self.DOMOFON_WIDTH, self.DOMOFON_HEIGHT),
            )

        # Кирпичи
        for i, (pos_x, pos_y) in enumerate(self.BRICK_POSITIONS):
            try:
                brick_img = pygame.image.load(f"assets/kirpich{i + 1}.png")
                brick_img = pygame.transform.scale(
                    brick_img, (self.BRICK_WIDTH, self.BRICK_HEIGHT)
                )
                screen.blit(brick_img, (pos_x, pos_y))
            except:
                pygame.draw.rect(
                    screen,
                    (150, 100, 50),
                    (pos_x, pos_y, self.BRICK_WIDTH, self.BRICK_HEIGHT),
                )

        # Активная головоломка поверх
        if self.current_puzzle == "domofon":
            self.draw_domofon_puzzle(screen)
        elif self.current_puzzle == "brick":
            self.draw_brick_puzzle(screen)

    # ---------- РИСОВАНИЕ ПАЗЛОВ ----------

    def draw_domofon_puzzle(self, screen):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        try:
            domofon_img = pygame.image.load("assets/domofon_blizhe.png")
            domofon_img = pygame.transform.scale(
                domofon_img, (self.DOMOFON_CLOSE_WIDTH, self.DOMOFON_CLOSE_HEIGHT)
            )
            screen.blit(domofon_img, (self.DOMOFON_CLOSE_X, self.DOMOFON_CLOSE_Y))
        except:
            pygame.draw.rect(
                screen,
                (50, 50, 50),
                (
                    self.DOMOFON_CLOSE_X,
                    self.DOMOFON_CLOSE_Y,
                    self.DOMOFON_CLOSE_WIDTH,
                    self.DOMOFON_CLOSE_HEIGHT,
                ),
            )

        # Отображение кода
        font = pygame.font.SysFont("Arial", 36)
        code_display = (
            "       ".join(self.domofon_code)
            if self.domofon_code
            else "_       _       _       _"
        )
        text_surface = font.render(code_display, True, (0, 0, 0))
        text_y = self.screen_height // 2 - 50
        text_x = self.screen_width // 2 - 150
        screen.blit(text_surface, (text_x, text_y))

    def draw_brick_puzzle(self, screen):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont("Arial", 72)
        text = self.brick_numbers.get(self.current_puzzle_data, "?")
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(
            text_surface,
            (
                self.screen_width // 2 - text_surface.get_width() // 2,
                self.screen_height // 2 - text_surface.get_height() // 2,
            ),
        )

    # ---------- СМЕНА СОСТОЯНИЯ ----------

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

    # ---------- СОБЫТИЯ ВНУТРИ ПАЗЛОВ ----------

    def handle_puzzle_event(self, event):
        # Домофон
        if self.current_puzzle == "domofon":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if "".join(self.domofon_code) == "2905":
                        return "pyramid_solved"
                    else:
                        self.domofon_code = []
                elif event.key == pygame.K_BACKSPACE:
                    self.domofon_code = self.domofon_code[:-1] if self.domofon_code else []
                elif event.unicode.isdigit() and len(self.domofon_code) < 4:
                    self.domofon_code.append(event.unicode)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                domofon_rect = pygame.Rect(
                    self.DOMOFON_CLOSE_X,
                    self.DOMOFON_CLOSE_Y,
                    self.DOMOFON_CLOSE_WIDTH,
                    self.DOMOFON_CLOSE_HEIGHT,
                )
                # клик ВНЕ увеличенного домофона — закрыть пазл
                if not domofon_rect.collidepoint(x, y):
                    self.set_puzzle(None)

        # Кирпич (показ цифры)
        elif self.current_puzzle == "brick":
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                self.set_puzzle(None)

        return None

    # ---------- СОБЫТИЯ НА ФОНЕ ПИРАМИДЫ ----------

    def handle_room_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos

            # Домофон
            domofon_rect = pygame.Rect(
                self.DOMOFON_X, self.DOMOFON_Y, self.DOMOFON_WIDTH, self.DOMOFON_HEIGHT
            )
            if domofon_rect.collidepoint(x, y):
                self.set_puzzle("domofon")
                return None

            # Кирпичи
            for i, (brick_x, brick_y) in enumerate(self.BRICK_POSITIONS):
                brick_rect = pygame.Rect(brick_x, brick_y, self.BRICK_WIDTH, self.BRICK_HEIGHT)
                if brick_rect.collidepoint(x, y):
                    self.set_puzzle("brick", i + 1)
                    return None

        return None
