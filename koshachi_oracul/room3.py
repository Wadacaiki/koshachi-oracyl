import pygame
import random
from button import Button, TextInput


class Room3:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background = None
        self.inventory = []
        self.add_to_inventory = None
        self.remove_from_inventory = None
        self.selected_item = None
        self.current_puzzle = None
        self.painting_completed = False
        self.note_safe_opened = False
        self.symbol_safe_opened = False
        self.symbol_safe_code = []
        self.note_safe_code = ""
        self.selected_tile = None
        self.puzzle_tiles = None
        self.load_background()

    def load_background(self):
        try:
            self.background = pygame.image.load("assets/bg_room.png")
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except:
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((70, 50, 30))

    def draw(self, screen, has_all_statues=False):
        screen.blit(self.background, (0, 0))

        # Картина
        try:
            if self.painting_completed:
                painting_img = pygame.image.load("assets/sobrana_kartina.png")
            else:
                painting_img = pygame.image.load("assets/ne_sobrana_kartina.png")
            painting_img = pygame.transform.scale(painting_img, (200, 150))
            screen.blit(painting_img, (self.screen_width - 250, 100))
        except:
            pygame.draw.rect(screen, (100, 100, 100), (self.screen_width - 250, 100, 200, 150))

        # Карта под картиной
        if self.painting_completed and "karta" not in self.inventory:
            try:
                map_img = pygame.image.load("assets/karta.png")
                map_img = pygame.transform.scale(map_img, (80, 60))
                screen.blit(map_img, (self.screen_width - 200, 260))
            except:
                pygame.draw.rect(screen, (150, 150, 200), (self.screen_width - 200, 260, 80, 60))

        # Полка с запиской (верхняя)
        try:
            note_shelf_img = pygame.image.load("assets/polka_s_seyfom_s_zapiskoy.png")
            note_shelf_img = pygame.transform.scale(note_shelf_img, (150, 120))
            screen.blit(note_shelf_img, (100, 150))
        except:
            pygame.draw.rect(screen, (120, 120, 120), (100, 150, 150, 120))

        # Статуэтка кота на полке с запиской
        if self.note_safe_opened and "black_cat" not in self.inventory:
            try:
                cat_img = pygame.image.load("assets/black_cat.png")
                cat_img = pygame.transform.scale(cat_img, (60, 80))
                screen.blit(cat_img, (145, 160))
            except:
                pygame.draw.circle(screen, (0, 0, 0), (175, 200), 25)

        # Полка с символами (нижняя)
        try:
            symbol_shelf_img = pygame.image.load("assets/polka_s_seyfom_s_simvolami.png")
            symbol_shelf_img = pygame.transform.scale(symbol_shelf_img, (150, 120))
            screen.blit(symbol_shelf_img, (100, 300))
        except:
            pygame.draw.rect(screen, (120, 120, 120), (100, 300, 150, 120))

        # Статуэтка кота на полке с символами
        if self.symbol_safe_opened and "med_cat" not in self.inventory:
            try:
                cat_img = pygame.image.load("assets/med_cat.png")
                cat_img = pygame.transform.scale(cat_img, (60, 80))
                screen.blit(cat_img, (145, 310))
            except:
                pygame.draw.circle(screen, (200, 150, 0), (175, 350), 25)

        # Символы на стенах (тусклые)
        symbol_positions = [(400, 50), (600, 80), (800, 60)]
        for i, pos in enumerate(symbol_positions):
            try:
                symbol_img = pygame.image.load(f"assets/simvol{i + 1}.png")
                symbol_img = pygame.transform.scale(symbol_img, (80, 80))
                symbol_img.set_alpha(150)
                screen.blit(symbol_img, pos)
            except:
                pygame.draw.circle(screen, (100, 100, 100), (pos[0] + 40, pos[1] + 40), 30)

        # Кристаллы
        if "kristal1" not in self.inventory:
            try:
                crystal_img = pygame.image.load("assets/kristal1.png")
                crystal_img = pygame.transform.scale(crystal_img, (50, 50))
                screen.blit(crystal_img, (self.screen_width - 400, self.screen_height - 200))
            except:
                pygame.draw.circle(screen, (100, 200, 255), (self.screen_width - 375, self.screen_height - 175), 20)

        if "kristal2" not in self.inventory:
            try:
                crystal_img = pygame.image.load("assets/kristal2.png")
                crystal_img = pygame.transform.scale(crystal_img, (50, 50))
                screen.blit(crystal_img, (self.screen_width - 300, self.screen_height - 150))
            except:
                pygame.draw.circle(screen, (255, 100, 200), (self.screen_width - 275, self.screen_height - 125), 20)

        # Стрелки навигации
        try:
            left_arrow = pygame.image.load("assets/left_strelka.png")
            left_arrow = pygame.transform.scale(left_arrow, (50, 50))
            screen.blit(left_arrow, (20, self.screen_height // 2))
        except:
            pygame.draw.polygon(screen, (255, 255, 255),
                                [(20, self.screen_height // 2), (50, self.screen_height // 2 - 25),
                                 (50, self.screen_height // 2 + 25)])

        try:
            right_arrow = pygame.image.load("assets/right_strelka.png")
            right_arrow = pygame.transform.scale(right_arrow, (50, 50))
            screen.blit(right_arrow, (self.screen_width - 70, self.screen_height // 2))
        except:
            pygame.draw.polygon(screen, (255, 255, 255),
                                [(self.screen_width - 20, self.screen_height // 2),
                                 (self.screen_width - 50, self.screen_height // 2 - 25),
                                 (self.screen_width - 50, self.screen_height // 2 + 25)])

        # Показать головоломки
        if self.current_puzzle == "painting":
            self.draw_painting_puzzle(screen)
        elif self.current_puzzle == "note_safe":
            self.draw_note_safe_puzzle(screen)
        elif self.current_puzzle == "symbol_safe":
            self.draw_symbol_safe_puzzle(screen)

        return None

    def draw_painting_puzzle(self, screen):
        # Используем предоставленный код для пазла
        try:
            background = pygame.image.load("assets/patnashki.png").convert()
            background = pygame.transform.scale(background, (self.screen_width, self.screen_height))
        except:
            background = pygame.Surface((self.screen_width, self.screen_height))
            background.fill((0, 0, 0))

        try:
            cat_image = pygame.image.load("assets/sama_kartina.png").convert_alpha()
            cat_image = pygame.transform.scale(cat_image, (400, 400))
        except:
            cat_image = pygame.Surface((400, 400))
            cat_image.fill((100, 100, 100))

        # Создаем плитки пазла (5x5 вместо 3x3)
        tile_size = 80
        grid_size = 5
        tiles = []

        for i in range(grid_size):
            for j in range(grid_size):
                tile_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
                tile_surface.blit(cat_image, (0, 0), (j * (400 // grid_size), i * (400 // grid_size),
                                                      400 // grid_size, 400 // grid_size))
                tile_surface = pygame.transform.scale(tile_surface, (tile_size, tile_size))

                tiles.append({
                    "image": tile_surface,
                    "correct_pos": (i, j),
                    "current_pos": (i, j),
                    "rect": pygame.Rect(self.screen_width // 2 - (grid_size * tile_size) // 2 + j * tile_size,
                                        self.screen_height // 2 - (grid_size * tile_size) // 2 + i * tile_size,
                                        tile_size, tile_size)
                })

        # Перемешиваем плитки
        if self.puzzle_tiles is None:
            for _ in range(100):
                i1, i2 = random.sample(range(len(tiles)), 2)
                tiles[i1]["current_pos"], tiles[i2]["current_pos"] = tiles[i2]["current_pos"], tiles[i1]["current_pos"]
                pos1 = tiles[i1]["current_pos"]
                pos2 = tiles[i2]["current_pos"]
                tiles[i1]["rect"].x = self.screen_width // 2 - (grid_size * tile_size) // 2 + pos1[1] * tile_size
                tiles[i1]["rect"].y = self.screen_height // 2 - (grid_size * tile_size) // 2 + pos1[0] * tile_size
                tiles[i2]["rect"].x = self.screen_width // 2 - (grid_size * tile_size) // 2 + pos2[1] * tile_size
                tiles[i2]["rect"].y = self.screen_height // 2 - (grid_size * tile_size) // 2 + pos2[0] * tile_size
            self.puzzle_tiles = tiles

        font = pygame.font.SysFont("Arial", 36)
        instruction = font.render("Собери картинку! Кликай по двум плиткам чтобы поменять их местами", True,
                                  (255, 255, 255))

        screen.blit(background, (0, 0))
        screen.blit(instruction, (self.screen_width // 2 - instruction.get_width() // 2, 50))

        # Рисуем плитки
        for tile in self.puzzle_tiles:
            screen.blit(tile["image"], tile["rect"])
            if self.selected_tile == tile:
                pygame.draw.rect(screen, (255, 255, 0), tile["rect"], 3)

        # Кнопка назад
        back_btn = Button(50, self.screen_height - 150, "Назад", lambda: self.set_puzzle(None))
        back_btn.check_hover(pygame.mouse.get_pos())
        back_btn.draw(screen)

    def draw_note_safe_puzzle(self, screen):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        try:
            safe_img = pygame.image.load("assets/polka_s_seyfom_s_zapiskoy.png")
            safe_img = pygame.transform.scale(safe_img, (300, 250))
            screen.blit(safe_img, (self.screen_width // 2 - 150, self.screen_height // 2 - 125))
        except:
            pygame.draw.rect(screen, (100, 100, 100),
                             (self.screen_width // 2 - 150, self.screen_height // 2 - 125, 300, 250))

        # Окошко для ввода
        input_rect = pygame.Rect(self.screen_width // 2 - 80, self.screen_height // 2, 160, 40)
        pygame.draw.rect(screen, (50, 50, 50), input_rect)
        pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)

        font = pygame.font.SysFont("Arial", 24)
        code_display = "*" * len(self.note_safe_code) if self.note_safe_code else "Введите пароль"
        text_surface = font.render(code_display, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 8))

        # Кнопка назад
        back_btn = Button(self.screen_width // 2 - 50, self.screen_height // 2 + 100, "Назад",
                          lambda: self.set_puzzle(None))
        back_btn.check_hover(pygame.mouse.get_pos())
        back_btn.draw(screen)

    def draw_symbol_safe_puzzle(self, screen):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        try:
            safe_img = pygame.image.load("assets/polka_s_seyfom_s_simvolami.png")
            safe_img = pygame.transform.scale(safe_img, (300, 250))
            screen.blit(safe_img, (self.screen_width // 2 - 150, self.screen_height // 2 - 125))
        except:
            pygame.draw.rect(screen, (100, 100, 100),
                             (self.screen_width // 2 - 150, self.screen_height // 2 - 125, 300, 250))

        # Окошко для ввода
        input_rect = pygame.Rect(self.screen_width // 2 - 60, self.screen_height // 2, 120, 40)
        pygame.draw.rect(screen, (50, 50, 50), input_rect)
        pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)

        font = pygame.font.SysFont("Arial", 24)
        code_display = " ".join(self.symbol_safe_code) if self.symbol_safe_code else "_ _ _"
        text_surface = font.render(code_display, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 8))

        # Кнопка назад
        back_btn = Button(self.screen_width // 2 - 50, self.screen_height // 2 + 100, "Назад",
                          lambda: self.set_puzzle(None))
        back_btn.check_hover(pygame.mouse.get_pos())
        back_btn.draw(screen)

    def set_puzzle(self, puzzle_type):
        self.current_puzzle = puzzle_type
        if puzzle_type is None:
            self.symbol_safe_code = []
            self.note_safe_code = ""
            self.selected_tile = None
            self.puzzle_tiles = None

    def handle_event(self, event, has_all_statues=False):
        if self.current_puzzle:
            return self.handle_puzzle_event(event)
        else:
            return self.handle_room_event(event, has_all_statues)

    def handle_puzzle_event(self, event):
        if self.current_puzzle == "painting":
            return self.handle_painting_puzzle(event)
        elif self.current_puzzle == "note_safe":
            return self.handle_note_safe_puzzle(event)
        elif self.current_puzzle == "symbol_safe":
            return self.handle_symbol_safe_puzzle(event)
        return None

    def handle_painting_puzzle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Кнопка назад
            back_btn = Button(50, self.screen_height - 150, "Назад", lambda: self.set_puzzle(None))
            if back_btn.rect.collidepoint(x, y):
                self.set_puzzle(None)
                return None

            # Проверяем клик по плиткам
            if self.puzzle_tiles:
                clicked_tile = None
                for tile in self.puzzle_tiles:
                    if tile["rect"].collidepoint(x, y):
                        clicked_tile = tile
                        break

                if clicked_tile:
                    if self.selected_tile is None:
                        self.selected_tile = clicked_tile
                    else:
                        # Меняем плитки местами
                        self.selected_tile["current_pos"], clicked_tile["current_pos"] = \
                            clicked_tile["current_pos"], self.selected_tile["current_pos"]

                        # Обновляем позиции
                        pos1 = self.selected_tile["current_pos"]
                        pos2 = clicked_tile["current_pos"]

                        self.selected_tile["rect"].x = self.screen_width // 2 - (5 * 80) // 2 + pos1[1] * 80
                        self.selected_tile["rect"].y = self.screen_height // 2 - (5 * 80) // 2 + pos1[0] * 80
                        clicked_tile["rect"].x = self.screen_width // 2 - (5 * 80) // 2 + pos2[1] * 80
                        clicked_tile["rect"].y = self.screen_height // 2 - (5 * 80) // 2 + pos2[0] * 80

                        self.selected_tile = None

                        # Проверяем решение
                        if self.is_puzzle_solved():
                            self.painting_completed = True
                            self.set_puzzle(None)
                            return "painting_completed"

        return None

    def handle_note_safe_puzzle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.note_safe_code == "1234":
                    self.note_safe_opened = True
                    if "zapiska" in self.inventory and self.remove_from_inventory:
                        self.remove_from_inventory("zapiska")
                    self.set_puzzle(None)
                    return "note_safe_opened"
                else:
                    self.note_safe_code = ""
            elif event.key == pygame.K_BACKSPACE:
                self.note_safe_code = self.note_safe_code[:-1]
            elif event.unicode.isdigit() and len(self.note_safe_code) < 4:
                self.note_safe_code += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            back_btn = Button(self.screen_width // 2 - 50, self.screen_height // 2 + 100, "Назад",
                              lambda: self.set_puzzle(None))
            if back_btn.rect.collidepoint(event.pos):
                self.set_puzzle(None)

        return None

    def handle_symbol_safe_puzzle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if "".join(self.symbol_safe_code) == "567":
                    self.symbol_safe_opened = True
                    self.set_puzzle(None)
                    return "symbol_safe_opened"
                else:
                    self.symbol_safe_code = []
            elif event.key == pygame.K_BACKSPACE:
                self.symbol_safe_code = self.symbol_safe_code[:-1] if self.symbol_safe_code else []
            elif event.unicode.isdigit() and len(self.symbol_safe_code) < 3:
                self.symbol_safe_code.append(event.unicode)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            back_btn = Button(self.screen_width // 2 - 50, self.screen_height // 2 + 100, "Назад",
                              lambda: self.set_puzzle(None))
            if back_btn.rect.collidepoint(event.pos):
                self.set_puzzle(None)

        return None

    def is_puzzle_solved(self):
        if not self.puzzle_tiles:
            return False
        for tile in self.puzzle_tiles:
            if tile["current_pos"] != tile["correct_pos"]:
                return False
        return True

    def handle_room_event(self, event, has_all_statues=False):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Стрелки навигации
            if 20 <= x <= 70 and self.screen_height // 2 - 25 <= y <= self.screen_height // 2 + 25:
                return "prev_room"
            if self.screen_width - 70 <= x <= self.screen_width - 20 and self.screen_height // 2 - 25 <= y <= self.screen_height // 2 + 25:
                return "next_room"

            # Картина
            painting_rect = pygame.Rect(self.screen_width - 250, 100, 200, 150)
            if painting_rect.collidepoint(x, y) and not self.painting_completed:
                self.set_puzzle("painting")
                return None

            # Карта под картиной
            if self.painting_completed and "karta" not in self.inventory:
                map_rect = pygame.Rect(self.screen_width - 200, 260, 80, 60)
                if map_rect.collidepoint(x, y):
                    if self.add_to_inventory:
                        self.add_to_inventory("karta")
                    return "add_karta"

            # Полка с запиской
            note_shelf_rect = pygame.Rect(100, 150, 150, 120)
            if note_shelf_rect.collidepoint(x, y):
                if not self.note_safe_opened:
                    self.set_puzzle("note_safe")
                elif "black_cat" not in self.inventory:
                    if self.add_to_inventory:
                        self.add_to_inventory("black_cat")
                    return "add_black_cat"
                return None

            # Полка с символами
            symbol_shelf_rect = pygame.Rect(100, 300, 150, 120)
            if symbol_shelf_rect.collidepoint(x, y):
                if not self.symbol_safe_opened:
                    self.set_puzzle("symbol_safe")
                elif "med_cat" not in self.inventory:
                    if self.add_to_inventory:
                        self.add_to_inventory("med_cat")
                    return "add_med_cat"
                return None

            # Кристаллы
            if "kristal1" not in self.inventory:
                crystal1_rect = pygame.Rect(self.screen_width - 400, self.screen_height - 200, 50, 50)
                if crystal1_rect.collidepoint(x, y):
                    if self.add_to_inventory:
                        self.add_to_inventory("kristal1")
                    return "add_kristal1"

            if "kristal2" not in self.inventory:
                crystal2_rect = pygame.Rect(self.screen_width - 300, self.screen_height - 150, 50, 50)
                if crystal2_rect.collidepoint(x, y):
                    if self.add_to_inventory:
                        self.add_to_inventory("kristal2")
                    return "add_kristal2"

        return None