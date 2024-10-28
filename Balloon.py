import pygame
import math
from Ball import Ball
class Balloon(Ball):
    w, h = 100, 200
    m = 10
    r = w/2
    color = 'Red'
    Image = ''
    def __init__(self, npos, ncolor):
        self.pos = npos
        self.color = ncolor
        if self.color == 'Red':
            self.Image = pygame.image.load('RedBalloon.png')
        elif self.color == 'Green':
            self.Image = pygame.image.load('GreenBalloon.png')
        self.h = self.Image.get_height()
        self.w = self.Image.get_width()
    def draw(self, screen, cameraPos):
        screen.blit(self.Image, (self.pos[0] - self.r - cameraPos[0], self.pos[1]-self.h/4 - cameraPos[1]))
    def des(balloon1, balloon2):
        return math.sqrt(((balloon1.pos[0]-balloon2.pos[0])*(balloon1.pos[0]-balloon2.pos[0]))+((balloon1.pos[1]-balloon2.pos[1])*(balloon1.pos[1]-balloon2.pos[1])))
    def is_clicked(self):
        tempBalloon = Balloon(pygame.mouse.get_pos(),'Red')
        return pygame.mouse.get_pressed()[0] and Balloon.des(tempBalloon,self) < self.w