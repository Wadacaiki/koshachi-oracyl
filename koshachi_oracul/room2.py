import pygame
from button import Button


class Room2:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background = None
        self.inventory = []
        self.add_to_inventory = None
        self.remove_from_inventory = None
        self.selected_item = None
        self.current_puzzle = None
        self.crystal_shelf_state = 0
        self.scrolls_placed = [False, False, False, False, False]
        self.scrolls_order = [1, 2, 3, 4, 5]
        self.npc_interacted = False
        self.npc_key_available = False
        self.selected_scroll = None
        self.load_background()

    def load_background(self):
        try:
            self.background = pygame.image.load("assets/bg_room.png")
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except:
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((80, 60, 40))

    def draw(self, screen, has_all_statues=False):
        screen.blit(self.background, (0, 0))

        # Шкаф
        try:
            closet_img = pygame.image.load("assets/hkaf.png")
            closet_img = pygame.transform.scale(closet_img, (300, 400))
            screen.blit(closet_img, (100, self.screen_height - 450))
        except:
            pygame.draw.rect(screen, (100, 70, 30), (100, self.screen_height - 450, 300, 400))

        # Полка с кристаллами (на шкафу)
        try:
            if self.crystal_shelf_state == 0:
                crystal_img = pygame.image.load("assets/polka_kristal.png")
            elif self.crystal_shelf_state == 1:
                crystal_img = pygame.image.load("assets/polka_kristal_2.png")
            else:
                crystal_img = pygame.image.load("assets/polka_kristal_3.png")
            crystal_img = pygame.transform.scale(crystal_img, (120, 100))
            screen.blit(crystal_img, (150, self.screen_height - 400))
        except:
            pygame.draw.rect(screen, (150, 150, 150), (150, self.screen_height - 400, 120, 100))

        # Свиток под полкой (после решения)
        if self.crystal_shelf_state >= 2 and "svitok3" not in self.inventory:
            try:
                scroll_img = pygame.image.load("assets/svitok3.png")
                scroll_img = pygame.transform.scale(scroll_img, (40, 60))
                screen.blit(scroll_img, (170, self.screen_height - 300))
            except:
                pygame.draw.rect(screen, (200, 200, 150), (170, self.screen_height - 300, 40, 60))

        # Полка со свитками (на шкафу, выше)
        try:
            scroll_shelf_img = pygame.image.load("assets/polka_svitok.png")
            scroll_shelf_img = pygame.transform.scale(scroll_shelf_img, (120, 100))
            screen.blit(scroll_shelf_img, (150, self.screen_height - 500))
        except:
            pygame.draw.rect(screen, (150, 150, 150), (150, self.screen_height - 500, 120, 100))

        # Свитки на полке (если размещены)
        scroll_positions = [(160, self.screen_height - 490), (180, self.screen_height - 480),
                            (200, self.screen_height - 470), (220, self.screen_height - 460),
                            (240, self.screen_height - 450)]

        for i, pos in enumerate(scroll_positions):
            if self.scrolls_placed[i]:
                try:
                    height = 60 - i * 5
                    pygame.draw.rect(screen, (200, 200, 150), (pos[0], pos[1], 30, height))
                except:
                    pass

        # Ключ под полкой со свитками (после решения)
        if all(self.scrolls_placed) and self.is_scrolls_correct() and "anibus_key" not in self.inventory:
            try:
                key_img = pygame.image.load("assets/anibus_key.png")
                key_img = pygame.transform.scale(key_img, (60, 30))
                screen.blit(key_img, (170, self.screen_height - 400))
            except:
                pygame.draw.rect(screen, (200, 200, 0), (170, self.screen_height - 400, 60, 30))

        # NPC кот
        try:
            cat_img = pygame.image.load("assets/cat_npc.png")
            cat_img = pygame.transform.scale(cat_img, (150, 200))
            screen.blit(cat_img, (self.screen_width - 250, self.screen_height - 300))
        except:
            pygame.draw.circle(screen, (150, 150, 150), (self.screen_width - 175, self.screen_height - 200), 50)

        # Диалоговое облако
        if self.npc_interacted and not self.npc_key_available:
            try:
                dialog_img = pygame.image.load("assets/dialog.png")
                dialog_img = pygame.transform.scale(dialog_img, (200, 100))
                screen.blit(dialog_img, (self.screen_width - 400, self.screen_height - 350))

                font = pygame.font.SysFont("Arial", 16)
                text = font.render("Принеси мне карту!", True, (0, 0, 0))
                screen.blit(text, (self.screen_width - 390, self.screen_height - 320))
            except:
                pygame.draw.ellipse(screen, (255, 255, 255),
                                    (self.screen_width - 400, self.screen_height - 350, 200, 100))
                font = pygame.font.SysFont("Arial", 16)
                text = font.render("Принеси мне карту!", True, (0, 0, 0))
                screen.blit(text, (self.screen_width - 390, self.screen_height - 320))

        # Ключ от NPC (после получения карты)
        if self.npc_key_available and "key_from_npc" not in self.inventory:
            try:
                key_img = pygame.image.load("assets/key_from_npc.png")
                key_img = pygame.transform.scale(key_img, (60, 30))
                screen.blit(key_img, (self.screen_width - 200, self.screen_height - 350))
            except:
                pygame.draw.rect(screen, (200, 100, 0), (self.screen_width - 200, self.screen_height - 350, 60, 30))

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

        # Показать увеличенные полки
        if self.current_puzzle == "crystal_shelf":
            self.draw_crystal_shelf_puzzle(screen)
        elif self.current_puzzle == "scroll_shelf":
            self.draw_scroll_shelf_puzzle(screen)

        return None

    def draw_crystal_shelf_puzzle(self, screen):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        try:
            if self.crystal_shelf_state == 0:
                shelf_img = pygame.image.load("assets/polka_kristal.png")
            elif self.crystal_shelf_state == 1:
                shelf_img = pygame.image.load("assets/polka_kristal_2.png")
            else:
                shelf_img = pygame.image.load("assets/polka_kristal_3.png")
            shelf_img = pygame.transform.scale(shelf_img, (300, 250))
            screen.blit(shelf_img, (self.screen_width // 2 - 150, self.screen_height // 2 - 125))
        except:
            pygame.draw.rect(screen, (150, 150, 150),
                             (self.screen_width // 2 - 150, self.screen_height // 2 - 125, 300, 250))

        # Кнопка назад
        back_btn = Button(self.screen_width // 2 - 50, self.screen_height // 2 + 150, "Назад",
                          lambda: self.set_puzzle(None))
        back_btn.check_hover(pygame.mouse.get_pos())
        back_btn.draw(screen)

    def draw_scroll_shelf_puzzle(self, screen):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        try:
            shelf_img = pygame.image.load("assets/polka_svitok.png")
            shelf_img = pygame.transform.scale(shelf_img, (400, 200))
            screen.blit(shelf_img, (self.screen_width // 2 - 200, self.screen_height // 2 - 100))
        except:
            pygame.draw.rect(screen, (150, 150, 150),
                             (self.screen_width // 2 - 200, self.screen_height // 2 - 100, 400, 200))

        # Существующие свитки на полке (4 штуки)
        scroll_width = 60
        scroll_spacing = 70
        start_x = self.screen_width // 2 - 180

        for i in range(5):
            if i < 4:  # Первые 4 свитка уже на полке
                try:
                    scroll_img = pygame.image.load(f"assets/svitok{[1, 2, 4, 5][i]}.png")
                    scroll_height = 80 + ([1, 2, 4, 5][i] - 1) * 10
                    scroll_img = pygame.transform.scale(scroll_img, (scroll_width, scroll_height))
                    screen.blit(scroll_img, (start_x + i * scroll_spacing, self.screen_height // 2 - 50))
                except:
                    height = 80 + ([1, 2, 4, 5][i] - 1) * 10
                    pygame.draw.rect(screen, (200, 200, 150),
                                     (start_x + i * scroll_spacing, self.screen_height // 2 - 50, scroll_width, height))

        # Инструкция
        font = pygame.font.SysFont("Arial", 24)
        instruction = font.render("Расставьте свитки по возрастанию (кликайте для замены)", True, (255, 255, 255))
        screen.blit(instruction, (self.screen_width // 2 - instruction.get_width() // 2, self.screen_height // 2 - 150))

        # Кнопка назад
        back_btn = Button(self.screen_width // 2 - 50, self.screen_height // 2 + 120, "Назад",
                          lambda: self.set_puzzle(None))
        back_btn.check_hover(pygame.mouse.get_pos())
        back_btn.draw(screen)

    def set_puzzle(self, puzzle_type):
        self.current_puzzle = puzzle_type
        if puzzle_type is None:
            self.selected_scroll = None

    def is_scrolls_correct(self):
        return self.scrolls_order == [1, 2, 3, 4, 5]

    def handle_event(self, event, has_all_statues=False):
        if self.current_puzzle:
            return self.handle_puzzle_event(event)
        else:
            return self.handle_room_event(event, has_all_statues)

    def handle_puzzle_event(self, event):
        if self.current_puzzle == "crystal_shelf":
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Проверяем использование кристаллов
                if self.selected_item == "kristal1" and self.crystal_shelf_state == 0:
                    self.crystal_shelf_state = 1
                    if self.remove_from_inventory:
                        self.remove_from_inventory("kristal1")
                    return "remove_kristal1"
                elif self.selected_item == "kristal2" and self.crystal_shelf_state == 1:
                    self.crystal_shelf_state = 2
                    if self.remove_from_inventory:
                        self.remove_from_inventory("kristal2")
                    self.set_puzzle(None)
                    return "remove_kristal2"

                # Кнопка назад
                back_btn = Button(self.screen_width // 2 - 50, self.screen_height // 2 + 150, "Назад",
                                  lambda: self.set_puzzle(None))
                if back_btn.rect.collidepoint(event.pos):
                    self.set_puzzle(None)

        elif self.current_puzzle == "scroll_shelf":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Проверяем клик по свиткам
                scroll_width = 60
                scroll_spacing = 70
                start_x = self.screen_width // 2 - 180

                clicked_index = None
                for i in range(5):
                    scroll_rect = pygame.Rect(start_x + i * scroll_spacing, self.screen_height // 2 - 50, scroll_width,
                                              100)
                    if scroll_rect.collidepoint(x, y) and self.scrolls_placed[i]:
                        clicked_index = i
                        break

                if clicked_index is not None:
                    if self.selected_scroll is None:
                        self.selected_scroll = clicked_index
                    else:
                        # Меняем свитки местами
                        self.scrolls_order[self.selected_scroll], self.scrolls_order[clicked_index] = \
                            self.scrolls_order[clicked_index], self.scrolls_order[self.selected_scroll]
                        self.selected_scroll = None

                        # Проверяем правильность решения
                        if self.is_scrolls_correct():
                            self.set_puzzle(None)

                # Кнопка назад
                back_btn = Button(self.screen_width // 2 - 50, self.screen_height // 2 + 120, "Назад",
                                  lambda: self.set_puzzle(None))
                if back_btn.rect.collidepoint(event.pos):
                    self.set_puzzle(None)
                    self.selected_scroll = None

        return None

    def handle_room_event(self, event, has_all_statues=False):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Стрелки навигации
            if 20 <= x <= 70 and self.screen_height // 2 - 25 <= y <= self.screen_height // 2 + 25:
                return "prev_room"
            if self.screen_width - 70 <= x <= self.screen_width - 20 and self.screen_height // 2 - 25 <= y <= self.screen_height // 2 + 25:
                return "next_room"

            # Полка с кристаллами
            crystal_rect = pygame.Rect(150, self.screen_height - 400, 120, 100)
            if crystal_rect.collidepoint(x, y):
                self.set_puzzle("crystal_shelf")
                return None

            # Свиток под полкой с кристаллами
            if self.crystal_shelf_state >= 2 and "svitok3" not in self.inventory:
                scroll_rect = pygame.Rect(170, self.screen_height - 300, 40, 60)
                if scroll_rect.collidepoint(x, y):
                    if self.add_to_inventory:
                        self.add_to_inventory("svitok3")
                    return "add_svitok3"

            # Полка со свитками
            scroll_shelf_rect = pygame.Rect(150, self.screen_height - 500, 120, 100)
            if scroll_shelf_rect.collidepoint(x, y):
                if self.selected_item == "svitok3" and not all(self.scrolls_placed):
                    # Размещаем свиток
                    for i in range(len(self.scrolls_placed)):
                        if not self.scrolls_placed[i]:
                            self.scrolls_placed[i] = True
                            if self.remove_from_inventory:
                                self.remove_from_inventory("svitok3")
                            return "remove_svitok3"
                else:
                    self.set_puzzle("scroll_shelf")
                return None

            # Ключ под полкой со свитками
            if all(self.scrolls_placed) and self.is_scrolls_correct() and "anibus_key" not in self.inventory:
                key_rect = pygame.Rect(170, self.screen_height - 400, 60, 30)
                if key_rect.collidepoint(x, y):
                    if self.add_to_inventory:
                        self.add_to_inventory("anibus_key")
                    return "add_anibus_key"

            # NPC кот
            cat_rect = pygame.Rect(self.screen_width - 250, self.screen_height - 300, 150, 200)
            if cat_rect.collidepoint(x, y):
                if self.selected_item == "karta":
                    self.npc_key_available = True
                    if self.remove_from_inventory:
                        self.remove_from_inventory("karta")
                    return "remove_karta"
                else:
                    self.npc_interacted = True
                return None

            # Ключ от NPC
            if self.npc_key_available and "key_from_npc" not in self.inventory:
                key_rect = pygame.Rect(self.screen_width - 200, self.screen_height - 350, 60, 30)
                if key_rect.collidepoint(x, y):
                    if self.add_to_inventory:
                        self.add_to_inventory("key_from_npc")
                    return "add_key_from_npc"

        return None