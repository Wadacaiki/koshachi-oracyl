import pygame
from button import Button


class Room1:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background = None
        self.inventory = []
        self.add_to_inventory = None
        self.remove_from_inventory = None
        self.selected_item = None
        self.current_puzzle = None
        self.vase_broken = False
        self.safe_opened = False
        self.coffin_opened = False
        self.load_background()

    def load_background(self):
        try:
            self.background = pygame.image.load("assets/bg_room.png")
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except:
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((100, 100, 100))

    def draw(self, screen, has_all_statues=False):
        screen.blit(self.background, (0, 0))

        # Ваза
        if not self.vase_broken:
            try:
                vase_img = pygame.image.load("assets/vaza.png")
                vase_img = pygame.transform.scale(vase_img, (450, 750))
                screen.blit(vase_img, (30, self.screen_height - 550))
            except:
                pygame.draw.rect(screen, (200, 200, 200), (30, self.screen_height - 550, 450, 750))
        else:
            # Разбитая ваза
            try:
                vase_img = pygame.image.load("assets/vaza_razbita.png")
                vase_img = pygame.transform.scale(vase_img, (450, 750))
                screen.blit(vase_img, (30, self.screen_height - 600))
            except:
                pygame.draw.rect(screen, (150, 150, 150), (30, self.screen_height - 600, 450, 750))

        # Записка (после разбития вазы)
        if self.vase_broken and "zapiska" not in self.inventory:
            try:
                note_img = pygame.image.load("assets/zapiska.png")
                note_img = pygame.transform.scale(note_img, (60, 80))
                screen.blit(note_img, (225, self.screen_height - 550))
            except:
                pygame.draw.rect(screen, (255, 255, 200), (225, self.screen_height - 550, 60, 80))

        # Гробница
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

                # Анибус внутри
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

        # Сейф
        if not self.safe_opened:
            try:
                safe_img = pygame.image.load("assets/polka_s_seyfom_s_npc_key.png")
                safe_img = pygame.transform.scale(safe_img, (150, 150))
                screen.blit(safe_img, (self.screen_width - 200, 100))
            except:
                pygame.draw.rect(screen, (100, 100, 100), (self.screen_width - 200, 100, 150, 150))
        else:
            # Статуэтка кота в сейфе
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

        # Показать увеличенную записку
        if self.current_puzzle == "note":
            self.draw_note_puzzle(screen)

        return None

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
            text = "Записка с паролем: 1234"
            text_surface = font.render(text, True, (0, 0, 0))
            screen.blit(text_surface,
                        (self.screen_width // 2 - text_surface.get_width() // 2,
                         self.screen_height // 2 - text_surface.get_height() // 2))

    def set_puzzle(self, puzzle_type):
        self.current_puzzle = puzzle_type
        if puzzle_type is None:
            pygame.time.set_timer(pygame.USEREVENT, 0)

    def handle_event(self, event, has_all_statues=False):
        if self.current_puzzle:
            return self.handle_puzzle_event(event)
        else:
            return self.handle_room_event(event, has_all_statues)

    def handle_puzzle_event(self, event):
        if self.current_puzzle == "note":
            if event.type == pygame.USEREVENT:
                self.set_puzzle(None)
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                self.set_puzzle(None)

        return None

    def handle_room_event(self, event, has_all_statues=False):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Стрелки навигации
            if 20 <= x <= 70 and self.screen_height // 2 - 25 <= y <= self.screen_height // 2 + 25:
                return "prev_room"
            if self.screen_width - 70 <= x <= self.screen_width - 20 and self.screen_height // 2 - 25 <= y <= self.screen_height // 2 + 25:
                return "next_room"

            # Ваза
            vase_rect = pygame.Rect(30, self.screen_height - 550, 450, 750)
            if not self.vase_broken and vase_rect.collidepoint(x, y):
                self.vase_broken = True
                return None

            # Записка
            if self.vase_broken and "zapiska" not in self.inventory:
                note_rect = pygame.Rect(225, self.screen_height - 550, 60, 80)
                if note_rect.collidepoint(x, y):
                    if self.add_to_inventory:
                        self.add_to_inventory("zapiska")
                    return "add_zapiska"

            # Гробница
            coffin_rect = pygame.Rect(self.screen_width - 250, self.screen_height - 350, 200, 300)
            if coffin_rect.collidepoint(x, y):
                if not self.coffin_opened:
                    if self.selected_item == "anibus_key":
                        self.coffin_opened = True
                        if self.remove_from_inventory:
                            self.remove_from_inventory("anibus_key")
                        return "remove_anibus_key"
                elif "anibus" not in self.inventory:
                    if self.add_to_inventory:
                        self.add_to_inventory("anibus")
                    return "add_anibus"

            # Сейф
            safe_rect = pygame.Rect(self.screen_width - 200, 100, 150, 150)
            if safe_rect.collidepoint(x, y):
                if not self.safe_opened:
                    if self.selected_item == "key_from_npc":
                        self.safe_opened = True
                        if self.remove_from_inventory:
                            self.remove_from_inventory("key_from_npc")
                        return "remove_key_from_npc"
                elif "serebro_cat" not in self.inventory:
                    if self.add_to_inventory:
                        self.add_to_inventory("serebro_cat")
                    return "add_serebro_cat"

            # Дверь
            door_rect = pygame.Rect(self.screen_width // 2 - 75, self.screen_height - 300, 150, 250)
            if door_rect.collidepoint(x, y) and has_all_statues and "anibus" in self.inventory:
                return "door_puzzle"

        elif event.type == pygame.KEYDOWN:
            # Нажатие на записку в инвентаре
            if self.selected_item == "zapiska":
                self.set_puzzle("note")
                # Таймер на 5 секунд
                pygame.time.set_timer(pygame.USEREVENT, 5000)

        return None