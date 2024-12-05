import math
import pygame
from os.path import join
from Models.Player import Player
from Models.Traps import Fire
from Models.BaseObject import Block
from Models.Text import FixedText
from Models.Image import FixedImage
from Sprites import Sprites
from Models.Fruit import Fruit
from Models.Checkpoints import Checkpoint


class MainWindow:
    WIDTH, HEIGHT = 1000, 800
    FPS = 60
    PLAYER_VELOCITY = 5

    def __init__(self):
        self.clock = None
        pygame.init()
        pygame.display.set_caption("ITCJ - Juego de Plataforma")
        self.font_path = join('assets', 'Fonts', 'pixel_operator', 'PixelOperator-Bold.ttf')
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.sprites = Sprites()
        self.background_image = self.sprites.loaded_sprites["items"]["background"]
        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))
        self.player = None
        self.life_text = None
        self.objects = []
        self.non_physics_objects = []  # Objects that don't need to be checked for collision
        self.game_over_text = FixedText(self, self.WIDTH // 2, self.HEIGHT // 2, "Game Over", 64, (255, 0, 0))
        self.game_over_options = [
            FixedText(self, self.WIDTH // 2, self.HEIGHT // 2 + 64, "Press ESC to exit", 32, (0, 0, 0)),
            FixedText(self, self.WIDTH // 2, self.HEIGHT // 2 + 96, "Press R to restart", 32, (0, 0, 0))
        ]
        self.win_text = FixedText(self, self.WIDTH // 2, self.HEIGHT // 2, "You Win!", 64, (0, 255, 0))
        self.win_score_text = FixedText(self, self.WIDTH // 2, self.HEIGHT // 2 + 64, "Your score: ", 32, (0, 0, 0))
        self.win_options = [
            FixedText(self, self.WIDTH // 2, self.HEIGHT // 2 + 96, "Press ESC to exit", 32, (0, 0, 0)),
            FixedText(self, self.WIDTH // 2, self.HEIGHT // 2 + 128, "Press R to restart", 32, (0, 0, 0))
        ]
        self.goal = None
        self.offset_x = 0
        self.game_over_status = False
        self.score = 0
        self.score_text = None
        self.win_status = False
        self.init_game()

    def init_game(self):
        self.player = Player(self, 100, self.HEIGHT - 100, 50, 50)
        self.score = 0
        self.score_text = FixedText(self, self.WIDTH - 175, 5, f"Score: {self.score}", 32, (255, 255, 255))
        self.life_text = FixedText(self, 40, 4, f"x{self.player.lives}", 32, (50, 50, 50))
        self.goal = Checkpoint(self, 96 * 50, self.HEIGHT - 96 - 128)
        self.load_objects()
        self.offset_x = 0
        self.game_over_status = False
        self.win_status = False

    def load_objects(self):
        block_size = 96
        blocks = [Block(self, i * block_size, self.HEIGHT - block_size, block_size)
                  for i in range(5 * math.ceil(self.WIDTH / block_size))]
        blocks.extend([Block(self, 0, self.HEIGHT - block_size * i, block_size)
                       for i in range(2, math.ceil(self.HEIGHT / block_size))])
        blocks.append(Block(self, block_size * 3, self.HEIGHT - block_size * 4, block_size))
        blocks.append(Block(self, block_size * 4, self.HEIGHT - block_size * 4, block_size))
        blocks.append(Block(self, block_size * 5, self.HEIGHT - block_size * 4, block_size))
        blocks.append(Block(self, block_size * 6, self.HEIGHT - block_size * 4, block_size))
        blocks.append(Block(self, block_size * 9, self.HEIGHT - block_size * 4, block_size))
        blocks.append(Block(self, block_size * 11, self.HEIGHT - block_size * 2, block_size))
        blocks.append(Block(self, block_size * 11, self.HEIGHT - block_size * 6, block_size))
        blocks.append(Block(self, block_size * 12, self.HEIGHT - block_size * 6, block_size))
        blocks.append(Block(self, block_size * 13, self.HEIGHT - block_size * 6, block_size))
        blocks.append(Block(self, block_size * 14, self.HEIGHT - block_size * 6, block_size))
        blocks.append(Block(self, block_size * 16, self.HEIGHT - block_size * 2, block_size))
        blocks.append(Block(self, block_size * 16, self.HEIGHT - block_size * 3, block_size))
        blocks.append(Block(self, block_size * 16, self.HEIGHT - block_size * 4, block_size))
        blocks.append(Block(self, block_size * 17, self.HEIGHT - block_size * 3, block_size))
        blocks.append(Block(self, block_size * 18, self.HEIGHT - block_size * 3, block_size))
        blocks.append(Block(self, block_size * 22, self.HEIGHT - block_size * 2, block_size))
        blocks.append(Block(self, block_size * 22, self.HEIGHT - block_size * 3, block_size))

        blocks.append(Block(self, block_size * 25, self.HEIGHT - block_size * 4, block_size))
        blocks.append(Block(self, block_size * 28, self.HEIGHT - block_size * 2, block_size))
        blocks.append(Block(self, block_size * 28, self.HEIGHT - block_size * 3, block_size))
        blocks.append(Block(self, block_size * 28, self.HEIGHT - block_size * 4, block_size))
        blocks.append(Block(self, block_size * 30, self.HEIGHT - block_size * 2, block_size))
        blocks.append(Block(self, block_size * 30, self.HEIGHT - block_size * 6, block_size))
        blocks.append(Block(self, block_size * 32, self.HEIGHT - block_size * 7, block_size))

        blocks.append(Block(self, block_size * 34, self.HEIGHT - block_size * 2, block_size))
        blocks.append(Block(self, block_size * 35, self.HEIGHT - block_size * 2, block_size))
        blocks.append(Block(self, block_size * 35, self.HEIGHT - block_size * 3, block_size))
        blocks.append(Block(self, block_size * 36, self.HEIGHT - block_size * 2, block_size))
        blocks.append(Block(self, block_size * 36, self.HEIGHT - block_size * 3, block_size))
        blocks.append(Block(self, block_size * 36, self.HEIGHT - block_size * 4, block_size))
        blocks.append(Block(self, block_size * 37, self.HEIGHT - block_size * 2, block_size))
        blocks.append(Block(self, block_size * 37, self.HEIGHT - block_size * 3, block_size))
        blocks.append(Block(self, block_size * 37, self.HEIGHT - block_size * 4, block_size))
        blocks.append(Block(self, block_size * 37, self.HEIGHT - block_size * 5, block_size))

        blocks.append(Block(self, block_size * 40, self.HEIGHT - block_size * 2, block_size))
        blocks.append(Block(self, block_size * 40, self.HEIGHT - block_size * 3, block_size))
        blocks.append(Block(self, block_size * 40, self.HEIGHT - block_size * 4, block_size))
        blocks.append(Block(self, block_size * 40, self.HEIGHT - block_size * 5, block_size))
        blocks.append(Block(self, block_size * 41, self.HEIGHT - block_size * 2, block_size))
        blocks.append(Block(self, block_size * 41, self.HEIGHT - block_size * 3, block_size))
        blocks.append(Block(self, block_size * 41, self.HEIGHT - block_size * 4, block_size))
        blocks.append(Block(self, block_size * 42, self.HEIGHT - block_size * 2, block_size))
        blocks.append(Block(self, block_size * 42, self.HEIGHT - block_size * 3, block_size))
        blocks.append(Block(self, block_size * 43, self.HEIGHT - block_size * 2, block_size))

        # Fruits
        fruits = [
            Fruit(self, block_size * 3 + 16, self.HEIGHT - 48 - (block_size * 4), 32, 32, "banana"),
            Fruit(self, block_size * 6 + 16, self.HEIGHT - 48 - (block_size * 4), 32, 32, "apple"),
            Fruit(self, block_size * 12 + 16, self.HEIGHT - 48 - (block_size * 6), 32, 32, "apple"),
            Fruit(self, block_size * 13 + 16, self.HEIGHT - 48 - (block_size * 6), 32, 32, "apple"),
            Fruit(self, block_size * 17 + 16, self.HEIGHT - 48 - (block_size * 1), 32, 32, "banana"),
            Fruit(self, block_size * 30 + 16, self.HEIGHT - 48 - (block_size * 6), 32, 32, "apple"),
            Fruit(self, block_size * 30 + 16, self.HEIGHT - 48 - (block_size * 2), 32, 32, "banana"),
            Fruit(self, block_size * 32 + 16, self.HEIGHT - 48 - (block_size * 7), 32, 32, "banana"),
            Fruit(self, block_size * 37 + 16, self.HEIGHT - 48 - (block_size * 5), 32, 32, "apple"),
            Fruit(self, block_size * 40 + 16, self.HEIGHT - 48 - (block_size * 5), 32, 32, "banana"),
            Fruit(self, block_size * 60 + 16, self.HEIGHT - 48 - (block_size * 1), 32, 32, "banana"),
        ]

        # Traps
        traps = [
            Fire(self, block_size * 12 + 32, self.HEIGHT - 64 - (block_size * 1), 16, 32),
            Fire(self, block_size * 13 + 32, self.HEIGHT - 64 - (block_size * 1), 16, 32),
            Fire(self, block_size * 14 + 32, self.HEIGHT - 64 - (block_size * 1), 16, 32),
            Fire(self, block_size * 15 + 32, self.HEIGHT - 64 - (block_size * 1), 16, 32),
            Fire(self, block_size * 29 + 32, self.HEIGHT - 64 - (block_size * 1), 16, 32),
            Fire(self, block_size * 31 + 32, self.HEIGHT - 64 - (block_size * 1), 16, 32),
            Fire(self, block_size * 32 + 32, self.HEIGHT - 64 - (block_size * 1), 16, 32),
            Fire(self, block_size * 33 + 32, self.HEIGHT - 64 - (block_size * 1), 16, 32),
            Fire(self, block_size * 38 + 32, self.HEIGHT - 64 - (block_size * 1), 16, 32),
            Fire(self, block_size * 39 + 32, self.HEIGHT - 64 - (block_size * 1), 16, 32),
        ]

        self.objects = [
            *blocks,
            *fruits,
            *traps,
            self.goal
        ]
        # Fruit(self, 100, self.HEIGHT - block_size - 64, 32, 32, "apple"),
        # Fire(self, 1000, self.HEIGHT - block_size - 64, 16, 32)

        self.non_physics_objects = [FixedImage(self, 5, 5, "heart"),
                                    self.life_text, self.score_text]


    def draw(self) -> None:
        self.window.blit(self.background_image, (0, 0))

        if not self.game_over_status:
            self.player.draw(self.offset_x)

        for obj in self.objects:
            obj.draw(self.offset_x)

        for obj in self.non_physics_objects:
            obj.draw(self.offset_x)

        pygame.display.update()

    def handle_vertical_collision(self, dy: int):
        collided_objects = []
        for obj in self.objects:
            if pygame.sprite.collide_mask(self.player, obj):
                if not (isinstance(obj, Fruit) or isinstance(obj, Checkpoint)):
                    if dy > 0:
                        self.player.rect.bottom = obj.rect.top
                        self.player.landed()
                    elif dy < 0:
                        self.player.rect.top = obj.rect.bottom
                        self.player.hit_head()
                collided_objects.append(obj)

        return collided_objects

    def collide(self, dx):
        self.player.move(dx, 0)
        self.player.update()
        collided_object = None
        for obj in self.objects:
            if isinstance(obj, Fruit) or isinstance(obj, Checkpoint):
                continue
            if pygame.sprite.collide_mask(self.player, obj):
                collided_object = obj
                break

        self.player.move(-dx, 0)
        self.player.update()
        return collided_object

    def handle_movement(self):
        self.player.x_velocity = 0
        keys = pygame.key.get_pressed()

        collide_left = self.collide(-self.PLAYER_VELOCITY * 2)
        collide_right = self.collide(self.PLAYER_VELOCITY * 2)

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not collide_left:
            self.player.move_left(self.PLAYER_VELOCITY)
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not collide_right:
            self.player.move_right(self.PLAYER_VELOCITY)

        vertical_collide = self.handle_vertical_collision(self.player.y_velocity)
        to_check = [collide_left, collide_right, *vertical_collide]

        fruit_to_remove = None
        for obj in to_check:
            if obj is not None and obj.cause_damage and not self.player.invincible:
                self.player.hit()
                self.life_text.set_text(f"x{self.player.lives}")
                obj.handle_player_hit()
            if obj is not None and isinstance(obj, Fruit):
                fruit_to_remove = obj
                self.score += fruit_to_remove.score
                self.score_text.set_text(f"Score: {self.score}")
                self.objects.remove(fruit_to_remove)
            if obj is not None and isinstance(obj, Checkpoint):
                obj.handle_player_hit()
                self.win_status = True


    def game_over(self):
        running = True
        self.non_physics_objects.append(self.game_over_text)
        self.non_physics_objects.extend(self.game_over_options)
        while running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    # Exit the game
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    # Restart the game
                    self.init_game()
                    running = False

    def win(self):
        running = True
        self.non_physics_objects.append(self.win_text)
        self.win_score_text.set_text(f"Your score: {self.score}")
        self.non_physics_objects.append(self.win_score_text)
        self.non_physics_objects.extend(self.win_options)
        while running:
            self.clock.tick(self.FPS)
            self.player.y_velocity = 0
            self.player.x_velocity = 0
            self.player.loop(self.FPS, ignore_gravity=True)
            self.goal.loop()
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    # Exit the game
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    # Restart the game
                    self.init_game()
                    running = False

    def main(self):
        self.clock = pygame.time.Clock()
        scroll_area_width = 200

        running = True
        while running:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                    break
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.player.jump()

            for obj in self.objects:
                if callable(getattr(obj, "loop", None)):
                    obj.loop()
            self.player.loop(self.FPS)
            self.draw()
            if self.game_over_status:
                self.game_over()
            if self.win_status:
                self.win()
            if self.player.lives:
                self.handle_movement()


            if (self.player.rect.right - self.offset_x >= self.WIDTH - scroll_area_width and self.player.x_velocity > 0)\
                    or (self.player.rect.left - self.offset_x <= scroll_area_width and self.player.x_velocity < 0):
                self.offset_x += self.player.x_velocity

        pygame.quit()
        quit()


if __name__ == "__main__":
    app = MainWindow()
    app.main()
