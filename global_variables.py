# Constants
import pygame

# Game
FPS = 60
SCREENWIDTH, SCREENHEIGTH = (500, 500)
visible_collisions = False

# Screen
LEFT_SIDE, TOP_SIDE = (0, 0)
RIGHT_SIDE, BOTTOM_SIDE = (SCREENWIDTH, SCREENHEIGTH)
TILE_SIZE = SCREENHEIGTH / 10

# Physics
GRAVITY = 1

# entities
NUMBER_OF_ENEMIES = 5
level = pygame.sprite.Group()
alive_enemies = pygame.sprite.Group()
death_enemies = pygame.sprite.Group()
game_coin = pygame.sprite.Group()

sides = {
    "left": None,
    "right": None,
    "top": None,
    "bottom": None,
}
sides_float = {
    "left": 0,
    "right": 0,
    "top": 0,
    "bottom": 0,
}

LEFT = "left"
RIGHT = "right"
TOP = "top"
BOTTOM = "bottom"
