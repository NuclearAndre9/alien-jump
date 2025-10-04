import pygame as pg
from entities.base_entity import BaseEntity
from global_variables import *
import random as rd

WIDTH, HEIGHT = (int(TILE_SIZE / 2), int(TILE_SIZE / 2))
MAX_SPEED = 10
SPAWN_HEIGHT = 100
SPAWN_RATE = 10


class Enemy(BaseEntity):
    def __init__(self):
        super().__init__((WIDTH, HEIGHT), "sprites/meteorite.png")
        self.velocity = 0
        self.position = 0
        self.respawn()

    def fall(self):
        self.velocity = GRAVITY

    def update_movement(self):
        self.position = self.velocity
        self.rect.move_ip(0, self.position)

    def respawn(self):
        if rd.randint(1, SPAWN_RATE) != 1:
            return

        pos_x = rd.randint(LEFT_SIDE, RIGHT_SIDE - WIDTH)
        pos_y = -rd.randint(TOP_SIDE, SPAWN_HEIGHT)
        self.rect.topleft = (pos_x, pos_y)
        self.velocity = 0
        alive_enemies.add(self)

    def update(self, player):
        # desaparecer si toca el suelo o al personaje
        player_collision = self.rect.colliderect(player.rect)
        ground_collision = any(pg.sprite.spritecollide(self, level, False))

        if player_collision:
            player.kill()

        if ground_collision:
            self.kill()
            death_enemies.add(self)

        if not alive_enemies.has(self):
            self.respawn()
        # reaparecer en posición al azar si toca el suelo hasta arriba
        self.fall()
        self.update_movement()
