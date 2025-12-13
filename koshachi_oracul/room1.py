import pygame
from button import Button


class Room1:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Константы для вазы
        self.VASE_WIDTH = 450
        self.VASE_HEIGHT = 750
        self.VASE_X = 30
        self.VASE_Y = self.screen_height - 550

        # Константы для записки
        self.NOTE_WIDTH = 60
        self.NOTE_HEIGHT = 80
        self.NOTE_X = self.VASE_X + (self.VASE_WIDTH // 2) - (self.NOTE_WIDTH // 2)
        self.NOTE_Y = self.VASE_Y

        # Константы для гробницы
        self.COFFIN_WIDTH = 200
        self.COFFIN_HEIGHT = 300
        self.COFFIN_X = self.screen_width - 250
        self.COFFIN_Y = self.screen_height - 350

        # Константы для сейфа
        self.SAFE_WIDTH = 150
        self.SAFE_HEIGHT = 150
        self.SAFE_X = self.screen_width - 200
        self.SAFE_Y = 100

        # Константы для двери
        self.DOOR_WIDTH = 150
        self.DOOR_HEIGHT = 250
        self.DOOR_X = self.screen_width // 2 - 75
        self.DOOR_Y = self.screen_height - 300

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
                vase_img = pygame.transform.scale(vase_img, (self.VASE_WIDTH, self.VASE_HEIGHT))
                screen.blit(vase_img, (self.VASE_X, self.VASE_Y))
            except:
                pygame.draw.rect(screen, (200, 200, 200), (self.VASE_X, self.VASE_Y, self.VASE_WIDTH, self.VASE_HEIGHT))
        else:
            # Разбитая ваза - на 50px выше
            broken_vase_y = self.VASE_Y - 50
            try:
                vase_img = pygame.image.load("assets/vaza_razbita.png")
                vase_img = pygame.transform.scale(vase_img, (self.VASE_WIDTH, self.VASE_HEIGHT))
                screen.blit(vase_img, (self.VASE_X, broken_vase_y))
            except:
                pygame.draw.rect(screen, (150, 150, 150),
                                 (self.VASE_X, broken_vase_y, self.VASE_WIDTH, self.VASE_HEIGHT))

            # Записка на развалинах вазы
            if "zapiska" not in self.inventory:
                try:
                    note_img = pygame.image.load("assets/zapiska.png")
                    note_img = pygame.transform.scale(note_img, (self.NOTE_WIDTH, self.NOTE_HEIGHT))
                    screen.blit(note_img, (self.NOTE_X, self.NOTE_Y))
                except:
                    pygame.draw.rect(screen, (255, 255, 200),
                                     (self.NOTE_X, self.NOTE_Y, self.NOTE_WIDTH, self.NOTE_HEIGHT))

        # Гробница
        if not self.coffin_opened:
            try:
                coffin_img = pygame.image.load("assets/grob_close.png")
                coffin_img = pygame.transform.scale(coffin_img, (self.COFFIN_WIDTH, self.COFFIN_HEIGHT))
                screen.blit(coffin_img, (self.COFFIN_X, self.COFFIN_Y))
            except:
                pygame.draw.rect(screen, (150, 150, 150),
                                 (self.COFFIN_X, self.COFFIN_Y, self.COFFIN_WIDTH, self.COFFIN_HEIGHT))
        else:
            try:
                coffin_img = pygame.image.load("assets/grob_open.png")
                coffin_img = pygame.transform.scale(coffin_img, (self.COFFIN_WIDTH, self.COFFIN_HEIGHT))
                screen.blit(coffin_img, (self.COFFIN_X, self.COFFIN_Y))

                # Анибус внутри
                if "anibus" not in self.inventory:
                    try:
                        anibus_img = pygame.image.load("assets/anibus.png")
                        anibus_img = pygame.transform.scale(anibus_img, (80, 80))
                        anibus_x = self.COFFIN_X + (self.COFFIN_WIDTH // 2) - 40
                        anibus_y = self.COFFIN_Y + (self.COFFIN_HEIGHT // 2) - 40
                        screen.blit(anibus_img, (anibus_x, anibus_y))
                    except:
                        pygame.draw.circle(screen, (255, 215, 0),
                                           (self.COFFIN_X + self.COFFIN_WIDTH // 2,
                                            self.COFFIN_Y + self.COFFIN_HEIGHT // 2), 30)
            except:
                pass

        # Сейф
        if not self.safe_opened:
            try:
                safe_img = pygame.image.load("assets/polka_s_seyfom_s_npc_key.png")
                safe_img = pygame.transform.scale(safe_img, (self.SAFE_WIDTH, self.SAFE_HEIGHT))
                screen.blit(safe_img, (self.SAFE_X, self.SAFE_Y))
            except:
                pygame.draw.rect(screen, (100, 100, 100), (self.SAFE_X, self.SAFE_Y, self.SAFE_WIDTH, self.SAFE_HEIGHT))
        else:
            # Статуэтка кота в сейфе
            if "serebro_cat" not in self.inventory:
                try:
                    cat_img = pygame.image.load("assets/serebro_cat.png")
                    cat_img = pygame.transform.scale(cat_img, (80, 80))
                    cat_x = self.SAFE_X + (self.SAFE_WIDTH // 2) - 40
                    cat_y = self.SAFE_Y + 20
                    screen.blit(cat_img, (cat_x, cat_y))
                except:
                    pygame.draw.circle(screen, (200, 200, 200),
                                       (self.SAFE_X + self.SAFE_WIDTH // 2,
                                        self.SAFE_Y + self.SAFE_HEIGHT // 2), 30)

        # Дверь
        try:
            door_img = pygame.image.load("assets/door.png")
            door_img = pygame.transform.scale(door_img, (self.DOOR_WIDTH, self.DOOR_HEIGHT))
            screen.blit(door_img, (self.DOOR_X, self.DOOR_Y))
        except:
            pygame.draw.rect(screen, (100, 70, 30), (self.DOOR_X, self.DOOR_Y, self.DOOR_WIDTH, self.DOOR_HEIGHT))

        # Стрелки для навигации
        self.draw_navigation_arrows(screen)

        # Показать увеличенную записку
        if self.current_puzzle == "note":
            self.draw_note_puzzle(screen)

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
            left_arrow_rect = pygame.Rect(20, self.screen_height // 2 - 25, 50, 50)
            right_arrow_rect = pygame.Rect(self.screen_width - 70, self.screen_height // 2 - 25, 50, 50)

            if left_arrow_rect.collidepoint(x, y):
                return "prev_room"
            if right_arrow_rect.collidepoint(x, y):
                return "next_room"

            # Целая ваза
            vase_rect = pygame.Rect(self.VASE_X, self.VASE_Y, self.VASE_WIDTH, self.VASE_HEIGHT)
            if not self.vase_broken and vase_rect.collidepoint(x, y):
                self.vase_broken = True
                return None

            # Записка на разбитой вазе
            if self.vase_broken and "zapiska" not in self.inventory:
                note_rect = pygame.Rect(self.NOTE_X, self.NOTE_Y, self.NOTE_WIDTH, self.NOTE_HEIGHT)
                if note_rect.collidepoint(x, y):
                    if self.add_to_inventory:
                        self.add_to_inventory("zapiska")
                    return "add_zapiska"

            # Гробница
            coffin_rect = pygame.Rect(self.COFFIN_X, self.COFFIN_Y, self.COFFIN_WIDTH, self.COFFIN_HEIGHT)
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
            safe_rect = pygame.Rect(self.SAFE_X, self.SAFE_Y, self.SAFE_WIDTH, self.SAFE_HEIGHT)
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
            door_rect = pygame.Rect(self.DOOR_X, self.DOOR_Y, self.DOOR_WIDTH, self.DOOR_HEIGHT)
            if door_rect.collidepoint(x, y) and has_all_statues and "anibus" in self.inventory:
                return "door_puzzle"

        elif event.type == pygame.KEYDOWN:
            # Нажатие на записку в инвентаре
            if self.selected_item == "zapiska":
                self.set_puzzle("note")
                pygame.time.set_timer(pygame.USEREVENT, 5000)  # 5 секунд

        return None