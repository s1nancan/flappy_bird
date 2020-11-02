# Import packages
import pygame
import neat
import time
import os
import random
pygame.font.init()

# Window size for game
WIN_WIDTH = 500
WIN_HEIGHT = 800
GEN = 0
# Images to be displayed 
BIRD_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BCKGRND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))

# Fonts for displaying the scoore
STAT_FONT = pygame.font.SysFont('comicsans',50)

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


def draw_window(win, birds, pipes, base, score, GEN):

    '''
    Win is the window from the pygame module, and blit is used to display the given image on a given position.
    
    '''
    # blit just draws
    win.blit(BCKGRND_IMG, (0,0))


    # There can be more than a single pipe in a given screen, so draw all the pipes 
    for pipe in pipes:
        pipe.draw(win)

    # Render the core on the top right 
    text = STAT_FONT.render("Score: " + str(score),1,(255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text2 = STAT_FONT.render("Generation: " + str(GEN),1,(255, 255, 255))
    win.blit(text2, (10, 10))

    # Draw the base 
    base.draw(win)

    # Draw the bird
    for bird in birds:
        bird.draw(win)

    # Update the display with the given blits. 
    pygame.display.update()



# main loop of the game
def main(genomes, config):
    '''
    Main function that combines the different parts and displays the game
    Initialize 3 different classes, bird, base, pipes, and initialize the score.

    This function should work for more than a single bird. We can make it to run a game per bird but that will take a while
    '''
    global GEN 
    GEN+=1

    nets = [] # need to keep track of neural networks
    ge= []  # need to keep track of genome, so that we can change their fitness depending on where they are 
    birds = [] #Bird(230,350)  # start position 
    
    for _, g in genomes:    # genomes are tuple with genome id and genome object. We dont need the id. 
        
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness = 0
        ge.append(g)

    
    base = Base(720)
    pipes = [Pipe(700)]
    score = 0

    # Initially there is no pipe
    add_pipe = False
    
    # initialization of the window
    win=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    
    # to set the game speed. 
    clock = pygame.time.Clock()
    

    # The game runs in a loop, and it only breaks if we "hit" either pipes or to the base. 

    run = True
    while run and len(birds)>0:
        clock.tick(30)
        
        # If we click to the X to close the game. 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break
        
        

        # Start the bird movement 
        #bird.move()

        pipe_ind = 0
        if len(birds) > 0 :

            # If the bird position is larger than the pipe_0 (that is if the bird passed the pipe)
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        
        else :  # Quit running the game
            run = False
            break

        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1   # Every sec it stay alive, it will gain a point
            bird.move()

            
            # MAIN PART THAT UTILIZES NN to DECIDE WHETHER OR JUMP,
            # remember we have used tanh as output activation, and now choosing 0.5 to decide to jump
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5: # outputs are list, we have 1 element but still its a list.
                bird.jump()

        # Move the base
        base.move()

        add_pipe = False
        rem = [] # pipes to be removed
        for pipe in pipes:
            # Move each pipe in the pipes
            pipe.move()

            for x, bird in enumerate(birds):
            # Check for collision
                if pipe.collide(bird,win):
                    ge[x].fitness -= 1  # Everytime it fits to pipe, we lower fitness
                    birds.pop(x) # Eliminate the birds that hit the pipes
                    nets.pop(x) # Eliminate the birds that hit the pipes
                    ge.pop(x)   # Eliminate the birds that hit the pipes

                

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)    # pipe is going to be removed

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True      # Bird passed the pipe position.
                add_pipe = True



        if add_pipe: 
            score+= 1       # tracking out score
            for g in ge:
                g.fitness += 5 # if they pass a pipe, increase their fitness
            
            pipes.append(Pipe(600))
            #add_pipe = False

        for r in rem:
            pipes.remove(r)

        
        # Condition to check if we have hit the base or flying over the top
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_width() >= 720 or bird.y < -50:
                # if a bird hits ground, remove from population
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)




        draw_window(win, birds, pipes, base, score, GEN)

        # break if score gets large enough
        '''if score > 20:
            pickle.dump(nets[0],open("best.pickle", "wb"))
            break'''
                


def run(config_path):

    # subheadings used in the config file are passed in the following:
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
            neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    # get the statistics about generations
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # run for 50 iterations for a given fitness function (how far it moves in the game)
    winner = p.run(main,50)

    print('\nBest genome:\n{!s}'.format(winner))
    

if __name__ == "__main__":

    # path to config file
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)