import pygame
from button import Button  # можно оставить, даже если сейчас не используешь


class Room1:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.VASE_WIDTH = 700
        self.VASE_HEIGHT = 650
        self.VASE_X = -100
        self.VASE_Y = self.screen_height - 470

        self.NOTE_WIDTH = 60
        self.NOTE_HEIGHT = 80
        self.NOTE_X = self.VASE_X + (self.VASE_WIDTH // 2) - (self.NOTE_WIDTH // 2)
        self.NOTE_Y = self.VASE_Y + 370

        self.COFFIN_WIDTH = 300
        self.COFFIN_HEIGHT = 450
        self.COFFIN_X = self.screen_width - 400
        self.COFFIN_Y = self.screen_height - 450

        self.ANIBUS_WIDTH = 100
        self.ANIBUS_HEIGHT = 100

        self.SAFE_WIDTH = 200
        self.SAFE_HEIGHT = 150
        self.SAFE_X = self.screen_width - 280
        self.SAFE_Y = 120

        self.DOOR_WIDTH = 350
        self.DOOR_HEIGHT = 650
        self.DOOR_X = self.screen_width // 2 - 175
        self.DOOR_Y = self.screen_height - 650

        self.ARROW_SIZE = 50

        self.vase_broken = False
        self.note_visible_on_floor = False
        self.note_taken = False
        self.show_note_big = False
        self.note_big_rect = None

        self.coffin_opened = False
        self.anibus_taken = False

        self.safe_opened = False
        self.serebro_cat_taken = False

        self.background = self._load_scaled(
            "assets/bg_room.png", (self.screen_width, self.screen_height)
        )
        self.vase_img = self._load_scaled("assets/vaza.png", (self.VASE_WIDTH, self.VASE_HEIGHT))
        self.vase_broken_img = self._load_scaled(
            "assets/vaza_razbita.png", (self.VASE_WIDTH, self.VASE_HEIGHT)
        )
        self.note_img = self._load_scaled("assets/zapiska.png", (self.NOTE_WIDTH, self.NOTE_HEIGHT))
        self.note_big_img = self._load_scaled("assets/zapiska_blizhe.png", (400, 300))

        self.coffin_closed_img = self._load_scaled(
            "assets/grob_close.png", (self.COFFIN_WIDTH, self.COFFIN_HEIGHT)
        )
        self.coffin_open_img = self._load_scaled(
            "assets/grob_open.png", (self.COFFIN_WIDTH, self.COFFIN_HEIGHT)
        )
        self.anibus_img = self._load_scaled(
            "assets/anibus.png", (self.ANIBUS_WIDTH, self.ANIBUS_HEIGHT)
        )

        self.safe_closed_img = self._load_scaled(
            "assets/polka_s_seyfom_s_npc_key.png", (self.SAFE_WIDTH, self.SAFE_HEIGHT)
        )
        self.serebro_cat_img = self._load_scaled("assets/serebro_cat.png", (80, 80))

        self.door_img = self._load_scaled("assets/door.png", (self.DOOR_WIDTH, self.DOOR_HEIGHT))

        self.left_arrow_img = self._load_scaled("assets/left_strelka.png",
                                                (self.ARROW_SIZE, self.ARROW_SIZE))
        self.right_arrow_img = self._load_scaled("assets/right_strelka.png",
                                                 (self.ARROW_SIZE, self.ARROW_SIZE))

        self.font_mid = pygame.font.SysFont("Arial", 24)

    def _load_scaled(self, path, size):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        except:
            surf = pygame.Surface(size, pygame.SRCALPHA)
            surf.fill((80, 80, 80))
            return surf


    def draw(self, screen, has_all_statues):
        screen.blit(self.background, (0, 0))

        if not self.vase_broken:
            screen.blit(self.vase_img, (self.VASE_X, self.VASE_Y))
        else:
            broken_y = self.VASE_Y - 50
            screen.blit(self.vase_broken_img, (self.VASE_X, broken_y))

        if self.vase_broken and self.note_visible_on_floor and not self.note_taken:
            screen.blit(self.note_img, (self.NOTE_X, self.NOTE_Y))

        if not self.coffin_opened:
            screen.blit(self.coffin_closed_img, (self.COFFIN_X, self.COFFIN_Y))
        else:
            screen.blit(self.coffin_open_img, (self.COFFIN_X, self.COFFIN_Y))
            if not self.anibus_taken:
                anibus_x = self.COFFIN_X + self.COFFIN_WIDTH // 2 - self.ANIBUS_WIDTH // 2
                anibus_y = self.COFFIN_Y + self.COFFIN_HEIGHT // 2
                screen.blit(self.anibus_img, (anibus_x, anibus_y))

        screen.blit(self.safe_closed_img, (self.SAFE_X, self.SAFE_Y))
        if self.safe_opened and not self.serebro_cat_taken:
            cat_x = self.SAFE_X + self.SAFE_WIDTH // 2 - 40
            cat_y = self.SAFE_Y + 20
            screen.blit(self.serebro_cat_img, (cat_x, cat_y))

        screen.blit(self.door_img, (self.DOOR_X, self.DOOR_Y))

        self._draw_arrows(screen)

        if self.show_note_big:
            self._draw_big_note(screen)

        return None

    def _draw_arrows(self, screen):
        left_x = 20
        left_y = self.screen_height // 2 - self.ARROW_SIZE // 2
        right_x = self.screen_width - 20 - self.ARROW_SIZE
        right_y = left_y
        screen.blit(self.left_arrow_img, (left_x, left_y))
        screen.blit(self.right_arrow_img, (right_x, right_y))

    def _draw_big_note(self, screen):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        self.note_big_rect = self.note_big_img.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2)
        )
        screen.blit(self.note_big_img, self.note_big_rect.topleft)


    def handle_event(self, event, selected_item, has_all_statues):
        if self.show_note_big:
            return self._handle_big_note_event(event)

        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return None

        x, y = event.pos

        left_rect = pygame.Rect(20, self.screen_height // 2 - self.ARROW_SIZE // 2,
                                self.ARROW_SIZE, self.ARROW_SIZE)
        right_rect = pygame.Rect(self.screen_width - 20 - self.ARROW_SIZE,
                                 self.screen_height // 2 - self.ARROW_SIZE // 2,
                                 self.ARROW_SIZE, self.ARROW_SIZE)
        if left_rect.collidepoint(x, y):
            return "prev_room"
        if right_rect.collidepoint(x, y):
            return "next_room"

        vase_rect = pygame.Rect(self.VASE_X, self.VASE_Y, self.VASE_WIDTH, self.VASE_HEIGHT)
        if vase_rect.collidepoint(x, y) and not self.vase_broken:
            self.vase_broken = True
            self.note_visible_on_floor = True
            return None

        if self.vase_broken and self.note_visible_on_floor and not self.note_taken:
            note_rect = pygame.Rect(self.NOTE_X, self.NOTE_Y,
                                    self.NOTE_WIDTH, self.NOTE_HEIGHT)
            if note_rect.collidepoint(x, y):
                self.note_taken = True
                self.note_visible_on_floor = False
                return "add_zapiska"

        coffin_rect = pygame.Rect(self.COFFIN_X, self.COFFIN_Y,
                                  self.COFFIN_WIDTH, self.COFFIN_HEIGHT)
        if coffin_rect.collidepoint(x, y):
            if not self.coffin_opened:
                if selected_item == "anibus_key":
                    self.coffin_opened = True
                    return "remove_anibus_key"
            else:
                if not self.anibus_taken:
                    self.anibus_taken = True
                    return "add_anibus"
            return None

        if self.coffin_opened and not self.anibus_taken:
            anibus_x = self.COFFIN_X + self.COFFIN_WIDTH // 2 - self.ANIBUS_WIDTH // 2
            anibus_y = self.COFFIN_Y + self.COFFIN_HEIGHT // 2
            anibus_rect = pygame.Rect(anibus_x, anibus_y,
                                      self.ANIBUS_WIDTH, self.ANIBUS_HEIGHT)
            if anibus_rect.collidepoint(x, y):
                self.anibus_taken = True
                return "add_anibus"

        safe_rect = pygame.Rect(self.SAFE_X, self.SAFE_Y, self.SAFE_WIDTH, self.SAFE_HEIGHT)
        if safe_rect.collidepoint(x, y):
            if not self.safe_opened:
                if selected_item == "key_from_npc":
                    self.safe_opened = True
                    return "remove_key_from_npc"
            else:
                if not self.serebro_cat_taken:
                    cat_x = self.SAFE_X + self.SAFE_WIDTH // 2 - 40
                    cat_y = self.SAFE_Y + 20
                    cat_rect = pygame.Rect(cat_x, cat_y, 80, 80)
                    if cat_rect.collidepoint(x, y):
                        self.serebro_cat_taken = True
                        return "add_serebro_cat"
            return None

        door_rect = pygame.Rect(self.DOOR_X, self.DOOR_Y, self.DOOR_WIDTH, self.DOOR_HEIGHT)
        if door_rect.collidepoint(x, y) and has_all_statues:
            return "door_puzzle"

        return None

    def _handle_big_note_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.show_note_big = False
            return None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if self.note_big_rect and not self.note_big_rect.collidepoint(x, y):
                self.show_note_big = False
        return None

    def open_note_from_inventory(self):
        if self.note_taken:
            self.show_note_big = True
