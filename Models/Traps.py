from Models.BaseObject import Object
import pygame


class Fire(Object):
    ANIMATION_DELAY = 5

    def __init__(self, app, x, y, width, height):
        super().__init__(app, x, y, width, height)
        self.fire = self.app.sprites.loaded_sprites["Fire"]
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "on"
        self.cause_damage = True
        self.off_count = 0

    def on(self):
        self.animation_name = "on"
        self.cause_damage = True
        self.animation_count = 0

    def off(self):
        self.animation_name = "off"
        self.off_count = 0
        self.cause_damage = False
        self.animation_count = 0

    def handle_player_hit(self):
        self.off()

    def loop(self):
        if self.animation_name == "off":
            self.off_count += 1
            if self.off_count == 100:
                self.on()
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0
