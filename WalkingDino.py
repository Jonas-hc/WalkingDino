import pyglet
import math, sys, random
import pymunk
import pygame
from pygame.locals import *
from pygame.colordict import THECOLORS
from pymunk import Vec2d
from pymunk.pyglet_util import DrawOptions
import pymunk.pygame_util
import time

#conda install package-name=2.3.4 -n some-environment


width, height = 1280, 720
space = pymunk.Space()

all_sprite_list = pygame.sprite.Group()

mass   = 1
radius = 10
stepCount = 0
space.gravity = 0, -1000

circle_moment          = pymunk.moment_for_circle(mass, 0, radius)
circle_body            = pymunk.Body(mass, circle_moment)

circle_body.position   = 400, 160
circle_shape           = pymunk.Circle(circle_body, radius)
circle_shape.elasticity = 0.1
#circle_shape.friction   = 10.0
circle_shape.color = pygame.color.THECOLORS["lightskyblue"]

segment_shape          = pymunk.Segment(space.static_body, (0, 0),(800, 0), 40)
segment_shape.body.position  = 100, 100
segment_shape.elasticity = 0.0
segment_shape.friction = 1.0
segment_shape.color = pygame.color.THECOLORS["saddlebrown"]
space.add(segment_shape)

segment_shape          = pymunk.Segment(space.static_body, (0, 0),(800, 0), 10)
segment_shape.body.position  = 100, 140
segment_shape.elasticity = 0.0
segment_shape.friction = 1.0
segment_shape.color = pygame.color.THECOLORS["forestgreen"]
space.add(segment_shape)

segment_shape          = pymunk.Segment(space.static_body, (0, 0),(800, 0), 40)
segment_shape.body.position  = 600, 150
segment_shape.elasticity = 0.0
segment_shape.friction = 1.0
segment_shape.color = pygame.color.THECOLORS["saddlebrown"]
space.add(segment_shape)


segment_shape          = pymunk.Segment(space.static_body, (0, 0),(800, 0), 10)
segment_shape.body.position  = 600, 190
segment_shape.elasticity = 0.0
segment_shape.friction = 1.0
segment_shape.color = pygame.color.THECOLORS["forestgreen"]
space.add(segment_shape)


dino_img = pygame.image.load("res/Dino.png")

def coll_begin(arbiter, space, data):
    circle_body.velocity = (0, circle_body.velocity[1])
    return True

def coll_pre(arbiter, space, data):
    #print('pre solve')
    return True

#def coll_post(arbiter, space, data):
    #print('post solve')

#def coll_separate(arbiter, space, data):
    #print('separate')

coll_handler            = space.add_default_collision_handler()
coll_handler.begin      = coll_begin
coll_handler.pre_solve  = coll_pre
#coll_handler.post_solve = coll_post
#coll_handler.separate   = coll_separate


def flipy(p):
    """Convert chipmunk coordinates to pygame coordinates."""
    #return Vec2d(p[0], -p[1] + 600)
    return Vec2d(p[0]-35, -p[1] + 637)


class Dino(pygame.sprite.Sprite):
    # Sprite for player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.rect  = self.image.get_rect()
        self.direction = ''
        self.run = 1
        self.rect.center = flipy(circle_body.position)


    def draws(self, stepCount):

        dinoWalkRight = [pygame.image.load('Dino/Walk-Right/Walk(1).png'),
                         pygame.image.load('Dino/Walk-Right/Walk(2).png'),
                         pygame.image.load('Dino/Walk-Right/Walk(3).png'),
                         pygame.image.load('Dino/Walk-Right/Walk(4).png'),
                         pygame.image.load('Dino/Walk-Right/Walk(5).png'),
                         pygame.image.load('Dino/Walk-Right/Walk(6).png'),
                         pygame.image.load('Dino/Walk-Right/Walk(7).png'),
                         pygame.image.load('Dino/Walk-Right/Walk(8).png'),
                         pygame.image.load('Dino/Walk-Right/Walk(9).png')]

        dinoWalkLeft = [pygame.image.load('Dino/Walk-Left/Walk(1).png'),
                         pygame.image.load('Dino/Walk-Left/Walk(2).png'),
                         pygame.image.load('Dino/Walk-Left/Walk(3).png'),
                         pygame.image.load('Dino/Walk-Left/Walk(4).png'),
                         pygame.image.load('Dino/Walk-Left/Walk(5).png'),
                         pygame.image.load('Dino/Walk-Left/Walk(6).png'),
                         pygame.image.load('Dino/Walk-Left/Walk(7).png'),
                         pygame.image.load('Dino/Walk-Left/Walk(8).png'),
                         pygame.image.load('Dino/Walk-Left/Walk(9).png')]

        if(self.direction == 'right'):
            self.image = dinoWalkRight[stepCount // 3]
        else:
            self.image = dinoWalkLeft[stepCount // 3]
        self.rect.center = flipy(circle_body.position)


dino = Dino()
all_sprite_list = pygame.sprite.Group()
all_sprite_list.add(dino)




def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    running = True

    draw_options = pymunk.pygame_util.DrawOptions(screen)
    draw_options.shape_outline_color = pygame.color.THECOLORS["white"]
    # Set its gravity
    space.add(circle_body, circle_shape)

    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.
    myfont = pygame.font.SysFont('Comic Sans MS', 80)
    textsurface = myfont.render('Dino Walk', 1, (0,128,0))
    screen.blit(textsurface, (50, 50))
    stepCount = 0
    count = 0
    walk = False

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            keys = pygame.key.get_pressed()
            if event.type == KEYDOWN and event.key == K_SPACE:
                running = False

            if event.type == KEYDOWN and event.key == K_LSHIFT:
                dino.run = 4
            elif event.type == KEYDOWN and event.key == K_RSHIFT:
                dino.run = 1

            if event.type == KEYDOWN and event.key == K_UP and count == 0:
                if dino.direction == 'right':
                    circle_body.velocity = (400, 500)
                else:
                    circle_body.velocity = (-400, 500)
                count = 20
            elif event.type == KEYUP and event.key == K_UP:
                if dino.direction == 'right':
                    circle_body.velocity = (400, 0)
                else:
                    circle_body.velocity = (-400, 0)
            if event.type == KEYDOWN and event.key == K_RIGHT:
                circle_body.velocity = ((200 * dino.run), 0)
                if dino.direction == 'left':
                    dino.direction = 'right'
                    stepCount = 0
                else:
                    dino.direction = 'right'
                walk = True
            elif event.type == KEYUP and event.key == K_RIGHT:
                circle_body.velocity = (0, 0)
                if dino.direction == 'left':
                    dino.direction = 'right'
                    stepCount = 0
                else:
                    dino.direction = 'right'
                walk = False
            if event.type == KEYDOWN and event.key == K_LEFT:
                circle_body.velocity = ((-200 * dino.run), 0)
                if dino.direction == 'right':
                    dino.direction = 'left'
                    stepCount = 0
                else:
                    dino.direction = 'left'
                walk = True
            elif event.type == KEYUP and event.key == K_LEFT:
                circle_body.velocity = (0, 0)
                if dino.direction == 'right':
                    dino.direction = 'left'
                    stepCount = 0
                else:
                    dino.direction = 'left'
                walk = False


        dino.rect.center = flipy(circle_body.position)

        pygame.display.flip()
        screen.fill(THECOLORS["lightskyblue"])
        all_sprite_list.update()

        space.debug_draw(draw_options)
        all_sprite_list.draw(screen)

        if stepCount + 2 >= 27:
            stepCount = 0
        elif walk:
            stepCount = stepCount + 2

        dino.draws(stepCount)

        if(circle_body.velocity[1] >= 0):
            circle_body.velocity[0] = 0

        screen.blit(textsurface, (50, 50))

        #fps = 60
        fps = 20
        dt = 1. / fps
        space.step(dt)

        pygame.display.flip()
        clock.tick(fps)

        if count == 0:
            count = 0
        else:
            count -= 1

        if circle_body.position[1] < -1000:
            running = False


if __name__ == "__main__":
    sys.exit(main())