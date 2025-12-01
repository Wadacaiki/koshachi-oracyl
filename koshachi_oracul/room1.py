import pygame
from button import Button, TextInput


class Room1:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background = None
        self.inventory = []
        self.add_to_inventory = None
        self.remove_from_inventory = None
        self.current_puzzle = None
        self.domofon_code = ""
        self.vase_broken = False
        self.safe_opened = False
        self.coffin_opened = False
        self.load_background()

    def load_background(self):
        try:
            self.background = pygame.image.load("assets/Pyramid.png")
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except:
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((100, 100, 100))

    def draw(self, screen, has_all_statues=False):
        screen.blit(self.background, (0, 0))

        # Рисуем интерактивные элементы
        if not self.vase_broken:
            try:
                vase_img = pygame.image.load("assets/vaza.png")
                vase_img = pygame.transform.scale(vase_img, (100, 150))
                screen.blit(vase_img, (100, self.screen_height - 250))
            except:
                pygame.draw.rect(screen, (200, 200, 200), (100, self.screen_height - 250, 100, 150))

        if not self.coffin_opened:
            try:
                coffin_img = pygame.image.load("assets/grob_close.png")
                coffin_img = pygame.transform.scale(coffin_img, (200, 300))
                screen.blit(coffin_img, (self.screen_width - 250, self.screen_height - 350))
            except:
                pygame.draw.rect(screen, (150, 150, 150), (self.screen_width - 250, self.screen_height - 350, 200, 300))
        else:
            try:
                coffin_img = pygame.image.load("assets/grob_open.png")
                coffin_img = pygame.transform.scale(coffin_img, (200, 300))
                screen.blit(coffin_img, (self.screen_width - 250, self.screen_height - 350))
                # Анибус в гробнице
                if "anibus" not in self.inventory:
                    try:
                        anibus_img = pygame.image.load("assets/anibus.png")
                        anibus_img = pygame.transform.scale(anibus_img, (80, 80))
                        screen.blit(anibus_img, (self.screen_width - 200, self.screen_height - 300))
                    except:
                        pygame.draw.circle(screen, (255, 215, 0), (self.screen_width - 160, self.screen_height - 260),
                                           30)
            except:
                pass

        if not self.safe_opened:
            try:
                safe_img = pygame.image.load("assets/polka_s_seyfom_s_npc_key.png")
                safe_img = pygame.transform.scale(safe_img, (150, 150))
                screen.blit(safe_img, (self.screen_width - 200, 100))
            except:
                pygame.draw.rect(screen, (100, 100, 100), (self.screen_width - 200, 100, 150, 150))
        else:
            if "serebro_cat" not in self.inventory:
                try:
                    cat_img = pygame.image.load("assets/serebro_cat.png")
                    cat_img = pygame.transform.scale(cat_img, (80, 80))
                    screen.blit(cat_img, (self.screen_width - 180, 120))
                except:
                    pygame.draw.circle(screen, (200, 200, 200), (self.screen_width - 140, 160), 30)

        # Дверь
        try:
            door_img = pygame.image.load("assets/door.png")
            door_img = pygame.transform.scale(door_img, (150, 250))
            screen.blit(door_img, (self.screen_width // 2 - 75, self.screen_height - 300))
        except:
            pygame.draw.rect(screen, (100, 70, 30), (self.screen_width // 2 - 75, self.screen_height - 300, 150, 250))

        # Домофон
        try:
            domofon_img = pygame.image.load("assets/domofon.png")
            domofon_img = pygame.transform.scale(domofon_img, (80, 80))
            screen.blit(domofon_img, (self.screen_width // 2 + 100, self.screen_height - 200))
        except:
            pygame.draw.rect(screen, (50, 50, 50), (self.screen_width // 2 + 100, self.screen_height - 200, 80, 80))

        # Кирпичи
        brick_positions = [(200, 200), (300, 150), (400, 250), (500, 180)]
        for i, pos in enumerate(brick_positions):
            try:
                brick_img = pygame.image.load(f"assets/kirpich{i + 1}.png")
                brick_img = pygame.transform.scale(brick_img, (60, 40))
                screen.blit(brick_img, pos)
            except:
                pygame.draw.rect(screen, (150, 100, 50), (pos[0], pos[1], 60, 40))

        # Стрелки для навигации
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
            pygame.draw.polygon(screen, (255, 255, 255), [(self.screen_width - 20, self.screen_height // 2),
                                                          (self.screen_width - 50, self.screen_height // 2 - 25),
                                                          (self.screen_width - 50, self.screen_height // 2 + 25)])

        # Если активна головоломка, рисуем ее поверх
        if self.current_puzzle == "domofon":
            self.draw_domofon_puzzle(screen)
        elif self.current_puzzle == "brick":
            self.draw_brick_puzzle(screen)
        elif self.current_puzzle == "note":
            self.draw_note_puzzle(screen)

        return None

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

    def draw_brick_puzzle(self, screen):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont("Arial", 72)
        if self.current_puzzle_data == 1:
            text = "2"
        elif self.current_puzzle_data == 2:
            text = "9"
        elif self.current_puzzle_data == 3:
            text = "0"
        elif self.current_puzzle_data == 4:
            text = "5"
        else:
            text = "?"

        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (self.screen_width // 2 - text_surface.get_width() // 2,
                                   self.screen_height // 2 - text_surface.get_height() // 2))

    def draw_note_puzzle(self, screen):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        try:
            note_img = pygame.image.load("assets/zapiska_blizhe.png")
            note_img = pygame.transform.scale(note_img, (400, 500))
            screen.blit(note_img, (self.screen_width // 2 - 200, self.screen_height // 2 - 250))
        except:
            pygame.draw.rect(screen, (255, 255, 200),
                             (self.screen_width // 2 - 200, self.screen_height // 2 - 250, 400, 500))
            font = pygame.font.SysFont("Arial", 24)
            text = "Это записка с паролем: 1234"
            text_surface = font.render(text, True, (0, 0, 0))
            screen.blit(text_surface, (self.screen_width // 2 - text_surface.get_width() // 2,
                                       self.screen_height // 2 - text_surface.get_height() // 2))

    def set_puzzle(self, puzzle_type, data=None):
        self.current_puzzle = puzzle_type
        self.current_puzzle_data = data
        if puzzle_type is None:
            self.domofon_code = ""

    def handle_event(self, event, has_all_statues=False):
        if self.current_puzzle:
            return self.handle_puzzle_event(event)
        else:
            return self.handle_room_event(event, has_all_statues)

    def handle_puzzle_event(self, event):
        if self.current_puzzle == "domofon":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if "".join(self.domofon_code) == "2905":
                        self.set_puzzle(None)
                        return "next_room"  # Переход к комнатам пирамиды
                    else:
                        self.domofon_code = []  # Неправильный код
                elif event.key == pygame.K_BACKSPACE:
                    self.domofon_code = self.domofon_code[:-1]
                elif event.unicode.isdigit() and len(self.domofon_code) < 4:
                    self.domofon_code.append(event.unicode)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Проверяем кнопку назад
                back_btn = Button(self.screen_width // 2 - 50, self.screen_height // 2 + 100, "Назад",
                                  lambda: self.set_puzzle(None))
                if back_btn.rect.collidepoint(event.pos):
                    self.set_puzzle(None)

        elif self.current_puzzle == "brick":
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                self.set_puzzle(None)

        elif self.current_puzzle == "note":
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                self.set_puzzle(None)

        return None

    def handle_room_event(self, event, has_all_statues=False):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Проверяем стрелки навигации
            if 20 <= x <= 70 and self.screen_height // 2 - 25 <= y <= self.screen_height // 2 + 25:
                return "prev_room"
            if self.screen_width - 70 <= x <= self.screen_width - 20 and self.screen_height // 2 - 25 <= y <= self.screen_height // 2 + 25:
                return "next_room"

            # Проверяем домофон
            domofon_rect = pygame.Rect(self.screen_width // 2 + 100, self.screen_height - 200, 80, 80)
            if domofon_rect.collidepoint(x, y):
                self.set_puzzle("domofon")
                return None

            # Проверяем кирпичи
            brick_positions = [(200, 200, 60, 40), (300, 150, 60, 40), (400, 250, 60, 40), (500, 180, 60, 40)]
            for i, (bx, by, bw, bh) in enumerate(brick_positions):
                if bx <= x <= bx + bw and by <= y <= by + bh:
                    self.set_puzzle("brick", i + 1)
                    return None

            # Проверяем вазу
            if not self.vase_broken and 100 <= x <= 200 and self.screen_height - 250 <= y <= self.screen_height - 100:
                self.vase_broken = True
                self.add_to_inventory("zapiska")
                return "add_zapiska"

            # Проверяем гробницу
            coffin_rect = pygame.Rect(self.screen_width - 250, self.screen_height - 350, 200, 300)
            if coffin_rect.collidepoint(x, y):
                if not self.coffin_opened and "anibus_key" in self.inventory:
                    self.coffin_opened = True
                    self.remove_from_inventory("anibus_key")
                    return "remove_anibus_key"
                elif self.coffin_opened and "anibus" not in self.inventory:
                    self.add_to_inventory("anibus")
                    return "add_anibus"

            # Проверяем сейф
            safe_rect = pygame.Rect(self.screen_width - 200, 100, 150, 150)
            if safe_rect.collidepoint(x, y):
                if not self.safe_opened and "key_from_npc" in self.inventory:
                    self.safe_opened = True
                    self.remove_from_inventory("key_from_npc")
                    return "remove_key_from_npc"
                elif self.safe_opened and "serebro_cat" not in self.inventory:
                    self.add_to_inventory("serebro_cat")
                    return "add_serebro_cat"

            # Проверяем дверь
            door_rect = pygame.Rect(self.screen_width // 2 - 75, self.screen_height - 300, 150, 250)
            if door_rect.collidepoint(x, y) and has_all_statues and "anibus" in self.inventory:
                return "door_puzzle"

        return None