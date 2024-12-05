import pygame
from Models.BaseObject import Object


class Text(Object):
    def __init__(self, app, x, y, text, size, color=(255, 255, 255)):
        super().__init__(app, x, y, 0, 0)
        self.text = text
        self.size = size
        self.color = color
        self.font = pygame.font.Font(self.app.font_path, size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect(topleft=(x, y))

    def set_text(self, text):
        self.text = text
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))


class FixedText(Text):
    def draw(self, offset_x=0):
        self.app.window.blit(self.image, (self.rect.x, self.rect.y))
