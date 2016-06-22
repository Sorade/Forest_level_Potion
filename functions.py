# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 19:58:44 2016

@author: Julien
"""

import pygame, variables#, instances, random
import numpy as np
import random
from pygame.locals import *
from math import acos
from math import sqrt
from math import pi

#def for_group(group,*functions):
#    for item in group:
#        for function in functions:
#            pass

def move_item(char,item,inv_a,inv_b):
    '''moves an item from one Inventory to another,
    the item HAS TO BE IN the inventory to start with'''
    #item_to_move = [x for x in char.inv_a.contents if isinstance(x, type(item)) == True][0]
    inv_a.remove(item)
    inv_b.append(item)
    
def exchange_item(char,item_a,item_b,inv_a,inv_b):
    move_item(char,item_a,inv_a,inv_b)
    move_item(char,item_b,inv_b,inv_a)
    
def attempt_exchange(char,item_a,item_b,inv_a,inv_b):
    if len([x for x in char.inv_a.contents if isinstance(x, type(item_a)) == True]) > 0:
        has_item_a = True 
    else:
        has_item_a = False
    if len([x for x in char.inv_b.contents if isinstance(x, type(item_b)) == True]) > 0:
        has_item_b = True 
    else:
        has_item_b = False
     
    if has_item_a == True and has_item_b == True:
        exchange_item(char,item_a,item_b,inv_a,inv_b)
        

def d10(int):
    rng = range(0,int)
    total = 0
    for x in rng:
        total += random.randint(0,10)
    return total
    
def get_circle(radius):
    "Bresenham complete circle algorithm in Python"
    # init vars
    switch = 3 - (2 * radius)
    points = set()
    x = 0
    y = radius
    dly = 0
    # first quarter/octant starts clockwise at 12 o'clock
    while x <= y:
        if dly == 12:
            dly = 0
            # first quarter first octant
            points.add((x,-y))
            # first quarter 2nd octant
            points.add((y,-x))
            # second quarter 3rd octant
            points.add((y,x))
            # second quarter 4.octant
            points.add((x,y))
            # third quarter 5.octant
            points.add((-x,y))        
            # third quarter 6.octant
            points.add((-y,x))
            # fourth quarter 7.octant
            points.add((-y,-x))
            # fourth quarter 8.octant
            points.add((-x,-y))
        if switch < 0:
            switch = switch + (4 * x) + 6
        else:
            switch = switch + (4 * (x - y)) + 10
            y = y - 1
        x = x + 1
        dly += 1
        
    return points

def shadow_gen(shadow_surf,source,cir_pt,obstacles):
    #line_points = get_line(source.pos,cir_pt)
    for line_pt in get_line(source.pos,cir_pt)[0::35]:#[0::3]:
        for obs in obstacles:
            if obs.rect.collidepoint(line_pt) or pygame.Rect(0,0,variables.screenWIDTH,variables.screenHEIGHT).collidepoint(line_pt) == False:
                return
#            if shadow_surf.get_at(line_pt) != (255, 255, 255, 255):
            pygame.draw.circle(shadow_surf, (255,255,255), line_pt, 28, 0) #radius to 5px and 0 to fill the circle
                
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
    obstacles_list = [rectangle.rect for rectangle in obstacles] #to support indexing
    obstacles_in_sight = zone.collidelistall(obstacles_list)
    for x in range(1,len(line_of_sight),5):
        for obs_index in obstacles_in_sight:
            if obstacles_list[obs_index].collidepoint(line_of_sight[x]):
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
        
'''Shadow Generation And Geometry Functions'''
def pop_poly_pts(source,corner,obstacles, poly_pts):
    for pt in fn.get_line(source.pos,corner)[0::20]:
        for obstacle in obstacles:
            if obstacle.rect.collidepoint(pt):
                print source.pos,pt
                angle = angle_clockwise(source.pos,(source.pos[0],source.pos[1]-50),pt)
                poly_pts[angle] = pt
                return
                
def cast_multi(source,point,Ray):
    '''casts a ray to the point and to 2 more nearby points'''
    return [Ray(source,point,0),Ray(source,point,0.01),Ray(source,point,-0.01)]
                
def get_seg(rect,Segment):
    return [Segment(rect.topleft,rect.topright),\
           Segment(rect.topright,rect.bottomright),\
           Segment(rect.bottomleft,rect.bottomright),\
           Segment(rect.topleft,rect.bottomleft)]
                
def length(s,v):
    return sqrt((s[0]-v[0])**2+(s[1]-v[1])**2)
    
'''a · b = ax × bx + ay × by'''
def dot_product(s,v,w):
   return (v[0]-s[0])*(w[0]-s[0])+(v[1]-s[1])*(w[1]-s[1])
def determinant(s,v,w):
   return (v[0]-s[0])*(w[1]-s[1])-(v[1]-s[1])*(w[0]-s[0])
def inner_angle(s,v,w):
    if (length(s,v)*length(s,w)) != 0:
       cosx=dot_product(s,v,w)/(length(s,v)*length(s,w))
       rad=acos(cosx) # in radians
       return rad*180/pi # returns degrees
    else:
        return 0
def angle_clockwise(s,A, B):
    a = (float(A[0]),float(A[1]))
    b = (float(B[0]),float(B[1]))
    inner=inner_angle(s,a,b)
    det = determinant(s,a,b)
    if det<0: #this is a property of the det. If the det < 0 then B is clockwise of A
        return inner
    else: # if the det > 0 then A is immediately clockwise of B
        return 360-inner    

def isBetween(a, b, c):
    a_x,a_y = a
    b_x,b_y = b
    c_x,c_y = c
    a_x,a_y = float(a_x),float(a_y)
    b_x,b_y = float(b_x),float(b_y)
    c_x,c_y = float(c_x),float(c_y)    
    
    crossproduct = (c_y - a_y) * (b_x - a_x) - (c_x - a_x) * (b_y - a_y)
    if abs(crossproduct) > 0.001 : return False   # (or != 0 if using integers)

    dotproduct = (c_x - a_x) * (b_x - a_x) + (c_y - a_y)*(b_y - a_y)
    if dotproduct < 0 : return False

    squaredlengthba = (b_x - a_x)*(b_x - a_x) + (b_y - a_y)*(b_y - a_y)
    if dotproduct > squaredlengthba: return False

    return True

def det(a, b):
    return float(a[0]) * float(b[1]) - float(a[1]) * float(b[0])

def line_intersection(line1, line2):
    xdiff = (float(line1[0][0]) - float(line1[1][0]), float(line2[0][0]) - float(line2[1][0]))
    ydiff = (float(line1[0][1]) - float(line1[1][1]), float(line2[0][1]) - float(line2[1][1])) #Typo was here

    div = det(xdiff, ydiff)
    if div == 0:
        return False
       #raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / float(div)
    y = det(d, ydiff) / float(div)
    return x,y
        
    
        

            
            
            
            