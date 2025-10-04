import pygame as pg
from global_variables import *


class GameText:
    def __init__(self, text_color="white"):
        self.font = pg.font.Font(None, 50)
        self.color = pg.color.Color(text_color)
        self.text = self.font.render("", False, self.color)
        self.position = (0, 0)

    def draw(self, surface: pg.Surface):
        surface.blit(self.text, self.position)


class Scoreboard(GameText):
    def __init__(self):
        super(Scoreboard, self).__init__()
        self.score = 0

    def update(self):
        self.text = self.font.render(F"Score: {self.score}", False, self.color)
        size = self.text.get_size()
        self.position = ((SCREENWIDTH - size[0]) / 2, 50)
        self.score += 1


class GameOver(GameText):
    def __init__(self):
        super(GameOver, self).__init__("red")
        self.font = pg.font.Font(None, 80)
        self.text = self.font.render("GAME OVER", False, self.color)
        size = self.text.get_size()
        self.position = ((SCREENWIDTH - size[0]) / 2, (SCREENHEIGTH - size[1]) / 2)
