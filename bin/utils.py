import pygame
import neat
import time
import os
import random
from utils import *
from constants import *
from bird import *
from base import *
from pipe import *

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
def eval_genomes(genomes, config):
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
               