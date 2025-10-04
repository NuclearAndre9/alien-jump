import pygame as pg
from global_variables import *
import colors as cs
from entities.base_entity import BaseEntity

WIDTH = SCREENHEIGTH
HEIGHT = 20

level_layout = [
    '          ',
    '          ',
    '          ',
    '      --  ',
    '-     -- -',
    '--  - ## -',
    '#-----  -#',
    '##--#-  - ',
    '##########',
    '##########'
]


class Tile(BaseEntity):
    def __init__(self):
        super().__init__((TILE_SIZE, TILE_SIZE), "sprites/tile.png")
        # super().__init__(position, (TILE_SIZE, TILE_SIZE), cs.GREEN)


def load_level():
    tiles = []
    coin_spawns = []
    for y, line in enumerate(level_layout):
        for x, char in enumerate(line):
            if char == " ":
                continue
            pos_x = x * TILE_SIZE
            pos_y = y * TILE_SIZE

            if char == "#":
                tile = Tile()
                tile.rect = pg.rect.Rect((pos_x, pos_y), (TILE_SIZE, TILE_SIZE))
                tiles.append(tile)
                continue
            if char == "-":
                coin_spawns.append((pos_x+TILE_SIZE/2, pos_y+TILE_SIZE/2))

    return tiles, coin_spawns
