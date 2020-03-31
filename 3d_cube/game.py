import pygame
from pygame.locals import *
from math import sin, cos, pi, atan, sqrt
from itertools import combinations
from vector_manipulation import *


def integer(*args):
    if len(args) == 1:
        temp = int(args[0])
        if args[0] - temp > 0.5:
            return temp + 1
        else:
            return temp
    elif len(args) > 1:
        return list([integer(i) for i in args])


class Camera:
    def __init__(self, distance): #distance = distance from camera to origin
        self.height = windowHeight
        self.width = windowWidth
        self.pointUpLeft = integer(-self.width/2, self.height/2,distance)
        self.pointUpRight = integer(self.width/2, self.height/2,distance)
        self.pointDownRight = integer(self.width/2, -self.height/2,distance)
        self.PointDownLeft = integer(-self.width/2, -self.height/2,distance)
        self.vanishingPoint = rectangleCentre(self.pointUpLeft,  self.pointUpRight, self.pointDownRight,
                                              self.PointDownLeft, vpDistance)


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def draw(self):
        for i,j in self.edges:
            pygame.draw.line(windowSurface, RED, (i.display_x, i.display_y), (j.display_x, j.display_y), 2)
        for k in self.nodes:
            if k.display_x >= 0 and k.display_y >= 0:
                pygame.draw.circle(windowSurface, BLACK, (k.display_x, k.display_y), 4)

class Node:
    def __init__(self, coordinates, name):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]
        self._display_x = self.x
        self._display_y = self.y
        self.name = "Node" + str(name)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

    @property
    def display_x(self):
        vectorFromOrigin = linePlaneIntersect(camera.vanishingPoint, (self.x,self.y,self.z), camera.pointUpLeft,
                                              camera.pointUpRight, camera.pointDownRight, 1e-6)
        vectorFromTopLeftCorner = subv3v3(vectorFromOrigin, camera.pointUpLeft)
        return int(vectorFromTopLeftCorner[0])

    @display_x.setter
    def display_x(self, value):
        self._display_x = value

    @display_x.deleter
    def display_x(self):
        del self._display_x

    @property
    def display_y(self):
        vectorFromOrigin = linePlaneIntersect(camera.vanishingPoint, (self.x,self.y,self.z), camera.pointUpLeft,
                                              camera.pointUpRight, camera.pointDownRight,1e-6)
        vectorFromTopLeftCorner = subv3v3(vectorFromOrigin, camera.pointUpLeft)
        return - int(vectorFromTopLeftCorner[1])

    @display_y.setter
    def display_y(self, value):
        self._display_y = value

    @display_y.deleter
    def display_y(self):
        del self._display_y

    def move(self):
        def findAngle(self):
            a = self.x >= 0
            b = self.y >= 0
            c = self.z >= 0
            if self.z == 0:
                yz_angle = 0
            elif (b and c) or (not b and c):
                yz_angle = atan(self.y / self.z)
            elif not b and not c:
                yz_angle = -pi + atan(self.y / self.z)
            else:
                yz_angle = pi + atan(self.y / self.z)

            if self.x == 0:
                xz_angle = 0
            elif (a and c) or (not c and a):
                xz_angle = atan(self.z / self.x)
            elif not c and not a:
                xz_angle = -pi + atan(self.z / self.x)
            else:
                xz_angle = pi + atan(self.z / self.x)
            return yz_angle, xz_angle

        if rotateUp == True:
            yz_angle, xz_angle = findAngle(self)
            radius = sqrt(self.y ** 2 + self.z ** 2)
            self.y = radius * sin(w + yz_angle)
            self.z = radius * cos(w + yz_angle)
        if rotateDown == True:
            yz_angle, xz_angle = findAngle(self)
            radius = sqrt(self.y ** 2 + self.z ** 2)
            self.y = radius * sin(yz_angle - w)
            self.z = radius * cos(yz_angle - w)
        if rotateLeft == True:
            yz_angle, xz_angle = findAngle(self)
            radius = sqrt(self.x ** 2 + self.z **2)
            self.x = radius * cos(w + xz_angle)
            self.z = radius * sin(w + xz_angle)
        if rotateRight == True:
            yz_angle, xz_angle = findAngle(self)
            radius = sqrt(self.x ** 2 + self.z **2)
            self.x = radius * cos(xz_angle - w)
            self.z = radius * sin(xz_angle - w)


def redrawWindow():
    windowSurface.fill(WHITE)
    for i in graph.nodes:
        i.move()
    graph.draw()
    pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    mainClock = pygame.time.Clock()
    windowSurface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    windowHeight, windowWidth = pygame.display.Info().current_h, pygame.display.Info().current_w
    FPS = 60
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    angularVelocity = pi / 20
    w = angularVelocity
    vpDistance = 500  # distance from vanishing point to camera
    rotateDown, rotateLeft, rotateRight, rotateUp = False, False, False, False
    graph = Graph()
    num = 1
    for i,j,k in [(i,j,k) for i in (1,-1) for j in (1,-1) for k in (1,-1)]:
        graph.nodes.append(Node((100*i, 100*j, 100*k), num))
        num += 1
    for i,j in combinations(graph.nodes, 2):
        graph.edges.append([i,j])
    camera = Camera(200)
    while True:
        mainClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == K_DOWN:
                    rotateDown = True
                if event.key == K_UP:
                    rotateUp = True
                if event.key == K_LEFT:
                    rotateLeft = True
                if event.key == K_RIGHT:
                    rotateRight = True
            if event.type == KEYUP:
                if event.key == K_DOWN:
                    rotateDown = False
                if event.key == K_UP:
                    rotateUp = False
                if event.key == K_LEFT:
                    rotateLeft = False
                if event.key == K_RIGHT:
                    rotateRight = False
        redrawWindow()

