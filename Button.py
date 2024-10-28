import pygame
import math
from Ball import Ball


class Button(Ball):
    def __init__(self, npos, nr, imagePath):
        self.pos = npos
        self.r = nr
        self.Image = pygame.image.load(imagePath)
        self.h = self.Image.get_height()
        self.w = self.Image.get_width()

    def draw(self, screen, cameraPos):
        screen.blit(self.Image, (self.pos[0] - self.r - cameraPos[0], self.pos[1] - self.h /10 - cameraPos[1]))

    def des(balloon1, balloon2):
        return math.sqrt(((balloon1.pos[0] - balloon2.pos[0]) * (balloon1.pos[0] - balloon2.pos[0])) + (
                    (balloon1.pos[1] - balloon2.pos[1]) * (balloon1.pos[1] - balloon2.pos[1])))

    def is_clicked(self):
        tempBalloon = Button(pygame.mouse.get_pos(), 'Red')
        return pygame.mouse.get_pressed()[0] and Button.des(tempBalloon, self) < self.w
