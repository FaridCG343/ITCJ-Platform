import pygame


class Object(pygame.sprite.Sprite):
    def __init__(self, app, x, y, width, height, name=None):
        super().__init__()
        self.app = app
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.width = width
        self.height = height
        self.name = name
        self.cause_damage = False

    def draw(self, offset_x):
        self.app.window.blit(self.image, (self.rect.x - offset_x, self.rect.y))

    def handle_player_hit(self):
        ...


class Block(Object):
    def __init__(self, app, x, y, size):
        super().__init__(app, x, y, size, size)
        if f"block_{size}" not in app.sprites.loaded_sprites["blocks"]:
            app.sprites.load_block(size)
        block = app.sprites.loaded_sprites["blocks"][f"block_{size}"]
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
