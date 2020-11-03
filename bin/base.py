import pygame
import neat
import time
import os
import random
pygame.font.init()
from constants import *

class Base:

    ''' There is a grass at the bottom of the page, that is the base. We need to define: 
            - How fast the base image moves, should be same with the pipe velocity for smooth motion (remember, the bird only moves up and down)
            - Base image (with widht measured, since the image is smaller than the whole screen, we are going to need to 
        duplicate the image and put one after another. )
        Modules:
            - move: We need to move the base image along with the pipes to give the impression that bird is flying forward.
            - draw: Display the base image. 
    '''

    VEL = 5 # needs to be same as pipe velocity
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH


    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0 :
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0 : 
            self.x2 = self.x1 + self.WIDTH

    def draw(self,win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


# We have defined the 3 classes for playing the game:
    # BIRD, PIPES, BASE now define the functions to display the game and the main function for playing.
