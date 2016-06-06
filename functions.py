# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 19:58:44 2016

@author: Julien
"""

import pygame, variables#, instances, random
import numpy as np
from pygame.locals import *

def get_line(start, end):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end
 
    >>> points1 = get_line((0, 0), (3, 4))
    >>> points2 = get_line((3, 4), (0, 0))
    >>> assert(set(points1) == set(points2))
    >>> print points1
    [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    >>> print points2
    [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
 
    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
 
    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points

def in_sight(shooter, target, range_, obstacles):
    line_of_sight = get_line(shooter.rect.center, target.rect.center)
    zone = shooter.rect.inflate(range_,range_)
    obstacles_in_sight = zone.collidelistall(obstacles)
    for x in range(1,len(line_of_sight),5):
        for obs in obstacles_in_sight:
            if obs.rect.collidepoint(x):
                return False
    return True
            
            

def group_collision_check(group,character):
#    col_y = False
#    col_x = False
    char_col_points = [character.rect.bottomleft,
                       character.rect.bottomright,
                       character.rect.midleft,
                       character.rect.midright,
                       character.rect.midbottom,
                       character.rect.center]

    for sprite in group: #checks if sprite collide with character using test_rect
        test_rect = Rect(sprite.rect)
#        print test_rect
        if (variables.dx  == 0 and variables.dy == 0) == False:
            #check x xollision
            test_rect = test_rect.move(variables.xoffset,0)#.inflate(-test_rect.width/8,-test_rect.height/10)
            if len([x for x in char_col_points if test_rect.inflate(-test_rect.width/5,0).collidepoint(x)]) >= 1:
                print len([x for x in char_col_points if test_rect.collidepoint(x)])
                variables.xoffset = 0 #set x offset to 0 for global use
                variables.yoffset += variables.xoffset
#                col_x = True
            #check y collision
            test_rect = Rect(sprite.rect) #resets test_rect to initial sprite position
            test_rect = test_rect.move(0,variables.yoffset)#.inflate(-10,-5)
            if len([x for x in char_col_points if test_rect.inflate(0,-test_rect.height/5).collidepoint(x)]) >= 1:
                variables.yoffset = 0 #set y offset to 0 for global use
                variables.xoffset += variables.yoffset
#                col_y = True
                
                
def group_offset(group):
    #if no collision on ALL SPRITES then moves the sprites in the group            
    for sprite in group:
        if (variables.dx  == 0 and variables.dy == 0) == False:
            sprite.rect = sprite.rect.move(variables.xoffset,variables.yoffset)
            
def group_push(group,character):
    for sprite in group:
        if (variables.dx  == 0 and variables.dy == 0) == False:
            sprite.rect = sprite.rect.move(variables.xoffset,variables.yoffset)
            if pygame.sprite.collide_rect(sprite, character):
                sprite.rect = sprite.rect.move(-variables.xoffset,-variables.yoffset)           

def get_offset(character,event):
    #if event.type == MOUSEBUTTONDOWN: #maybe check here for map's dest vs map pos using dx and dy
        #print 'reset'
        m_pos = pygame.mouse.get_pos() #mouse position tracker
        speed = character.speed #player's speed
        
        xp = (variables.screenWIDTH/2)-(instances.hero.image.get_rect()[2]/2.)
        yp = (variables.screenHEIGHT/2)-(instances.hero.image.get_rect()[3]/2.)
        #print xp,yp
        xm = m_pos[0]-instances.hero.image.get_rect()[2] #adds offset to center player
        ym = m_pos[1]-instances.hero.image.get_rect()[3]
        
        variables.dx = xm-xp
        variables.dy= float(ym-yp) 
        
        
        dist = (variables.dx**2+variables.dy**2)**0.5 #get lenght to travel
        
        
        #calculates angle and sets quadrant
        if variables.dx == 0 or variables.dy == 0:
            angle_rad = 0#np.pi/2
            if variables.dx == 0 and ym > yp:
                xoffset = 0
                yoffset = -speed
                variables.orientation = 180
            elif variables.dx == 0 and ym < yp:
                xoffset = 0
                yoffset = speed
                variables.orientation = 0
            elif variables.dy == 0 and xm > xp:
                xoffset = 0
                yoffset = -speed
                variables.orientation = 90
            elif variables.dy == 0 and xm < xp:
                xoffset = 0
                yoffset = speed
                variables.orientation = 270
            else:
                xoffset, yoffset = 0,0
                variables.orientation = 180
        elif xm > xp and ym > yp:
            angle_rad = np.arctan((abs(variables.dy)/abs(variables.dx)))
            xoffset = -np.cos(angle_rad)*speed
            yoffset = -np.sin(angle_rad)*speed
            variables.orientation = angle_rad*(180.0/np.pi)+90
        elif xm < xp and ym > yp:
            angle_rad = np.arctan((abs(variables.dx)/abs(variables.dy)))
            xoffset =  np.sin(angle_rad)*speed
            yoffset = -np.cos(angle_rad)*speed
            variables.orientation = angle_rad*(180.0/np.pi)+180
        elif xm < xp and ym < yp:
            angle_rad = np.arctan((abs(variables.dy)/abs(variables.dx)))
            xoffset = np.cos(angle_rad)*speed
            yoffset = np.sin(angle_rad)*speed
            variables.orientation = angle_rad*(180.0/np.pi)+270
        else:# xm > xp and ym < yp:
            angle_rad = np.arctan((abs(variables.dx)/abs(variables.dy)))
            xoffset = -np.sin(angle_rad)*speed
            yoffset =  np.cos(angle_rad)*speed
            variables.orientation = angle_rad*(180.0/np.pi)
        
        variables.xoffset = xoffset
        variables.yoffset = yoffset
        print variables.orientation
        
def adjust_offset():        
    variables.dx += variables.xoffset
    variables.dy += variables.yoffset
    
def check_null_offset():
    if variables.dx <= 1 and variables.dx >= -1:
        variables.dx = 0
        variables.xoffset = 0
    if variables.dy <= 1 and variables.dy >= -1:
        variables.dy = 0
        variables.yoffset = 0
    if variables.has_shot == True:
        variables.dy, variables.dx = 0,0
        variables.yoffset, variables.xoffset = 0,0
        variables.has_shot = False
        
    
        

            
            
            
            