import numpy as np
from pygame.sprite import Sprite
import math
class Ball(Sprite):
    pos = [0, 0]
    speed = [0, 0]
    acc = [0, 0]
    m = 0
    r = 0
    def __init__(self, pos, r, m):
        self.pos = pos
        self.m = m
        self.r = r
    def updatePos(self):
        self.speed = np.add(self.speed, self.acc)
        self.pos = np.add(self.pos,self.speed)
        self.acc = [0, 0]
    def Force(self, F):
        self.acc = np.add(self.acc, [F[0]/self.m,F[1]/self.m])
    def des(a, b):
        return math.sqrt(((a[0] - b[0]) * (a[0] - b[0])) + ((a[1] - b[1]) * (a[1] - b[1])))
    def collides(B1, B2):# لمنع تصادم بالونين
        return Ball.des(B1.pos, B2.pos) <= B1.r + B2.r