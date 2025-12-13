import pygame
from button import Button


class Room2:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Константы для шкафа
        self.CLOSET_WIDTH = 300
        self.CLOSET_HEIGHT = 400
        self.CLOSET_X = 100
        self.CLOSET_Y = self.screen_height - 450

        # Константы для полки с кристаллами
        self.CRYSTAL_SHELF_WIDTH = 120
        self.CRYSTAL_SHELF_HEIGHT = 100
        self.CRYSTAL_SHELF_X = self.CLOSET_X + 50
        self.CRYSTAL_SHELF_Y = self.CLOSET_Y + 50

        # Константы для полки со свитками
        self.SCROLL_SHELF_WIDTH = 120
        self.SCROLL_SHELF_HEIGHT = 100
        self.SCROLL_SHELF_X = self.CLOSET_X + 50
        self.SCROLL_SHELF_Y = self.CLOSET_Y - 50

        # Константы для NPC кота
        self.CAT_WIDTH = 150
        self.CAT_HEIGHT = 200
        self.CAT_X = self.screen_width - 250
        self.CAT_Y = self.screen_height - 300

        # Константы для ключей и свитков
        self.KEY_WIDTH = 60
        self.KEY_HEIGHT = 30
        self.SCROLL_WIDTH = 40
        self.SCROLL_HEIGHT = 60

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
            closet_img = pygame.transform.scale(closet_img, (self.CLOSET_WIDTH, self.CLOSET_HEIGHT))
            screen.blit(closet_img, (self.CLOSET_X, self.CLOSET_Y))
        except:
            pygame.draw.rect(screen, (100, 70, 30),
                             (self.CLOSET_X, self.CLOSET_Y, self.CLOSET_WIDTH, self.CLOSET_HEIGHT))

        # Полка с кристаллами
        try:
            if self.crystal_shelf_state == 0:
                crystal_img = pygame.image.load("assets/polka_kristal.png")
            elif self.crystal_shelf_state == 1:
                crystal_img = pygame.image.load("assets/polka_kristal_2.png")
            else:
                crystal_img = pygame.image.load("assets/polka_kristal_3.png")
            crystal_img = pygame.transform.scale(crystal_img,
                                                 (self.CRYSTAL_SHELF_WIDTH, self.CRYSTAL_SHELF_HEIGHT))
            screen.blit(crystal_img, (self.CRYSTAL_SHELF_X, self.CRYSTAL_SHELF_Y))
        except:
            pygame.draw.rect(screen, (150, 150, 150),
                             (self.CRYSTAL_SHELF_X, self.CRYSTAL_SHELF_Y,
                              self.CRYSTAL_SHELF_WIDTH, self.CRYSTAL_SHELF_HEIGHT))

        # Свиток под полкой с кристаллами (после решения)
        if self.crystal_shelf_state >= 2 and "svitok3" not in self.inventory:
            scroll_x = self.CRYSTAL_SHELF_X + 20
            scroll_y = self.CRYSTAL_SHELF_Y + self.CRYSTAL_SHELF_HEIGHT + 20
            try:
                scroll_img = pygame.image.load("assets/svitok3.png")
                scroll_img = pygame.transform.scale(scroll_img, (self.SCROLL_WIDTH, self.SCROLL_HEIGHT))
                screen.blit(scroll_img, (scroll_x, scroll_y))
            except:
                pygame.draw.rect(screen, (200, 200, 150), (scroll_x, scroll_y, self.SCROLL_WIDTH, self.SCROLL_HEIGHT))

        # Полка со свитками
        try:
            scroll_shelf_img = pygame.image.load("assets/polka_svitok.png")
            scroll_shelf_img = pygame.transform.scale(scroll_shelf_img,
                                                      (self.SCROLL_SHELF_WIDTH, self.SCROLL_SHELF_HEIGHT))
            screen.blit(scroll_shelf_img, (self.SCROLL_SHELF_X, self.SCROLL_SHELF_Y))
        except:
            pygame.draw.rect(screen, (150, 150, 150),
                             (self.SCROLL_SHELF_X, self.SCROLL_SHELF_Y,
                              self.SCROLL_SHELF_WIDTH, self.SCROLL_SHELF_HEIGHT))

        # Ключ под полкой со свитками (после решения)
        if all(self.scrolls_placed) and self.is_scrolls_correct() and "anibus_key" not in self.inventory:
            key_x = self.SCROLL_SHELF_X + 20
            key_y = self.SCROLL_SHELF_Y + self.SCROLL_SHELF_HEIGHT + 20
            try:
                key_img = pygame.image.load("assets/anibus_key.png")
                key_img = pygame.transform.scale(key_img, (self.KEY_WIDTH, self.KEY_HEIGHT))
                screen.blit(key_img, (key_x, key_y))
            except:
                pygame.draw.rect(screen, (200, 200, 0), (key_x, key_y, self.KEY_WIDTH, self.KEY_HEIGHT))

        # NPC кот
        try:
            cat_img = pygame.image.load("assets/cat_npc.png")
            cat_img = pygame.transform.scale(cat_img, (self.CAT_WIDTH, self.CAT_HEIGHT))
            screen.blit(cat_img, (self.CAT_X, self.CAT_Y))
        except:
            pygame.draw.circle(screen, (150, 150, 150),
                               (self.CAT_X + self.CAT_WIDTH // 2,
                                self.CAT_Y + self.CAT_HEIGHT // 2),
                               self.CAT_WIDTH // 3)

        # Диалоговое облако
        if self.npc_interacted and not self.npc_key_available:
            dialog_x = self.CAT_X - 150
            dialog_y = self.CAT_Y - 50

            try:
                dialog_img = pygame.image.load("assets/dialog.png")
                dialog_img = pygame.transform.scale(dialog_img, (200, 100))
                screen.blit(dialog_img, (dialog_x, dialog_y))

                font = pygame.font.SysFont("Arial", 16)
                text = font.render("Принеси мне карту!", True, (0, 0, 0))
                screen.blit(text, (dialog_x + 10, dialog_y + 30))
            except:
                pygame.draw.ellipse(screen, (255, 255, 255), (dialog_x, dialog_y, 200, 100))
                font = pygame.font.SysFont("Arial", 16)
                text = font.render("Принеси мне карту!", True, (0, 0, 0))
                screen.blit(text, (dialog_x + 10, dialog_y + 30))

        # Ключ от NPC (после получения карты)
        if self.npc_key_available and "key_from_npc" not in self.inventory:
            key_x = self.CAT_X + 50
            key_y = self.CAT_Y - 50
            try:
                key_img = pygame.image.load("assets/key_from_npc.png")
                key_img = pygame.transform.scale(key_img, (self.KEY_WIDTH, self.KEY_HEIGHT))
                screen.blit(key_img, (key_x, key_y))
            except:
                pygame.draw.rect(screen, (200, 100, 0), (key_x, key_y, self.KEY_WIDTH, self.KEY_HEIGHT))

        # Стрелки для навигации
        self.draw_navigation_arrows(screen)

        # Если активна головоломка, рисуем ее поверх
        if self.current_puzzle == "crystal_shelf":
            self.draw_crystal_shelf_puzzle(screen)
        elif self.current_puzzle == "scroll_shelf":
            self.draw_scroll_shelf_puzzle(screen)

        return None

    def draw_navigation_arrows(self, screen):
        # Стрелка влево
        left_arrow_x = 20
        left_arrow_y = self.screen_height // 2 - 25

        try:
            left_arrow = pygame.image.load("assets/left_strelka.png")
            left_arrow = pygame.transform.scale(left_arrow, (50, 50))
            screen.blit(left_arrow, (left_arrow_x, left_arrow_y))
        except:
            pygame.draw.polygon(screen, (255, 255, 255),
                                [(left_arrow_x, left_arrow_y + 25),
                                 (left_arrow_x + 30, left_arrow_y),
                                 (left_arrow_x + 30, left_arrow_y + 50)])

        # Стрелка вправо
        right_arrow_x = self.screen_width - 70
        right_arrow_y = self.screen_height // 2 - 25

        try:
            right_arrow = pygame.image.load("assets/right_strelka.png")
            right_arrow = pygame.transform.scale(right_arrow, (50, 50))
            screen.blit(right_arrow, (right_arrow_x, right_arrow_y))
        except:
            pygame.draw.polygon(screen, (255, 255, 255),
                                [(right_arrow_x + 20, right_arrow_y + 25),
                                 (right_arrow_x - 10, right_arrow_y),
                                 (right_arrow_x - 10, right_arrow_y + 50)])

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
            left_arrow_rect = pygame.Rect(20, self.screen_height // 2 - 25, 50, 50)
            right_arrow_rect = pygame.Rect(self.screen_width - 70, self.screen_height // 2 - 25, 50, 50)

            if left_arrow_rect.collidepoint(x, y):
                return "prev_room"
            if right_arrow_rect.collidepoint(x, y):
                return "next_room"

            # Полка с кристаллами
            crystal_rect = pygame.Rect(self.CRYSTAL_SHELF_X, self.CRYSTAL_SHELF_Y,
                                       self.CRYSTAL_SHELF_WIDTH, self.CRYSTAL_SHELF_HEIGHT)
            if crystal_rect.collidepoint(x, y):
                self.set_puzzle("crystal_shelf")
                return None

            # Свиток под полкой с кристаллами
            if self.crystal_shelf_state >= 2 and "svitok3" not in self.inventory:
                scroll_x = self.CRYSTAL_SHELF_X + 20
                scroll_y = self.CRYSTAL_SHELF_Y + self.CRYSTAL_SHELF_HEIGHT + 20
                scroll_rect = pygame.Rect(scroll_x, scroll_y, self.SCROLL_WIDTH, self.SCROLL_HEIGHT)
                if scroll_rect.collidepoint(x, y):
                    if self.add_to_inventory:
                        self.add_to_inventory("svitok3")
                    return "add_svitok3"

            # Полка со свитками
            scroll_shelf_rect = pygame.Rect(self.SCROLL_SHELF_X, self.SCROLL_SHELF_Y,
                                            self.SCROLL_SHELF_WIDTH, self.SCROLL_SHELF_HEIGHT)
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
                key_x = self.SCROLL_SHELF_X + 20
                key_y = self.SCROLL_SHELF_Y + self.SCROLL_SHELF_HEIGHT + 20
                key_rect = pygame.Rect(key_x, key_y, self.KEY_WIDTH, self.KEY_HEIGHT)
                if key_rect.collidepoint(x, y):
                    if self.add_to_inventory:
                        self.add_to_inventory("anibus_key")
                    return "add_anibus_key"

            # NPC кот
            cat_rect = pygame.Rect(self.CAT_X, self.CAT_Y, self.CAT_WIDTH, self.CAT_HEIGHT)
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
                key_x = self.CAT_X + 50
                key_y = self.CAT_Y - 50
                key_rect = pygame.Rect(key_x, key_y, self.KEY_WIDTH, self.KEY_HEIGHT)
                if key_rect.collidepoint(x, y):
                    if self.add_to_inventory:
                        self.add_to_inventory("key_from_npc")
                    return "add_key_from_npc"

        return None