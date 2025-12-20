import pygame
import time
from button import Button


class DoorPuzzle:
    def __init__(self, screen_width, screen_height, inventory):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.inventory = inventory
        self.background = None
        self.statues_used = []
        self.load_background()

    def load_background(self):
        try:
            self.background = pygame.image.load("assets/history.png")
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except:
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((0, 0, 0))

    def show_ending(self, screen):
        """Показ финальной истории"""
        try:
            with open("data/finish.txt", "r", encoding="utf-8") as file:
                story_text = file.read()
        except:
            story_text = "Поздравляем! Вы завершили игру!"

        font = pygame.font.SysFont("Arial", 24)
        words = story_text.split()
        current_text = ""
        start_time = time.time()
        word_delay = 0.5

        showing = True
        while showing:
            current_time = time.time() - start_time
            words_to_show = min(len(words), int(current_time / word_delay))

            screen.blit(self.background, (0, 0))

            if words_to_show < len(words):
                current_text = " ".join(words[:words_to_show])
            else:
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

    def run(self, screen):
        # Проверяем, есть ли все статуэтки
        required_statues = ["serebro_cat", "black_cat", "med_cat"]
        has_all_statues = all(statue in self.inventory for statue in required_statues)
        has_anibus = "anibus" in self.inventory

        if not has_all_statues or not has_anibus:
            # Показываем сообщение, что нужны все статуэтки и анибус
            font = pygame.font.SysFont("Arial", 36)
            message = "Нужны все статуэтки котов и анибус чтобы открыть дверь!"
            text_surface = font.render(message, True, (255, 255, 255))

            screen.blit(self.background, (0, 0))
            screen.blit(text_surface, (self.screen_width // 2 - text_surface.get_width() // 2,
                                       self.screen_height // 2 - text_surface.get_height() // 2))

            back_btn = Button(self.screen_width // 2 - 50, self.screen_height // 2 + 50, "Назад", lambda: "back")
            back_btn.check_hover(pygame.mouse.get_pos())
            back_btn.draw(screen)

            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return "exit"
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if back_btn.rect.collidepoint(event.pos):
                            return "back"
            return "back"
        else:
            # Все условия выполнены - показываем финальную заставку
            if self.show_ending(screen):
                return "game_completed"
            else:
                return "exit"
