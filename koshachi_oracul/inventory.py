import pygame


class Inventory:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.items = []
        self.selected_item = None
        self.visible = True
        self.item_size = 80
        self.margin = 10

        try:
            bg = pygame.image.load("assets/inentar.png").convert_alpha()
            self.background = pygame.transform.scale(bg, (self.screen_width, 100))
        except:
            self.background = pygame.Surface((self.screen_width, 100))
            self.background.fill((100, 100, 100))

        self.fallback_font = pygame.font.SysFont("Arial", 12)
        self.item_images = {}  # cache: имя -> Surface

    def _get_item_image(self, item):
        if item in self.item_images:
            return self.item_images[item]
        try:
            img = pygame.image.load(f"assets/{item}.png").convert_alpha()
            img = pygame.transform.scale(img, (self.item_size, self.item_size))
            self.item_images[item] = img
            return img
        except:
            self.item_images[item] = None
            return None

    def add_item(self, item_name):
        if item_name not in self.items:
            self.items.append(item_name)

    def remove_item(self, item_name):
        if item_name in self.items:
            self.items.remove(item_name)
            if self.selected_item == item_name:
                self.selected_item = None

    def has_item(self, item_name):
        return item_name in self.items

    def get_selected_item(self):
        return self.selected_item

    def toggle_visibility(self):
        self.visible = not self.visible

    def draw(self, screen):
        if not self.visible:
            return

        screen.blit(self.background, (0, self.screen_height - 100))

        for i, item in enumerate(self.items):
            x = self.margin + i * (self.item_size + self.margin)
            y = self.screen_height - 90

            img = self._get_item_image(item)
            if img is not None:
                screen.blit(img, (x, y))
                if item == self.selected_item:
                    pygame.draw.rect(
                        screen,
                        (255, 255, 0),
                        (x - 2, y - 2, self.item_size + 4, self.item_size + 4),
                        3,
                    )
            else:
                color = (200, 200, 200) if item != self.selected_item else (255, 255, 0)
                pygame.draw.rect(screen, color, (x, y, self.item_size, self.item_size))
                text = self.fallback_font.render(item, True, (0, 0, 0))
                screen.blit(text, (x + 5, y + 5))

    def handle_click(self, pos):
        if not self.visible:
            return None

        x, y = pos
        for i, item in enumerate(self.items):
            item_x = self.margin + i * (self.item_size + self.margin)
            item_y = self.screen_height - 90
            if item_x <= x <= item_x + self.item_size and item_y <= y <= item_y + self.item_size:
                self.selected_item = None if item == self.selected_item else item
                return item
        return None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.handle_click(event.pos)
        return None
