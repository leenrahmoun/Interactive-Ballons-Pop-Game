import numpy as np
import pygame
import math
from Ball import Ball


class Human():
    cameraPos = []
    pos = [0, 0]
    joints = []
    r = [50, 15, 15, 10, 10, 16, 16, 10, 10, 0, 0]
    color = [(239, 228, 176),
             (255, 0, 0),
             (255, 0, 0),
             (239, 228, 176),
             (239, 228, 176),
             (231, 76, 101),
             (231, 76, 101),
             (163, 73, 164),
             (163, 73, 164),
             (0, 0, 0),
             (0, 0, 0)]
    d = [70, 140, 90, 90, 100, 100, 150, 150]
    m = []
    faceImage = ''

    def __init__(self, npos):
        self.pos = npos
        for i in range(0, len(self.r)):
            self.cameraPos.append([0, 0])
        for rr in self.r:
            self.m.append(rr * 10)
        for i in range(0, len(self.r)):
            self.joints.append(Ball(self.pos, self.r[i], self.m[i]))
        self.joints[0].pos = np.subtract(self.joints[0].pos, [0, self.d[0]])
        self.joints[1].pos = np.add(self.joints[1].pos, [self.d[1] / 2 + self.d[2] + self.d[4], 0])
        self.joints[2].pos = np.subtract(self.joints[2].pos, [self.d[1] / 2 + self.d[3] + self.d[5], 0])
        self.joints[3].pos = np.add(self.joints[3].pos, [self.d[1] / 2 + self.d[2], 30])
        self.joints[4].pos = np.subtract(self.joints[4].pos, [self.d[1] / 2 + self.d[3], -30])
        self.joints[5].pos = np.add(self.joints[5].pos, [self.d[1] / 2, 0])
        self.joints[6].pos = np.subtract(self.joints[6].pos, [self.d[1] / 2, 0])
        self.joints[7].pos = np.add(self.joints[7].pos, [self.d[1] / 3, self.d[6]])
        self.joints[8].pos = np.add(self.joints[8].pos, [-self.d[1] / 3, self.d[7]])
        self.faceImage = pygame.image.load('wowFace.png')
        #self.bodyImage = pygame.image.load('wowFace.png')

    def drawJoint(self, screen, i, cameraPos):
        pygame.draw.circle(screen, self.color[i], np.subtract(self.joints[i].pos, cameraPos), self.r[i])

    def drawHuman(self, screen, cameraPos):
        newFacePos = self.setFacePos(self.pos, self.joints[0].pos, self.d[0])
        pygame.draw.polygon(screen, (163, 73, 164),
                            (np.subtract(self.joints[6].pos, cameraPos),
                             np.subtract(self.joints[5].pos, cameraPos),
                             np.add(np.subtract(self.joints[7].pos, cameraPos), [30, 50]),
                             np.add(np.subtract(self.joints[8].pos, cameraPos), [-3, 50])))
        pygame.draw.line(screen, (239, 228, 176), np.subtract(newFacePos, cameraPos), np.subtract(self.pos, cameraPos),
                         20)
        pygame.draw.circle(screen, self.color[0], np.subtract(newFacePos, cameraPos), self.r[0])
        vec = np.subtract(self.joints[0].pos, self.pos)
        deg = np.multiply(np.divide(np.arctan(vec[1] / vec[0]), np.pi), 180)
        if deg < 0:
            deg = -(deg + 90)
        else:
            deg = -deg + 90
        deg = np.max([deg, -10])
        deg = np.min([deg, 10])
        rotated_image_face = pygame.transform.rotate(self.faceImage, deg + 10)
        new_rect_face = rotated_image_face.get_rect(
            center=self.faceImage.get_rect(
                center=(newFacePos[0] - cameraPos[0], newFacePos[1] - 3 - cameraPos[1])).center)
        screen.blit(rotated_image_face, new_rect_face)
        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(newFacePos[0] -  40 - cameraPos[0], newFacePos[1] - 73 - cameraPos[1], 80, 20))
        pygame.draw.rect(screen, (30, 30, 30),
                         pygame.Rect(newFacePos[0] - 60 - cameraPos[0], newFacePos[1] - 50 - cameraPos[1], 120, 10))
        for i in range(7, 9):
            self.drawJoint(screen, i, cameraPos)
        pygame.draw.line(screen, (163, 73, 164), np.subtract(self.joints[5].pos, cameraPos), np.subtract(self.joints[6].pos, cameraPos), 15)
        pygame.draw.line(screen, (239, 228, 176), np.subtract(self.joints[3].pos, cameraPos), np.subtract(self.joints[5].pos, cameraPos), 15)
        pygame.draw.line(screen, (239, 228, 176), np.subtract(self.joints[4].pos, cameraPos), np.subtract(self.joints[6].pos, cameraPos), 15)
        for i in range(5, 7):
            self.drawJoint(screen, i, cameraPos)
        pygame.draw.line(screen, (239, 228, 176), np.subtract(self.joints[2].pos, cameraPos), np.subtract(self.joints[4].pos, cameraPos), 15)
        pygame.draw.line(screen, (239, 228, 176), np.subtract(self.joints[1].pos, cameraPos), np.subtract(self.joints[3].pos, cameraPos), 15)

        self.drawJoint(screen, 3, cameraPos)
        self.drawJoint(screen, 4, cameraPos)
        self.drawJoint(screen, 1, cameraPos)
        self.drawJoint(screen, 2, cameraPos)

    def editJoint(self, i, pos):
        self.cameraPos[i] = pos

    def des(a, b):
        return math.sqrt(((a[0] - b[0]) * (a[0] - b[0])) + ((a[1] - b[1]) * (a[1] - b[1])))

    def convertToPos(self):
        tx = (self.cameraPos[5][0] + self.cameraPos[6][0]) / 2
        ty = (self.cameraPos[5][1] + self.cameraPos[6][1]) / 2
        for i in range(0, len(self.r)):
            self.cameraPos[i] = np.subtract(self.cameraPos[i], [tx, ty])
        for i in range(0, len(self.r)):
            self.cameraPos[i] = np.divide(self.cameraPos[i], 0.008 * Human.des(self.cameraPos[6], self.cameraPos[5]))
        for i in range(0, len(self.r)):
            self.cameraPos[i] = np.add(self.cameraPos[i], self.pos)
        for i in range(0, len(self.r)):
            self.joints[i].pos = self.cameraPos[i]
        return [tx, ty]
    def setX(self, x):
        self.pos = [x, self.pos[1]]
    def setFacePos(self, a, b, l):
        p0 = np.subtract(b, a)
        l0 = np.sqrt(np.power(p0[0],2)+np.power(p0[1],2))

        return np.add(a, np.multiply(p0, l/l0))


