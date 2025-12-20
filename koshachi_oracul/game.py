import pygame
import time

from pyramid import PyramidPuzzle
from room1 import Room1
from room2 import Room2
from room3 import Room3
from inventory import Inventory


class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.current_screen = "story"  # story, pyramid, rooms

        self.pyramid_puzzle = PyramidPuzzle(screen_width, screen_height)
        self.rooms = [
            Room1(screen_width, screen_height),
            Room2(screen_width, screen_height),
            Room3(screen_width, screen_height),
        ]
        self.current_room = 0

        self.inventory = Inventory(screen_width, screen_height)

        self.story_shown = False
        self.pyramid_solved = False

        self.story_word_delay = 0.05
        self.story_extra_time = 5
    # ---------- ТЕКСТОВЫЕ ИСТОРИИ ----------

    def show_story(self, screen, filename):
        try:
            background = pygame.image.load("assets/history.png")
            background = pygame.transform.scale(
                background, (self.screen_width, self.screen_height)
            )
        except:
            background = pygame.Surface((self.screen_width, self.screen_height))
            background.fill((0, 0, 0))

        try:
            with open(f"data/{filename}", "r", encoding="utf-8") as file:
                story_text = file.read()
        except:
            story_text = (
                "Добро пожаловать в игру!"
                if filename == "start.txt"
                else "Поздравляем! Вы завершили игру!"
            )

        font = pygame.font.SysFont("Arial", 24)
        words = story_text.split()
        start_time = time.time()
        word_delay = self.story_word_delay

        showing = True
        while showing:
            current_time = time.time() - start_time
            words_to_show = min(len(words), int(current_time / word_delay))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    showing = False

            screen.blit(background, (0, 0))

            if words_to_show < len(words):
                current_text = " ".join(words[:words_to_show])
            else:
                current_text = story_text
                if current_time > len(words) * word_delay + self.story_extra_time:
                    showing = False

            # перенос строк
            lines = []
            words_in_line = current_text.split()
            current_line = ""
            for word in words_in_line:
                test_line = current_line + word + " "
                if font.size(test_line)[0] < self.screen_width - 100:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "
            lines.append(current_line)

            y_pos = self.screen_height // 2 - (len(lines) * 30) // 2
            for line in lines:
                text_surface = font.render(line, True, (255, 255, 255))
                screen.blit(text_surface, (50, y_pos))
                y_pos += 30

            pygame.display.flip()

        return "ok"

    # ---------- ИНВЕНТАРЬ ----------

    def is_inventory_toggle_clicked(self, pos):
        x, y = pos
        btn_rect = pygame.Rect(self.screen_width - 50, self.screen_height - 120, 40, 40)
        return btn_rect.collidepoint(x, y)

    def draw_inventory_toggle(self, screen):
        btn_rect = pygame.Rect(self.screen_width - 50, self.screen_height - 120, 40, 40)
        pygame.draw.rect(screen, (139, 69, 19), btn_rect, border_radius=5)
        font = pygame.font.SysFont("Arial", 20)
        btn_text = "↑" if not self.inventory.visible else "↓"
        text_surface = font.render(btn_text, True, (255, 255, 255))
        screen.blit(
            text_surface,
            (
                btn_rect.centerx - text_surface.get_width() // 2,
                btn_rect.centery - text_surface.get_height() // 2,
            ),
        )

    def check_door_conditions(self):
        cat_statues = ["serebro_cat", "black_cat", "med_cat"]
        has_all_statues = all(self.inventory.has_item(statue) for statue in cat_statues)
        has_anibus = self.inventory.has_item("anibus")
        return has_all_statues and has_anibus

    # ---------- ОСНОВНОЙ ЦИКЛ ----------

    def run(self, screen):
        if self.current_screen == "story" and not self.story_shown:
            res = self.show_story(screen, "start.txt")
            if res == "exit":
                return "exit"
            self.story_shown = True
            self.current_screen = "pyramid"

        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "main_menu"

                if self.current_screen == "pyramid":
                    self._handle_pyramid_event(event)
                elif self.current_screen == "rooms":
                    result = self._handle_rooms_event(event)
                    if result in ("exit", "main_menu"):
                        return result
                    if result == "door_solved":
                        end_res = self.show_story(screen, "finish.txt")
                        if end_res == "exit":
                            return "exit"
                        return "main_menu"

            screen.fill((0, 0, 0))

            if self.current_screen == "pyramid":
                self.pyramid_puzzle.draw(screen)
            elif self.current_screen == "rooms":
                self._draw_rooms(screen)

            pygame.display.flip()
            clock.tick(60)

        return "main_menu"

    # ---------- ПИРАМИДА ----------

    def _handle_pyramid_event(self, event):
        result = self.pyramid_puzzle.handle_event(event)
        if result == "pyramid_solved":
            self.current_screen = "rooms"
            self.pyramid_solved = True

    # ---------- КОМНАТЫ ----------

    def _draw_rooms(self, screen):
        current_room = self.rooms[self.current_room]

        cat_statues = ["serebro_cat", "black_cat", "med_cat"]
        has_all_statues = all(self.inventory.has_item(statue) for statue in cat_statues)

        current_room.draw(screen, has_all_statues)

        self.inventory.draw(screen)
        self.draw_inventory_toggle(screen)

    def _handle_rooms_event(self, event):
        current_room = self.rooms[self.current_room]

        # --- клик мышью: кнопка инвентаря + показ записки ---
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos

            # кнопка инвентаря
            if self.is_inventory_toggle_clicked(event.pos):
                self.inventory.toggle_visibility()
                return None

            # граница инвентаря
            inventory_top = self.screen_height - 100

            # 1‑я комната, выбран zapiska и клик выше инвентаря -> открыть записку и не отправлять событие в комнату
            if (
                isinstance(current_room, Room1)
                and self.inventory.get_selected_item() == "zapiska"
                and y < inventory_top
            ):
                current_room.open_note_from_inventory()
                return None

        # --- инвентарь ---
        self.inventory.handle_event(event)
        selected_item = self.inventory.get_selected_item()

        # --- условия двери ---
        cat_statues = ["serebro_cat", "black_cat", "med_cat"]
        has_all_statues = all(self.inventory.has_item(statue) for statue in cat_statues)

        # --- событие комнаты ---
        room_result = current_room.handle_event(event, selected_item, has_all_statues)

        if not room_result:
            return None

        # --- разбор результата комнаты ---
        if room_result.startswith("add_"):
            self.inventory.add_item(room_result[4:])
        elif room_result.startswith("remove_"):
            self.inventory.remove_item(room_result[7:])
        elif room_result == "next_room":
            self.current_room = (self.current_room + 1) % 3
        elif room_result == "prev_room":
            self.current_room = (self.current_room - 1) % 3
        elif room_result == "door_puzzle":
            if self.check_door_conditions():
                return "door_solved"
        elif room_result in (
            "painting_completed",
            "note_safe_opened",
            "symbol_safe_opened",
            "scroll_puzzle_solved",
        ):
            pass

        return None
