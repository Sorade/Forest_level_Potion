# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 10:40:43 2016

@author: Julien
"""

import pygame, sys
from pygame.locals import *
from functions import *
import variables as v
import levels as lvl
import classes as cls
import instances as ins

'''Game Init'''
#pygame.init()
clock = pygame.time.Clock() #set timer which is used to slow game down

'''Music Init'''
pygame.mixer.music.load('Theme3.ogg')
#pygame.mixer.music.play(-1)

'''Levels Init'''
mystartmenu = lvl.StartMenu()
mylevel1 = lvl.Level1()
mylevel2 = lvl.Level2()

'''setting starting level by binding it to hero'''
ins.hero.level = mylevel1

'''Pygame Game Loop'''   
while True:
    clock.tick(v.FPS) #needed to slow game down
    v.screen.fill((0,0,0)) #make background black for map edges
    
    '''Main Game Loop'''
    mystartmenu.execute(ins.hero.level)
    #getting level list is needed for game reset purposes
    v.level_list[1].execute()
    v.level_list[2].execute()
    
    pygame.display.update()
    

    
