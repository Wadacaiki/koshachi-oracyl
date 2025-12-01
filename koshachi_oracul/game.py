import pygame
import time
from room1 import Room1
from room2 import Room2
from room3 import Room3
from door_puzzle import DoorPuzzle


class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_room = 0
        self.rooms = [Room1(screen_width, screen_height),
                      Room2(screen_width, screen_height),
                      Room3(screen_width, screen_height)]
        self.inventory = []
        self.inventory_visible = True
        self.story_shown = False
        self.game_completed = False

    def show_story(self, screen):
        """Показ начальной истории"""
        try:
            background = pygame.image.load("assets/history.png")
            background = pygame.transform.scale(background, (self.screen_width, self.screen_height))
        except:
            background = pygame.Surface((self.screen_width, self.screen_height))
            background.fill((0, 0, 0))

        try:
            with open("data/start.txt", "r", encoding="utf-8") as file:
                story_text = file.read()
        except:
            story_text = "Добро пожаловать в игру!"

        font = pygame.font.SysFont("Arial", 24)
        words = story_text.split()
        current_text = ""
        start_time = time.time()
        word_delay = 0.5  # Задержка между словами

        showing = True
        while showing:
            current_time = time.time() - start_time
            words_to_show = min(len(words), int(current_time / word_delay))

            screen.blit(background, (0, 0))

            if words_to_show < len(words):
                current_text = " ".join(words[:words_to_show])
            else:
                # Весь текст показан, ждем 10 секунд
                if current_time > len(words) * word_delay + 10:
                    showing = False
                current_text = story_text

            # Разбиваем текст на строки
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

            # Отображаем строки
            y_pos = self.screen_height // 2 - (len(lines) * 30) // 2
            for line in lines:
                text_surface = font.render(line, True, (255, 255, 255))
                screen.blit(text_surface, (50, y_pos))
                y_pos += 30

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return True

        return True

    def draw_inventory(self, screen):
        if not self.inventory_visible:
            return

        try:
            inventory_bg = pygame.image.load("assets/inentar.png")
            inventory_bg = pygame.transform.scale(inventory_bg, (self.screen_width, 100))
            screen.blit(inventory_bg, (0, self.screen_height - 100))
        except:
            pygame.draw.rect(screen, (100, 100, 100), (0, self.screen_height - 100, self.screen_width, 100))

        # Рисуем предметы в инвентаре
        item_size = 80
        margin = 10
        for i, item in enumerate(self.inventory):
            try:
                item_img = pygame.image.load(f"assets/{item}.png")
                item_img = pygame.transform.scale(item_img, (item_size, item_size))
                screen.blit(item_img, (margin + i * (item_size + margin), self.screen_height - 90))
            except:
                pygame.draw.rect(screen, (200, 200, 200),
                                 (margin + i * (item_size + margin), self.screen_height - 90, item_size, item_size))

    def add_to_inventory(self, item):
        if item not in self.inventory:
            self.inventory.append(item)

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def run(self, screen):
        if not self.story_shown:
            if not self.show_story(screen):
                return "exit"
            self.story_shown = True

        # Проверяем, собраны ли все статуэтки для двери
        cat_statues = ["serebro_cat", "black_cat", "med_cat"]
        has_all_statues = all(statue in self.inventory for statue in cat_statues)

        running = True
        while running:
            current_room = self.rooms[self.current_room]

            # Обновляем инвентарь в комнате
            current_room.inventory = self.inventory
            current_room.add_to_inventory = self.add_to_inventory
            current_room.remove_from_inventory = self.remove_from_inventory

            result = current_room.draw(screen, has_all_statues)

            if result == "next_room":
                self.current_room = (self.current_room + 1) % 3
            elif result == "prev_room":
                self.current_room = (self.current_room - 1) % 3
            elif result == "door_puzzle":
                door_puzzle = DoorPuzzle(self.screen_width, self.screen_height, self.inventory)
                puzzle_result = door_puzzle.run(screen)
                if puzzle_result == "game_completed":
                    self.game_completed = True
                    return "main_menu"
            elif result == "exit":
                return "main_menu"

            self.draw_inventory(screen)

            # Кнопка скрытия/показа инвентаря
            inventory_btn_rect = pygame.Rect(self.screen_width - 50, self.screen_height - 120, 40, 40)
            pygame.draw.rect(screen, (139, 69, 19), inventory_btn_rect, border_radius=5)
            font = pygame.font.SysFont("Arial", 20)
            btn_text = "↑" if not self.inventory_visible else "↓"
            text_surface = font.render(btn_text, True, (255, 255, 255))
            screen.blit(text_surface, (inventory_btn_rect.centerx - text_surface.get_width() // 2,
                                       inventory_btn_rect.centery - text_surface.get_height() // 2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if inventory_btn_rect.collidepoint(event.pos):
                        self.inventory_visible = not self.inventory_visible

                room_result = current_room.handle_event(event, has_all_statues)
                if room_result:
                    if room_result.startswith("add_"):
                        self.add_to_inventory(room_result[4:])
                    elif room_result.startswith("remove_"):
                        self.remove_from_inventory(room_result[7:])
                    elif room_result == "next_room":
                        self.current_room = (self.current_room + 1) % 3
                    elif room_result == "prev_room":
                        self.current_room = (self.current_room - 1) % 3
                    elif room_result == "door_puzzle":
                        door_puzzle = DoorPuzzle(self.screen_width, self.screen_height, self.inventory)
                        puzzle_result = door_puzzle.run(screen)
                        if puzzle_result == "game_completed":
                            self.game_completed = True
                            return "main_menu"

        return "main_menu"