# Import packages
import pygame
import neat
import time
import os
import random
pygame.font.init()
from constants import *


# START with a BIRD CLASS to define the the actions of the bird. 
class Bird:
    '''
    To define the bird, we need to define its 
        - x and y position on the screen
        - its tilting, (while it goes up and down) to give a more natural look
        - Velocity : to give the realistic effect of going up slower after a push and going up faster while going down
        - Image count to keep track of what part of wing flapping we are on
        - Images to display

    Modules:
        - jump : Define a jump
        - move : Birds diplacement on the y axis and its tilting. 
        - draw : Define which image to be displayed at what tilting and wing condition and display it to the screen
        - get mask: Used in defining the pixel perfect collision. It was based in the pygame's own modules. 
    '''

    IMGS = BIRD_IMG
    # Constants to use later
    MAX_ROTATION = 25   # rotation of the bird head
    ROT_VEL = 20  # how fast the bird head rotates
    ANIMATION_TIME = 5  # flapping of wings
    
    def __init__(self,x,y):
        
        # Starting position of the bird
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
        
        
    def jump(self):
        
        """Jump of the bird"""
        
        # 0,0 is the top left. Go up : negative velocity, go down : positive velocity
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y # Original position it starts to jump
        
    def move(self):
        """Used to move the bird at every frame"""
        self.tick_count += 1 # how many times it moved/frame changed
        
        # Displacement, how many pixels are we moving up or down in each frame
        # It is formulation for how far it goes up, similar to d = v_0*t - 1/2g*t^2 (tick_count is like t, time here)
        d = self.velocity * self.tick_count + 1.5*self.tick_count**2
        
        # We don't want to set this to go very very fast at increasing t, therefore limit it to a fix value
        
        if d >=16: # Remember, positive d corresponds downward movement
            d=16
            
        if d<0:
            d-=2
            
        self.y = self.y + d # Update the new position for the bird by adding the displacement
        
        # Now write the tilting of the bird image. 
        # If we are moving up (d<0) or still above the original start position show the bird as if moving up (even though
        # it started to move downward after reaching the top for visual purposes) 
        
        # TO DO try different scenarios
        if d<0 or self.y < self.height + 50: # 50 is some arbitrary number to start tilting
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION # make sure the bird is not tilted all the way back.

        else : # Now bird is moving downwards, we can have the tilt to go nose dive
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self,win):
        self.img_count +=1 # how many ticks the game is played
        #print(self.ANIMATION_TIME)

        if self.img_count < self.ANIMATION_TIME:
            # show the flat wings
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            # show the up wing
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            # show the down wing
            self.img = self.IMGS[2] 
        elif self.img_count < self.ANIMATION_TIME*4:
            # back to previous step
            self.img = self.IMGS[1]  
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            # back to orinal flat wing
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80: # when nosediving
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2 # continuous from the line 84 (first elif above)


        rotated_image = pygame.transform.rotate(self.img, self.tilt) # rotate image for us
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft= (self.x, self.y)).center) # rotated in center
        win.blit(rotated_image, new_rect.topleft) 
        

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
