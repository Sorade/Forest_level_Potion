# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 10:40:43 2016

@author: Julien
"""

import pygame, sys
import variables as v
import levels as lvl
from pygame.locals import *
from classes import *
from functions import *
from characters import *
from items import *
from instances import *

'''Game Init'''
pygame.init()
clock = pygame.time.Clock() #set timer which is used to slow game down

'''Music Init'''
pygame.mixer.init()
pygame.mixer.music.load('Theme3.ogg')
pygame.mixer.music.play(-1)

'''Levels Init'''
mylevel1 = lvl.Level1()
mylevel1.run = True
mylevel2 = lvl.Level2()


'''Pygame Game Loop'''   
while True:
    clock.tick(v.FPS) #needed to slow game down
    v.screen.fill((0,0,0)) #make background black for map edges
    
    '''Main Game Loop'''
    mylevel1.execute()
    mylevel2.execute()
        
    pygame.display.update()
    

    
