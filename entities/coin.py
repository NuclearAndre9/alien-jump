import pygame as pg
from entities.base_entity import BaseEntity
from global_variables import *

WIDTH, HEIGHT = (TILE_SIZE / 2, TILE_SIZE / 2)


class Coin(BaseEntity):
    def __init__(self):
        super().__init__((WIDTH, HEIGHT), "sprites/coin.png")
        # super().__init__((0, 0), (WIDTH, HEIGHT), pg.Color("yellow"))

    def update(self, player):
        pg.sprite.spritecollide(player, game_coin, True)

    def respawn(self, position):
        self.rect.center = position
        game_coin.add(self)
