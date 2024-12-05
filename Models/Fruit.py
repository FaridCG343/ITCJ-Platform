from Models.BaseObject import Object
import pygame


class Fruit(Object):
    ANIMATION_DELAY = 5
    SCORE = {
        "apple": 100,
        "banana": 200,
        "cherry": 300,
        "grapes": 400,
        "orange": 500,
        "peach": 600,
        "pear": 700,
        "strawberry": 800,
        "watermelon": 900
    }

    def __init__(self, app, x, y, width, height, name):
        super().__init__(app, x, y, width, height)
        self.fruits = self.app.sprites.loaded_sprites["fruits"][name]
        self.image = self.fruits[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.score = self.SCORE[name]

    # def loop(self):
    #     sprites = self.fruits
    #     sprite_index = (self.animation_count // 10) % len(sprites)
    #     self.image = sprites[sprite_index]
    #     self.animation_count += 1
    #     self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
    #     self.mask = pygame.mask.from_surface(self.image)
    #     if self.animation_count // self.ANIMATION_DELAY > len(sprites):
    #         self.animation_count = 0
