import pygame


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = None
    ANIMATION_DELAY = 4

    def __init__(self, app, x, y, width, height):
        super().__init__()
        self.lives = 3
        self.app = app
        self.SPRITES = app.sprites.loaded_sprites["ITCJGuy"]
        self.rect = pygame.Rect(x, y, width, height)
        self.x_velocity = 0
        self.y_velocity = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.sprite = self.SPRITES["idle_left"][0]
        self.jump_count = 0
        self.get_hit = False
        self.hit_count = 0
        self.invincible = False

    def jump(self):
        if self.jump_count == 2:
            return
        self.y_velocity = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, velocity):
        self.x_velocity = -velocity
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, velocity):
        self.x_velocity = velocity
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def landed(self):
        self.y_velocity = 0
        self.fall_count = 0
        self.jump_count = 0

    def hit_head(self):
        self.y_velocity *= -1

    def hit(self):
        self.get_hit = True
        self.invincible = True
        self.hit_count = 0
        self.lives -= 1

    def loop(self, fps, ignore_gravity=False):
        if not ignore_gravity:
            self.y_velocity += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_velocity, self.y_velocity)

        if self.get_hit:
            self.hit_count += 1
            if self.hit_count > fps * 2:
                self.get_hit = False
                self.invincible = False

        self.fall_count += 1
        self.update_sprite()

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.lives == 0:
            sprite_sheet = "disappear"
        elif self.get_hit:
            sprite_sheet = "hit"
        elif self.y_velocity < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_velocity > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_velocity != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        if sprite_sheet == "disappear" and sprite_index == len(sprites) - 1:
            self.app.game_over_status = True
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, offset_x):
        self.app.window.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))
