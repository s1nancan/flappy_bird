import pygame
import neat
import time
import os, sys
import random
sys.path.insert(0,'bin')
import bird
import pipe
import base
from  utils import * 




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
    winner = p.run(eval_genomes,50)

    print('\nBest genome:\n{!s}'.format(winner))
    

if __name__ == "__main__":

    # path to config file
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)