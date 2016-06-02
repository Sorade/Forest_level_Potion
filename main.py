# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 10:40:43 2016

@author: Julien
"""

import pygame, sys
import variables as v
from pygame.locals import *
from classes import *
from functions import *
from characters import *
from items import *
from instances import *
import levels as lvl


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
print mylevel1.player_list

'''Pygame Game Loop'''   
while True:
    clock.tick(v.FPS) #needed to slow game down
    v.screen.fill((0,0,0)) #make background black for map edges
    
    '''Main Game Loop'''
    mylevel1.execute()
        
    pygame.display.update()
    

    
