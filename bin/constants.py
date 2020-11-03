import pygame
import neat
import time
import os
import random

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