import pygame
import neat
import time
import os
import random
from constants import *

class Pipe:

    ''' We need top and bottom pipe. To define both the pipes we need the following:

        - GAP: the distance between the bars. Currently set to fix, can be made alternating for complexity. 
        - Pipe moving velocity, currently set to fix velocity, can be increased based on complexity.
        - x position of the pipe along the screen
        - Position of top and bottom pipe. Since the images are placed based on the top left corner, we need to shift the 
        top pipe to up for correct positioning.

    Modules:
        - set_height: Set the y position (height) of the bars. 
        - move : In this game, bird does not move in x axis but the pipes and the background. So move the pipes 
        with a fixed velocity.
        - draw: Display the pipes. 
        - collide : Test if the bird and pipes are colliding with each other to set game over.      
    '''

    GAP = 200
    VEL = 5

    def __init__(self,x):

        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0

        # define the top pipe, by flipping the original image
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        # original image is already at the bottom
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False  # if the bird already passed the pipe
        self.set_height()
    
    def set_height(self):   
        """Get a random number to display the pipe"""
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL
    
    def draw(self,win):

        win.blit(self.PIPE_TOP,(self.x,self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    
    def collide(self,bird, win):

        """Did we collide with the pipe"""

        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset) # if they dont collide will return null, pygame does it for us
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False
