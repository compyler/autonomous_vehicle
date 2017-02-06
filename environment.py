import sys
import math
import numpy as np

import pygame
from pygame.locals import *
from pygame.color import THECOLORS

import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import DrawOptions

WIDTH = 800
HEIGHT = 1000
FPS = 60.0

UNIT_X = WIDTH/4
UNIT_Y = HEIGHT/1.5
UNIT_R = 20

pygame.init()
flags = pygame.DOUBLEBUF
display = pygame.display.set_mode((WIDTH, HEIGHT), flags)
display.set_alpha(None)
clock = pygame.time.Clock()

class Env:
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = (0.0,0.0)

        self.create_unit(UNIT_X, UNIT_Y, UNIT_R)
        self.create_enemy(WIDTH/2, HEIGHT/4, 30)

        self.borders = []
        self.borders.append(pymunk.Segment(
            self.space.static_body, (0,0), (0,HEIGHT), 3))
        self.borders.append(pymunk.Segment(
            self.space.static_body, (0,HEIGHT), (WIDTH,HEIGHT), 3))
        self.borders.append(pymunk.Segment(
            self.space.static_body, (WIDTH-1, HEIGHT), (WIDTH-1, 1), 3))
        self.borders.append(pymunk.Segment(
            self.space.static_body, (0,1), (WIDTH,1), 3))

        for border in self.borders:
            border.friction  = 1.05
            border.filter = pymunk.ShapeFilter(categories=1)
            border.collision_type = 2
            border.color = THECOLORS['green2']
        self.space.add(self.borders)


    def create_unit(self, x, y, r):
        self.unit_speed = 0
        self.unit_mass = 1
        self.unit_moment = pymunk.moment_for_circle(self.unit_mass, 0, r, (0,0))
        self.unit_body = pymunk.Body(self.unit_mass, self.unit_moment)
        self.unit_body.position = x, y
        self.unit_shape = pymunk.Circle(self.unit_body, r)
        self.unit_shape.elasticity = 1.0
        self.unit_shape.color = THECOLORS['red2']
        self.unit_shape.angle = math.pi / 4
        self.unit_direction = Vec2d(1,0).rotated(self.unit_body.angle)
        self.space.add(self.unit_body, self.unit_shape)

    def move_unit(self):
        self.unit_speed = 20
        self.unit_body.velocity = self.unit_direction * self.unit_speed
        print(self.unit_speed)

    def create_enemy(self, x, y, r):
        self.enemy_speed = 0
        self.enemy_mass = 1
        self.enemy_moment = pymunk.moment_for_circle(self.enemy_mass, 0, r, (0, 0))
        self.enemy_body = pymunk.Body(self.enemy_mass, self.enemy_moment)
        self.enemy_body.position = x, y
        self.enemy_shape = pymunk.Circle(self.enemy_body, r)
        self.enemy_shape.elasticity = 0.8
        self.enemy_shape.color = THECOLORS['blueviolet']
        self.enemy_shape.angle = math.pi / 4
        self.enemy_direction = Vec2d(1, 0).rotated(self.enemy_body.angle)
        self.space.add(self.enemy_body, self.enemy_shape)

    def move_enemy(self):
        self.enemy_speed = np.random.randint(50, 100)
        self.enemy_body.angle -= np.random.randint(-1, 2)/2
        self.enemy_direction = Vec2d(1,0).rotated(self.enemy_body.angle)
        self.enemy_body.velocity = self.enemy_speed * self.enemy_direction

    def screen_snap(self):
        draw_options = DrawOptions(display)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    sys.exit(0)

            display.fill((255,255,255))

            self.move_unit()
            self.move_enemy()

            self.space.debug_draw(draw_options)
            self.space.step(1/FPS)

            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    env = Env()
    sys.exit(env.screen_snap())