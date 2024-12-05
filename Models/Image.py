from Models.BaseObject import Object


class Image(Object):
    def __init__(self, app, x, y, name):
        super().__init__(app, x, y, 0, 0, name)
        self.image = app.sprites.loaded_sprites["items"][name]
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, offset_x):
        self.app.window.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class FixedImage(Image):
    def draw(self, offset_x):
        self.app.window.blit(self.image, (self.rect.x, self.rect.y))