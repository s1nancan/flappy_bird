# Import packages
import pygame
import neat
import time
import os
import random
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))

BCKGRND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
STAT_FONT = pygame.font.SysFont('comicsans',50)

class Bird:
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
        self.vel = -10.5
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


class Pipe:
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

    
    def collide(self,bird):

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


class Base:
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


def draw_window(win,bird, pipes, base, score):
    # blit just draws
    win.blit(BCKGRND_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score),1,(255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)
    bird.draw(win)

    pygame.display.update()



# main loop of the game
def main():
    bird = Bird(230,350)  # start position 
    base = Base(720)
    pipes = [Pipe(700)]
    score = 0
    add_pipe = False
    
    # initialization of the window
    win=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    
    clock = pygame.time.Clock()
    
    
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        #bird.move()

        rem = [] # pipes to be removed
        for pipe in pipes:
            # Check for collision
            if pipe.collide(bird):
                pass
            
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)    # pipe is going to be removed

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True      # Bird passed the pipe position.
                add_pipe = True


            pipe.move()

        if add_pipe: 
            score+= 1       # tracking out score
            pipes.append(Pipe(600))
            add_pipe = False

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_width() >= 720:
            pass

        base.move()
        draw_window(win,bird,pipes, base, score)
                
    pygame.quit()
    quit()

main()
        