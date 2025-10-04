import pygame as pg

class BaseEntity(pg.sprite.Sprite):
    def __init__(self, size, visuals):
        super().__init__()
        if type(visuals) == pg.color.Color:
            self.image = pg.Surface(size)
            self.image.fill(visuals)
        elif type(visuals) == str:
            self.image = pg.image.load(visuals).convert_alpha()
            self.image = pg.transform.scale(self.image, size)
        self.rect = self.image.get_rect()



    def draw(self, surface: pg.Surface):
        surface.blit(self.image, self.rect)
