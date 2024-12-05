from os.path import join, isfile
from os import listdir
import pygame


def flip(sprites: list):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect((96, 0, size, size))  # 96 is the x position of the block in the image
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


class Sprites:
    def __init__(self):
        character = "ITCJGuy"
        self.loaded_sprites = {'blocks': {}, 'items': {}, 'text': {}}
        self.load_sprite_sheets("MainCharacters", character, 32, 32, True)
        self.load_sprite_sheets("Traps", "Fire", 16, 32)
        self.load_image(["assets", "Other", "heart.png"], "heart", (32, 32), (0, 0))
        self.load_image(["assets", "Background", "nature_4", "origbig.png"], "background")
        self.load_sprite(["assets", "MainCharacters", "Disappearing (96x96).png"], character,
                         "disappear", (96, 96), (0, 0), direction=True)
        self.load_sprite(["assets", "Items", "Fruits", "Apple.png"],
                         "fruits", "apple", (32, 32), (0, 0), scale2x=True)
        self.load_sprite(["assets", "Items", "Fruits", "Bananas.png"],
                         "fruits", "banana", (32, 32), (0, 0), scale2x=True)
        self.load_sprite(["assets", "Items", "Checkpoints", "Checkpoint", "Checkpoint (Flag Idle)(64x64).png"],
                         "checkpoints", "idle", (64, 64), (0, 0), scale2x=True)
        self.load_sprite(["assets", "Items", "Checkpoints", "Checkpoint", "Checkpoint (No Flag).png"],
                         "checkpoints", "no_flag", (64, 64), (0, 0), scale2x=True)
        self.load_sprite(["assets", "Items", "Checkpoints", "Checkpoint", "Checkpoint (Flag Out) (64x64).png"],
                         "checkpoints", "flag_out", (64, 64), (0, 0), scale2x=True)
        # a - j
        char = 'a'
        for i in range(10):
            self.load_image(["assets", "Menu", "Text", "TextB.png"], char, (8, 10), (i * 8, 0), "text")
            char = chr(ord(char) + 1)
        # k - t
        for i in range(10):
            self.load_image(["assets", "Menu", "Text", "TextB.png"], char, (8, 10), (i * 8, 10), "text")
            char = chr(ord(char) + 1)
        # u - z
        for i in range(6):
            self.load_image(["assets", "Menu", "Text", "TextB.png"], char, (8, 10), (i * 8, 20), "text")
            char = chr(ord(char) + 1)
        # 0 - 9
        for i in range(10):
            self.load_image(["assets", "Menu", "Text", "TextB.png"], str(i), (8, 10), (i * 8, 30), "text")
        # symbols
        # . , : ? ! ( ) + -
        for i, char in enumerate([".", ",", ":", "?", "!", "(", ")", "+", "-"]):
            self.load_image(["assets", "Menu", "Text", "TextB.png"], char, (8, 10), (i * 8, 40), "text")



    def load_sprite_sheets(self, dir1, dir2, width, height, direction=False):
        path = join("assets", dir1, dir2)
        images = [f for f in listdir(path) if isfile(join(path, f))]
        self.loaded_sprites[dir2] = {}

        for image in images:
            sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

            sprites = []
            for i in range(sprite_sheet.get_width() // width):
                sprite = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                rect = pygame.Rect((i * width, 0, width, height))
                sprite.blit(sprite_sheet, (0, 0), rect)
                sprite = pygame.transform.scale2x(sprite)
                sprites.append(sprite)

            if direction:
                self.loaded_sprites[dir2][image.replace(".png", "") + "_right"] = sprites
                self.loaded_sprites[dir2][image.replace(".png", "") + "_left"] = flip(sprites)
            else:
                self.loaded_sprites[dir2][image.replace(".png", "")] = sprites

    # size is the size of the sprite and start is the starting position of the sprite in the image
    def load_sprite(self, path: list, source: str, name: str, size: tuple, start: tuple, scale2x=False,
                    direction=False):
        path = join(*path)
        image = pygame.image.load(path).convert_alpha()
        sprites = []
        for i in range(image.get_width() // size[0]):
            sprite = pygame.Surface(size, pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * size[0] + start[0], start[1], *size)
            sprite.blit(image, (0, 0), rect)
            if scale2x:
                sprite = pygame.transform.scale2x(sprite)
            sprites.append(sprite)
        if source not in self.loaded_sprites:
            self.loaded_sprites[source] = {}
        if direction:
            self.loaded_sprites[source][name + "_right"] = sprites
            self.loaded_sprites[source][name + "_left"] = flip(sprites)
        else:
            self.loaded_sprites[source][name] = sprites

    def load_block(self, size):
        path = join("assets", "Terrain", "Terrain.png")
        image = pygame.image.load(path).convert_alpha()
        surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        rect = pygame.Rect((96, 0, size, size))  # 96 is the x position of the block in the image
        surface.blit(image, (0, 0), rect)
        self.loaded_sprites['blocks'][f'block_{size}'] = pygame.transform.scale2x(surface)

    def load_image(self, path: list, name: str, size: tuple = None, start: tuple = (0, 0), source="items"):
        image = pygame.image.load(join(*path)).convert_alpha()
        if size is None:
            size = image.get_size()
        surface = pygame.Surface(size, pygame.SRCALPHA, 32)
        rect = pygame.Rect((*start, *size))
        surface.blit(image, (0, 0), rect)
        if source not in self.loaded_sprites:
            self.loaded_sprites[source] = {}
        self.loaded_sprites[source][name] = surface
        return surface
