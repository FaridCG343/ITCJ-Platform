from Models.BaseObject import Object
import pygame


class Checkpoint(Object):
    ANIMATION_DELAY = 5

    def __init__(self, app, x, y):
        self.checkpoints = app.sprites.loaded_sprites["checkpoints"]
        self.animation_name = "no_flag"
        self.image = self.checkpoints[self.animation_name][0]
        super().__init__(app, x, y, self.image.get_width(), self.image.get_height())
        self.animation_count = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.cause_damage = False
        self.app = app
        self.checked = False

    def handle_player_hit(self):
        if self.checked:
            return
        self.checked = True
        self.animation_name = "flag_out"
        self.animation_count = 0

    def loop(self):
        sprites = self.checkpoints[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            if self.animation_name == "flag_out":
                self.animation_name = "idle"
            self.animation_count = 0
