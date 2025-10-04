import sys
from entities.coin import Coin
from entities.enemy import Enemy
from entities.player import Player
from entities.level import *
import random as rd

from entities.game_text import Scoreboard, GameOver


def update_entities():
    player.update()
    current_coin.update(player)
    alive_enemies.update(player)
    death_enemies.update(player)


def draw_entities():
    screen.blit(wallpaper, (0,0))
    level.draw(screen)
    scoreboard.draw(screen)
    game_coin.draw(screen)
    player.draw(screen)
    alive_enemies.draw(screen)


def show_game_over_screen():
    game_over_screen.draw(screen)
    pg.display.update()

    waiting = True
    while waiting:
        for event_ in pg.event.get():
            if event_.type == pg.QUIT:
                pg.quit()
                sys.exit()
        clock.tick(15)


# window configuration
pg.init()
pg.display.set_caption("Jumping game!")
screen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGTH))

# game configuration
clock = pg.time.Clock()
wallpaper = pg.image.load("sprites/space.png")
wallpaper = pg.transform.scale(wallpaper, (SCREENWIDTH, SCREENHEIGTH))

# load entities
player = Player()
alive_enemies.add([Enemy() for _ in range(NUMBER_OF_ENEMIES)])
tiles, coin_spawns = load_level()
level.add(tiles)
current_coin = Coin()
scoreboard = Scoreboard()
game_over_screen = GameOver()

# game loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    if not player.is_alive:
        print("OH OH")
        show_game_over_screen()
        pg.display.update()
        continue

    if not current_coin.alive():
        scoreboard.update()
        current_coin.respawn(rd.choice(coin_spawns))

    update_entities()
    draw_entities()

    pg.display.update()
    clock.tick(FPS)
