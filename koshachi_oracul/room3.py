import pygame
import random
from button import Button  # можно оставить, даже если сейчас не используется


class Room3:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Картина
        self.PAINTING_WIDTH = 500
        self.PAINTING_HEIGHT = 350
        self.PAINTING_X = self.screen_width - 650
        self.PAINTING_Y = 100

        # Карта под картиной
        self.MAP_WIDTH = 80
        self.MAP_HEIGHT = 60
        self.MAP_X = self.PAINTING_X + (self.PAINTING_WIDTH // 2) - (self.MAP_WIDTH // 2)
        self.MAP_Y = self.PAINTING_Y + self.PAINTING_HEIGHT + 10

        # Полка с запиской (верхняя)
        self.NOTE_SHELF_WIDTH = 250
        self.NOTE_SHELF_HEIGHT = 180
        self.NOTE_SHELF_X = 80
        self.NOTE_SHELF_Y = 120

        # Полка с символами (нижняя, оставляем как сейф с цифрами 567)
        self.SYMBOL_SHELF_WIDTH = 250
        self.SYMBOL_SHELF_HEIGHT = 180
        self.SYMBOL_SHELF_X = 80
        self.SYMBOL_SHELF_Y = 320

        # Статуэтки котов
        self.CAT_STATUE_WIDTH = 60
        self.CAT_STATUE_HEIGHT = 80
        self.CAT_STATUE_X_OFFSET = 45
        self.CAT_STATUE_Y_OFFSET = 10

        # Кристаллы на полу
        self.CRYSTAL_WIDTH = 80
        self.CRYSTAL_HEIGHT = 150
        self.CRYSTAL1_X = self.screen_width - 150
        self.CRYSTAL1_Y = self.screen_height - 150
        self.CRYSTAL2_X = self.screen_width - 900
        self.CRYSTAL2_Y = self.screen_height - 150

        # Стрелки
        self.ARROW_SIZE = 50

        # Состояния
        self.painting_completed = False
        self.map_taken = False
        self.note_safe_opened = False
        self.symbol_safe_opened = False
        self.black_cat_taken = False
        self.med_cat_taken = False
        self.kristal1_taken = False
        self.kristal2_taken = False

        # Текущая мини‑игра: None / "painting" / "note_safe" / "symbol_safe"
        self.current_puzzle = None

        # Ввод кодов
        self.note_safe_code = ""      # 1234
        self.symbol_safe_code = []    # 567

        # Пазл картины
        self.puzzle_tiles = None
        self.selected_tile = None

        # Ресурсы
        self.background = self._load_scaled("assets/bg_room.png",
                                            (self.screen_width, self.screen_height))
        self.left_arrow_img = self._load_scaled("assets/left_strelka.png", (50, 50))
        self.right_arrow_img = self._load_scaled("assets/right_strelka.png", (50, 50))
        self.font_mid = pygame.font.SysFont("Arial", 24)

    def _load_scaled(self, path, size):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        except:
            surf = pygame.Surface(size, pygame.SRCALPHA)
            surf.fill((80, 80, 80))
            return surf

    # ---------- РИСОВАНИЕ КОМНАТЫ ----------

    def draw(self, screen, has_all_statues):
        screen.blit(self.background, (0, 0))

        # Картина
        try:
            if self.painting_completed:
                painting_img = pygame.image.load("assets/sobrana_kartina.png").convert_alpha()
            else:
                painting_img = pygame.image.load("assets/ne_sobrana_kartina.png").convert_alpha()
            painting_img = pygame.transform.scale(
                painting_img, (self.PAINTING_WIDTH, self.PAINTING_HEIGHT)
            )
        except:
            painting_img = pygame.Surface((self.PAINTING_WIDTH, self.PAINTING_HEIGHT))
            painting_img.fill((120, 120, 120))
        screen.blit(painting_img, (self.PAINTING_X, self.PAINTING_Y))

        # Карта
        if self.painting_completed and not self.map_taken:
            try:
                map_img = pygame.image.load("assets/karta.png").convert_alpha()
                map_img = pygame.transform.scale(map_img, (self.MAP_WIDTH, self.MAP_HEIGHT))
            except:
                map_img = pygame.Surface((self.MAP_WIDTH, self.MAP_HEIGHT))
                map_img.fill((150, 150, 220))
            screen.blit(map_img, (self.MAP_X, self.MAP_Y))

        # Полка с запиской
        note_shelf_img = self._load_scaled(
            "assets/polka_s_seyfom_s_zapiskoy.png",
            (self.NOTE_SHELF_WIDTH, self.NOTE_SHELF_HEIGHT),
        )
        screen.blit(note_shelf_img, (self.NOTE_SHELF_X, self.NOTE_SHELF_Y))

        if self.note_safe_opened and not self.black_cat_taken:
            cat_x = self.NOTE_SHELF_X + self.CAT_STATUE_X_OFFSET
            cat_y = self.NOTE_SHELF_Y + self.CAT_STATUE_Y_OFFSET
            cat_img = self._load_scaled("assets/black_cat.png",
                                        (self.CAT_STATUE_WIDTH, self.CAT_STATUE_HEIGHT))
            screen.blit(cat_img, (cat_x, cat_y))

        # Полка с «символами» (сейф 567)
        symbol_shelf_img = self._load_scaled(
            "assets/polka_s_seyfom_s_simvolami.png",
            (self.SYMBOL_SHELF_WIDTH, self.SYMBOL_SHELF_HEIGHT),
        )
        screen.blit(symbol_shelf_img, (self.SYMBOL_SHELF_X, self.SYMBOL_SHELF_Y))

        if self.symbol_safe_opened and not self.med_cat_taken:
            cat_x = self.SYMBOL_SHELF_X + self.CAT_STATUE_X_OFFSET
            cat_y = self.SYMBOL_SHELF_Y + self.CAT_STATUE_Y_OFFSET
            cat_img = self._load_scaled("assets/med_cat.png",
                                        (self.CAT_STATUE_WIDTH, self.CAT_STATUE_HEIGHT))
            screen.blit(cat_img, (cat_x, cat_y))

        # Кристаллы
        if not self.kristal1_taken:
            c1_img = self._load_scaled("assets/kristal1.png",
                                       (self.CRYSTAL_WIDTH, self.CRYSTAL_HEIGHT))
            screen.blit(c1_img, (self.CRYSTAL1_X, self.CRYSTAL1_Y))

        if not self.kristal2_taken:
            c2_img = self._load_scaled("assets/kristal2.png",
                                       (self.CRYSTAL_WIDTH, self.CRYSTAL_HEIGHT))
            screen.blit(c2_img, (self.CRYSTAL2_X, self.CRYSTAL2_Y))

        # Стрелки
        self._draw_arrows(screen)

        # Модальные пазлы
        if self.current_puzzle == "painting":
            self._draw_painting_puzzle(screen)
        elif self.current_puzzle == "note_safe":
            self._draw_note_safe_puzzle(screen)
        elif self.current_puzzle == "symbol_safe":
            self._draw_symbol_safe_puzzle(screen)

        return None

    def _draw_arrows(self, screen):
        left_x = 20
        left_y = self.screen_height // 2 - self.ARROW_SIZE // 2
        right_x = self.screen_width - 20 - self.ARROW_SIZE
        right_y = left_y
        screen.blit(self.left_arrow_img, (left_x, left_y))
        screen.blit(self.right_arrow_img, (right_x, right_y))

    # ---------- ПАЗЛ КАРТИНЫ ----------

    def _init_painting_tiles(self):
        try:
            cat_image = pygame.image.load("assets/sama_kartina.png").convert_alpha()
            cat_image = pygame.transform.scale(cat_image, (400, 400))
        except:
            cat_image = pygame.Surface((400, 400))
            cat_image.fill((100, 100, 100))

        tile_size = 80
        grid_size = 5
        tiles = []

        for i in range(grid_size):
            for j in range(grid_size):
                tile_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
                tile_surface.blit(
                    cat_image,
                    (0, 0),
                    (
                        j * (400 // grid_size),
                        i * (400 // grid_size),
                        400 // grid_size,
                        400 // grid_size,
                    ),
                )
                tile_surface = pygame.transform.scale(tile_surface, (tile_size, tile_size))

                tiles.append(
                    {
                        "image": tile_surface,
                        "correct_pos": (i, j),
                        "current_pos": (i, j),
                        "rect": pygame.Rect(
                            self.screen_width // 2 - (grid_size * tile_size) // 2
                            + j * tile_size,
                            self.screen_height // 2 - (grid_size * tile_size) // 2
                            + i * tile_size,
                            tile_size,
                            tile_size,
                        ),
                    }
                )

        for _ in range(100):
            i1, i2 = random.sample(range(len(tiles)), 2)
            tiles[i1]["current_pos"], tiles[i2]["current_pos"] = (
                tiles[i2]["current_pos"],
                tiles[i1]["current_pos"],
            )
            for t in (tiles[i1], tiles[i2]):
                i, j = t["current_pos"]
                t["rect"].x = self.screen_width // 2 - (grid_size * tile_size) // 2 + j * tile_size
                t["rect"].y = self.screen_height // 2 - (grid_size * tile_size) // 2 + i * tile_size

        self.puzzle_tiles = tiles
        self.selected_tile = None

    def _draw_painting_puzzle(self, screen):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))

        try:
            bg = pygame.image.load("assets/patnashki.png").convert()
            bg = pygame.transform.scale(bg, (self.screen_width, self.screen_height))
        except:
            bg = pygame.Surface((self.screen_width, self.screen_height))
            bg.fill((0, 0, 0))
        screen.blit(bg, (0, 0))

        if self.puzzle_tiles is None:
            self._init_painting_tiles()

        for tile in self.puzzle_tiles:
            screen.blit(tile["image"], tile["rect"])
            if self.selected_tile is tile:
                pygame.draw.rect(screen, (255, 255, 0), tile["rect"], 3)

    def _is_puzzle_solved(self):
        if not self.puzzle_tiles:
            return False
        for tile in self.puzzle_tiles:
            if tile["current_pos"] != tile["correct_pos"]:
                return False
        return True

    # ---------- СЕЙФ С ЗАПИСКОЙ (1234) ----------

    def _draw_note_safe_puzzle(self, screen):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        center_rect = pygame.Rect(
            self.screen_width // 2 - 150,
            self.screen_height // 2 - 125,
            300,
            250,
        )

        safe_img = self._load_scaled(
            "assets/polka_s_seyfom_s_zapiskoy.png", (center_rect.width, center_rect.height)
        )
        screen.blit(safe_img, center_rect.topleft)

        input_width = 160
        input_height = 40
        input_x = self.screen_width // 2 - input_width // 2
        input_y = self.screen_height // 2 + 70
        input_rect = pygame.Rect(input_x, input_y, input_width, input_height)
        pygame.draw.rect(screen, (50, 50, 50), input_rect)
        pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)

        code_display = "*" * len(self.note_safe_code) if self.note_safe_code else "Введите пароль"
        text_surface = self.font_mid.render(code_display, True, (255, 255, 255))
        screen.blit(text_surface, (input_x + 10, input_y + 8))

    # ---------- СЕЙФ С ЦИФРАМИ (567) ----------

    def _draw_symbol_safe_puzzle(self, screen):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        center_rect = pygame.Rect(
            self.screen_width // 2 - 150,
            self.screen_height // 2 - 125,
            300,
            250,
        )

        safe_img = self._load_scaled(
            "assets/polka_s_seyfom_s_simvolami.png", (center_rect.width, center_rect.height)
        )
        screen.blit(safe_img, center_rect.topleft)

        input_width = 120
        input_height = 40
        input_x = self.screen_width // 2 - input_width // 2
        input_y = self.screen_height // 2 + 70
        input_rect = pygame.Rect(input_x, input_y, input_width, input_height)
        pygame.draw.rect(screen, (50, 50, 50), input_rect)
        pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)

        code_display = " ".join(self.symbol_safe_code) if self.symbol_safe_code else "_ _ _"
        text_surface = self.font_mid.render(code_display, True, (255, 255, 255))
        screen.blit(text_surface, (input_x + 10, input_y + 8))

    # ---------- ОБЩЕЕ ДЛЯ ПАЗЛОВ ----------

    def set_puzzle(self, puzzle_type):
        self.current_puzzle = puzzle_type
        if puzzle_type is None:
            self.note_safe_code = ""
            self.symbol_safe_code = []
            self.selected_tile = None
            self.puzzle_tiles = None

    def handle_event(self, event, selected_item, has_all_statues):
        if self.current_puzzle:
            return self._handle_puzzle_event(event)
        return self._handle_room_event(event)

    def _handle_puzzle_event(self, event):
        if self.current_puzzle == "painting":
            return self._handle_painting_puzzle_event(event)
        if self.current_puzzle == "note_safe":
            return self._handle_note_safe_event(event)
        if self.current_puzzle == "symbol_safe":
            return self._handle_symbol_safe_event(event)
        return None

    def _handle_painting_puzzle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos

            if self.puzzle_tiles:
                clicked = None
                for tile in self.puzzle_tiles:
                    if tile["rect"].collidepoint(x, y):
                        clicked = tile
                        break

                if clicked:
                    if self.selected_tile is None:
                        self.selected_tile = clicked
                    else:
                        if self.selected_tile is not clicked:
                            self.selected_tile["current_pos"], clicked["current_pos"] = (
                                clicked["current_pos"],
                                self.selected_tile["current_pos"],
                            )
                            for t in (self.selected_tile, clicked):
                                i, j = t["current_pos"]
                                t["rect"].x = (
                                    self.screen_width // 2 - (5 * 80) // 2 + j * 80
                                )
                                t["rect"].y = (
                                    self.screen_height // 2 - (5 * 80) // 2 + i * 80
                                )
                        self.selected_tile = None

                        if self._is_puzzle_solved():
                            self.painting_completed = True
                            self.set_puzzle(None)
                            return "painting_completed"

        return None

    def _handle_note_safe_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.note_safe_code == "2457":
                    self.note_safe_opened = True
                    self.set_puzzle(None)
                    return "note_safe_opened"
                else:
                    self.note_safe_code = ""
            elif event.key == pygame.K_BACKSPACE:
                self.note_safe_code = self.note_safe_code[:-1]
            elif event.unicode.isdigit() and len(self.note_safe_code) < 4:
                self.note_safe_code += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            center_rect = pygame.Rect(
                self.screen_width // 2 - 150,
                self.screen_height // 2 - 125,
                300,
                250,
            )
            if not center_rect.collidepoint(x, y):
                self.set_puzzle(None)

        return None

    def _handle_symbol_safe_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if "".join(self.symbol_safe_code) == "567":
                    self.symbol_safe_opened = True
                    self.set_puzzle(None)
                    return "symbol_safe_opened"
                else:
                    self.symbol_safe_code = []
            elif event.key == pygame.K_BACKSPACE:
                if self.symbol_safe_code:
                    self.symbol_safe_code.pop()
            elif event.unicode.isdigit() and len(self.symbol_safe_code) < 3:
                self.symbol_safe_code.append(event.unicode)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            center_rect = pygame.Rect(
                self.screen_width // 2 - 150,
                self.screen_height // 2 - 125,
                300,
                250,
            )
            if not center_rect.collidepoint(x, y):
                self.set_puzzle(None)

        return None

    # ---------- ОБЫЧНАЯ КОМНАТА ----------

    def _handle_room_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return None

        x, y = event.pos

        # Стрелки
        left_rect = pygame.Rect(20, self.screen_height // 2 - self.ARROW_SIZE // 2,
                                self.ARROW_SIZE, self.ARROW_SIZE)
        right_rect = pygame.Rect(self.screen_width - 20 - self.ARROW_SIZE,
                                 self.screen_height // 2 - self.ARROW_SIZE // 2,
                                 self.ARROW_SIZE, self.ARROW_SIZE)
        if left_rect.collidepoint(x, y):
            return "prev_room"
        if right_rect.collidepoint(x, y):
            return "next_room"

        # Картина
        painting_rect = pygame.Rect(self.PAINTING_X, self.PAINTING_Y,
                                    self.PAINTING_WIDTH, self.PAINTING_HEIGHT)
        if painting_rect.collidepoint(x, y) and not self.painting_completed:
            self.set_puzzle("painting")
            return None

        # Карта
        if self.painting_completed and not self.map_taken:
            map_rect = pygame.Rect(self.MAP_X, self.MAP_Y, self.MAP_WIDTH, self.MAP_HEIGHT)
            if map_rect.collidepoint(x, y):
                self.map_taken = True
                return "add_karta"

        # Полка с запиской
        note_shelf_rect = pygame.Rect(self.NOTE_SHELF_X, self.NOTE_SHELF_Y,
                                      self.NOTE_SHELF_WIDTH, self.NOTE_SHELF_HEIGHT)
        if note_shelf_rect.collidepoint(x, y):
            if not self.note_safe_opened:
                self.set_puzzle("note_safe")
            else:
                if not self.black_cat_taken:
                    self.black_cat_taken = True
                    return "add_black_cat"
            return None

        # Полка с цифрами (бывшие символы)
        symbol_shelf_rect = pygame.Rect(self.SYMBOL_SHELF_X, self.SYMBOL_SHELF_Y,
                                        self.SYMBOL_SHELF_WIDTH, self.SYMBOL_SHELF_HEIGHT)
        if symbol_shelf_rect.collidepoint(x, y):
            if not self.symbol_safe_opened:
                self.set_puzzle("symbol_safe")
            else:
                if not self.med_cat_taken:
                    self.med_cat_taken = True
                    return "add_med_cat"
            return None

        # Кристаллы
        if not self.kristal1_taken:
            c1_rect = pygame.Rect(self.CRYSTAL1_X, self.CRYSTAL1_Y,
                                  self.CRYSTAL_WIDTH, self.CRYSTAL_HEIGHT)
            if c1_rect.collidepoint(x, y):
                self.kristal1_taken = True
                return "add_kristal1"

        if not self.kristal2_taken:
            c2_rect = pygame.Rect(self.CRYSTAL2_X, self.CRYSTAL2_Y,
                                  self.CRYSTAL_WIDTH, self.CRYSTAL_HEIGHT)
            if c2_rect.collidepoint(x, y):
                self.kristal2_taken = True
                return "add_kristal2"

        return None
