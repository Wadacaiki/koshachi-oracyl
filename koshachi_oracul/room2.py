import pygame


class Room2:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Шкаф
        self.CLOSET_WIDTH = 1300
        self.CLOSET_HEIGHT = 1000
        self.CLOSET_X = -350
        self.CLOSET_Y = self.screen_height - 900

        # Полка с кристаллами
        self.CRYSTAL_SHELF_WIDTH = 250
        self.CRYSTAL_SHELF_HEIGHT = 180
        self.CRYSTAL_SHELF_X = self.CLOSET_X + 535
        self.CRYSTAL_SHELF_Y = self.CLOSET_Y + 300

        # Полка со свитками
        self.SCROLL_SHELF_WIDTH = 250
        self.SCROLL_SHELF_HEIGHT = 20
        self.SCROLL_SHELF_X = self.CLOSET_X + 535
        self.SCROLL_SHELF_Y = self.CLOSET_Y + 650

        # NPC-кот
        self.CAT_WIDTH = 200
        self.CAT_HEIGHT = 300
        self.CAT_X = self.screen_width - 250
        self.CAT_Y = self.screen_height - 300

        # Символы над NPC (5,6,7 в ряд)
        self.SYMBOL_WIDTH = 80
        self.SYMBOL_HEIGHT = 80
        base_symbol_x = self.CAT_X - 240
        symbols_y = self.CAT_Y - 220
        self.SYMBOL_POSITIONS = [
            (base_symbol_x, symbols_y),
            (base_symbol_x + 150, symbols_y),
            (base_symbol_x + 250, symbols_y),
        ]
        self.symbol_hint_active = False
        self.symbol_hint_value = None

        # Ключ от NPC
        self.KEY_NPC_WIDTH = 60
        self.KEY_NPC_HEIGHT = 30
        self.KEY_NPC_X = self.CAT_X + 40
        self.KEY_NPC_Y = self.CAT_Y - 40

        self.ARROW_SIZE = 50

        self.current_puzzle = None
        self.crystals_on_shelf = 0
        self.crystal_puzzle_solved = False
        self.scroll_puzzle_solved = False

        self.svitok3_taken = False
        self.anibus_key_taken = False
        self.key_from_npc_taken = False

        self.npc_has_map = False
        self.show_dialog = False

        self.scroll_tiles = []
        self.scroll_selected = None

        self.background = self._load_scaled("assets/bg_room.png",
                                            (self.screen_width, self.screen_height))
        self.closet_img = self._load_scaled("assets/hkaf.png",
                                            (self.CLOSET_WIDTH, self.CLOSET_HEIGHT))
        self.crystal_shelf_small = self._load_scaled("assets/polka_kristal.png",
                                                     (self.CRYSTAL_SHELF_WIDTH, self.CRYSTAL_SHELF_HEIGHT))
        self.scroll_shelf_small = self._load_scaled("assets/polka_svitok.png",
                                                    (self.SCROLL_SHELF_WIDTH, self.SCROLL_SHELF_HEIGHT))

        self.crystal_shelf_big_1 = self._load_scaled("assets/polka_kristal.png", (400, 200))
        self.crystal_shelf_big_2 = self._load_scaled("assets/polka_kristal_2.png", (400, 200))
        self.crystal_shelf_big_3 = self._load_scaled("assets/polka_kristal_3.png", (400, 200))
        self.scroll_shelf_big = self._load_scaled("assets/polka_svitok.png", (450, 100))

        self.cat_npc_img = self._load_scaled("assets/cat_npc.png", (self.CAT_WIDTH, self.CAT_HEIGHT))
        self.dialog_img = self._load_scaled("assets/dialog.png", (250, 150))

        self.svitok3_img = self._load_scaled("assets/svitok3.png", (50, 80))
        self.key_anibus_img = self._load_scaled("assets/anibus_key.png", (60, 30))
        self.key_from_npc_img = self._load_scaled("assets/key_from_npc.png", (60, 30))

        self.svitok_imgs = {
            "svitok1": self._load_scaled("assets/svitok1.png", (80, 90)),
            "svitok2": self._load_scaled("assets/svitok2.png", (80, 100)),
            "svitok3": self._load_scaled("assets/svitok3.png", (80, 110)),
            "svitok4": self._load_scaled("assets/svitok4.png", (80, 120)),
            "svitok5": self._load_scaled("assets/svitok5.png", (80, 130)),
        }

        self.left_arrow_img = self._load_scaled("assets/left_strelka.png",
                                                (self.ARROW_SIZE, self.ARROW_SIZE))
        self.right_arrow_img = self._load_scaled("assets/right_strelka.png",
                                                 (self.ARROW_SIZE, self.ARROW_SIZE))

        self.font = pygame.font.SysFont("Arial", 18)

    def _load_scaled(self, path, size):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        except:
            surf = pygame.Surface(size, pygame.SRCALPHA)
            surf.fill((80, 80, 80))
            return surf

    # ---------- РИСОВАНИЕ ----------

    def draw(self, screen, has_all_statues):
        screen.blit(self.background, (0, 0))
        screen.blit(self.closet_img, (self.CLOSET_X, self.CLOSET_Y))
        screen.blit(self.crystal_shelf_small, (self.CRYSTAL_SHELF_X, self.CRYSTAL_SHELF_Y))
        screen.blit(self.scroll_shelf_small, (self.SCROLL_SHELF_X, self.SCROLL_SHELF_Y))

        if self.crystal_puzzle_solved and not self.svitok3_taken:
            sv_x = self.CRYSTAL_SHELF_X + 60
            sv_y = self.CRYSTAL_SHELF_Y + self.CRYSTAL_SHELF_HEIGHT + 10
            screen.blit(self.svitok3_img, (sv_x, sv_y))

        if self.scroll_puzzle_solved and not self.anibus_key_taken:
            key_x = self.SCROLL_SHELF_X + 70
            key_y = self.SCROLL_SHELF_Y + self.SCROLL_SHELF_HEIGHT + 10
            screen.blit(self.key_anibus_img, (key_x, key_y))

        screen.blit(self.cat_npc_img, (self.CAT_X, self.CAT_Y))

        if not self.npc_has_map and self.show_dialog:
            dialog_x = self.CAT_X - 200
            dialog_y = self.CAT_Y - 80
            screen.blit(self.dialog_img, (dialog_x, dialog_y))

        if self.npc_has_map and not self.key_from_npc_taken:
            screen.blit(self.key_from_npc_img, (self.KEY_NPC_X, self.KEY_NPC_Y))

        # Символы (5,6,7) над котом
        for i, (sx, sy) in enumerate(self.SYMBOL_POSITIONS):
            try:
                symbol_img = pygame.image.load(f"assets/simvol{i + 1}.png").convert_alpha()
                symbol_img = pygame.transform.scale(symbol_img,
                                                    (self.SYMBOL_WIDTH, self.SYMBOL_HEIGHT))
                symbol_img.set_alpha(150)
            except:
                symbol_img = pygame.Surface((self.SYMBOL_WIDTH, self.SYMBOL_HEIGHT), pygame.SRCALPHA)
                pygame.draw.circle(
                    symbol_img,
                    (100, 100, 100),
                    (self.SYMBOL_WIDTH // 2, self.SYMBOL_HEIGHT // 2),
                    self.SYMBOL_WIDTH // 2,
                )
            screen.blit(symbol_img, (sx, sy))

        # Подсказка при клике на символ
        if self.symbol_hint_active and self.symbol_hint_value is not None:
            overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))
            font_big = pygame.font.SysFont("Arial", 72)
            text_surface = font_big.render(self.symbol_hint_value, True, (255, 255, 255))
            screen.blit(
                text_surface,
                (
                    self.screen_width // 2 - text_surface.get_width() // 2,
                    self.screen_height // 2 - text_surface.get_height() // 2,
                ),
            )

        self._draw_arrows(screen)

        if self.current_puzzle == "crystal_shelf":
            self._draw_crystal_shelf_puzzle(screen)
        elif self.current_puzzle == "scroll_shelf":
            self._draw_scroll_shelf_puzzle(screen)

        return None

    def _draw_arrows(self, screen):
        left_x = 20
        left_y = self.screen_height // 2 - self.ARROW_SIZE // 2
        right_x = self.screen_width - 20 - self.ARROW_SIZE
        right_y = left_y
        screen.blit(self.left_arrow_img, (left_x, left_y))
        screen.blit(self.right_arrow_img, (right_x, right_y))

    def _draw_crystal_shelf_puzzle(self, screen):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        center_rect = pygame.Rect(
            self.screen_width // 2 - 200,
            self.screen_height // 2 - 100,
            400,
            200,
        )

        if self.crystals_on_shelf == 0:
            shelf_img = self.crystal_shelf_big_1
        elif self.crystals_on_shelf == 1:
            shelf_img = self.crystal_shelf_big_2
        else:
            shelf_img = self.crystal_shelf_big_3

        screen.blit(shelf_img, center_rect.topleft)

    # ---------- СВИТКИ НА БОЛЬШОЙ ПОЛКЕ ----------

    def _ensure_scroll_tiles(self):
        if self.scroll_tiles:
            return

        scroll_defs = [
            ("svitok4", 4),
            ("svitok2", 2),
            ("svitok1", 1),
            ("svitok5", 5),
        ]

        base_x = self.screen_width // 2 - 200
        base_y = self.screen_height // 2 - 40
        width = 60
        spacing = 10

        for i, (name, height) in enumerate(scroll_defs):
            rect = pygame.Rect(
                base_x + i * (width + spacing),
                base_y - height * 7,
                width,
                130,
            )
            self.scroll_tiles.append({"name": name, "height": height, "rect": rect})

    def _draw_scroll_shelf_puzzle(self, screen):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        center_rect = pygame.Rect(
            self.screen_width // 2 - 250,
            self.screen_height // 2 - 5,
            450,
            100,
        )
        screen.blit(self.scroll_shelf_big, center_rect.topleft)

        self._ensure_scroll_tiles()

        for tile in self.scroll_tiles:
            name = tile["name"]
            img = self.svitok_imgs.get(name)
            if img:
                if self.scroll_selected is tile:
                    pygame.draw.rect(screen, (255, 255, 0), tile["rect"], 3)
                screen.blit(img, (tile["rect"].x, tile["rect"].y))

    def _check_scroll_order(self):
        heights = [tile["height"] for tile in self.scroll_tiles]
        return heights == sorted(heights)

    # ---------- ОБЩИЙ СВИЧ ----------

    def set_puzzle(self, puzzle_type):
        self.current_puzzle = puzzle_type
        if puzzle_type is None:
            self.scroll_selected = None

    def handle_event(self, event, selected_item, has_all_statues):
        if self.current_puzzle:
            return self._handle_puzzle_event(event, selected_item)
        return self._handle_room_event(event, selected_item)

    def _handle_puzzle_event(self, event, selected_item):
        if self.current_puzzle == "crystal_shelf":
            return self._handle_crystal_shelf_event(event, selected_item)
        if self.current_puzzle == "scroll_shelf":
            return self._handle_scroll_shelf_event(event, selected_item)
        return None

    def _handle_crystal_shelf_event(self, event, selected_item):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            center_rect = pygame.Rect(
                self.screen_width // 2 - 200,
                self.screen_height // 2 - 100,
                400,
                200,
            )

            if not center_rect.collidepoint(x, y):
                self.set_puzzle(None)
                return None

            if center_rect.collidepoint(x, y):
                if selected_item in ("kristal1", "kristal2") and self.crystals_on_shelf < 2:
                    self.crystals_on_shelf += 1
                    return f"remove_{selected_item}"

                if self.crystals_on_shelf >= 2 and not self.crystal_puzzle_solved:
                    self.crystal_puzzle_solved = True
                    self.set_puzzle(None)

        return None

    def _handle_scroll_shelf_event(self, event, selected_item):
        center_rect = pygame.Rect(
            self.screen_width // 2 - 250,
            self.screen_height // 2 - 125,
            500,
            250,
        )

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos

            if not center_rect.collidepoint(x, y):
                self.set_puzzle(None)
                return None

            if selected_item == "svitok3":
                base_x = self.screen_width // 2 - 200
                base_y = self.screen_height // 2 - 40
                width = 60
                spacing = 10
                idx = len(self.scroll_tiles)
                height = 3
                rect = pygame.Rect(
                    base_x + idx * (width + spacing),
                    base_y - height * 7,
                    width,
                    130,
                )
                self.scroll_tiles.append({"name": "svitok3", "height": height, "rect": rect})
                return "remove_svitok3"

            for tile in self.scroll_tiles:
                if tile["rect"].collidepoint(x, y):
                    if self.scroll_selected is None:
                        self.scroll_selected = tile
                    else:
                        if self.scroll_selected is not tile:
                            self.scroll_selected["height"], tile["height"] = (
                                tile["height"],
                                self.scroll_selected["height"],
                            )
                            self.scroll_selected["name"], tile["name"] = (
                                tile["name"],
                                self.scroll_selected["name"],
                            )
                        self.scroll_selected = None

                        if self._check_scroll_order():
                            self.scroll_puzzle_solved = True
                            self.set_puzzle(None)
                            return "scroll_puzzle_solved"
                    return None

        return None

    # ---------- ОБЫЧНАЯ КОМНАТА ----------

    def _handle_room_event(self, event, selected_item):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return None

        x, y = event.pos

        # Если сейчас показывается подсказка по символу — любой клик её закрывает
        if self.symbol_hint_active:
            self.symbol_hint_active = False
            self.symbol_hint_value = None
            return None

        # Клик по символам над котом -> показать цифры 5/6/7
        for i, (sx, sy) in enumerate(self.SYMBOL_POSITIONS):
            symbol_rect = pygame.Rect(sx, sy, self.SYMBOL_WIDTH, self.SYMBOL_HEIGHT)
            if symbol_rect.collidepoint(x, y):
                mapping = ["5", "6", "7"]
                self.symbol_hint_value = mapping[i]
                self.symbol_hint_active = True
                return None

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

        # Полка с кристаллами
        crystal_shelf_rect = pygame.Rect(
            self.CRYSTAL_SHELF_X,
            self.CRYSTAL_SHELF_Y,
            self.CRYSTAL_SHELF_WIDTH,
            self.CRYSTAL_SHELF_HEIGHT,
        )
        if crystal_shelf_rect.collidepoint(x, y):
            self.set_puzzle("crystal_shelf")
            return None

        # Свиток3 под полкой
        if self.crystal_puzzle_solved and not self.svitok3_taken:
            sv_x = self.CRYSTAL_SHELF_X + 60
            sv_y = self.CRYSTAL_SHELF_Y + self.CRYSTAL_SHELF_HEIGHT + 10
            sv_rect = pygame.Rect(sv_x, sv_y, 50, 80)
            if sv_rect.collidepoint(x, y):
                self.svitok3_taken = True
                return "add_svitok3"

        # Полка со свитками
        scroll_shelf_rect = pygame.Rect(
            self.SCROLL_SHELF_X,
            self.SCROLL_SHELF_Y,
            self.SCROLL_SHELF_WIDTH,
            self.SCROLL_SHELF_HEIGHT,
        )
        if scroll_shelf_rect.collidepoint(x, y):
            self.set_puzzle("scroll_shelf")
            return None

        # Ключ анибуса под полкой
        if self.scroll_puzzle_solved and not self.anibus_key_taken:
            key_x = self.SCROLL_SHELF_X + 70
            key_y = self.SCROLL_SHELF_Y + self.SCROLL_SHELF_HEIGHT + 10
            key_rect = pygame.Rect(key_x, key_y, self.KEY_NPC_WIDTH, self.KEY_NPC_HEIGHT)
            if key_rect.collidepoint(x, y):
                self.anibus_key_taken = True
                return "add_anibus_key"

        # NPC кот
        cat_rect = pygame.Rect(self.CAT_X, self.CAT_Y, self.CAT_WIDTH, self.CAT_HEIGHT)
        if cat_rect.collidepoint(x, y):
            if selected_item == "karta" and not self.npc_has_map:
                self.npc_has_map = True
                self.show_dialog = False
                return "remove_karta"
            else:
                if not self.npc_has_map:
                    self.show_dialog = True
            return None

        # Ключ от NPC
        if self.npc_has_map and not self.key_from_npc_taken:
            key_rect = pygame.Rect(
                self.KEY_NPC_X, self.KEY_NPC_Y, self.KEY_NPC_WIDTH, self.KEY_NPC_HEIGHT
            )
            if key_rect.collidepoint(x, y):
                self.key_from_npc_taken = True
                return "add_key_from_npc"

        return None
