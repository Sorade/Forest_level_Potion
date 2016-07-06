# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 20:48:16 2016

@author: Julien
"""
#import pygame, sys, variables
#import weapons as wp
import characters as ch
#import armors as ar
#import items as it
#from pygame.locals import *
#from classes import *

##Instances
#Characters
#Creating the characters
#chars = []
hero = ch.Player()
#sword_h = wp.Sword()
#sword_h.rect = sword_h.rect.move(50,50)




##Level Edges
#for x in range(0,26):
#    y = random.randint(1,2)
#    if y == 1:
#        image = variables.tree_pack_ew
#    else:
#        image = pygame.transform.flip(variables.tree_pack_ew, True, False)
#    if x < 13:
#        w = Building('top_edge',0,image,x*152,-5, 1000)
#    elif x < 50 :
#        w = Building('bot_edge',0,variables.tree_pack_ew,(x-13)*152,1960, 1000)
#    variables.building_list.add(w)
#    variables.all_sprites_list.add(w)
#    
#for x in range(0,56):
#    if x < 28:
#        w = Building('wall_left',0,variables.pine_ns,-10,x*74, 1000)
#    else:
#        w = Building('wall_right',0,variables.pine_ns,2018,(x-28)*74, 1000)        
#    variables.building_list.add(w)
#    variables.all_sprites_list.add(w)
    
   
##Objects
##chest = Chest('Chest',2,variables.chest_img, 300, 300, Sword())
#sword = wp.Sword()
#sword.name = 'warhammer'
#sword.wield = 'two_handed'
#sword2 = wp.Sword()
#sword2.name = 'axe'
#sword2.rect = sword2.rect.move(10,10)
#helm = ar.Helm()
#house = Building('House',10, variables.house1_img, 350, 80, 80)
#scroll_map = Item('Map',0,variables.background, 0, 0)
#variables.all_sprites_list.add(house,hero) 
#variables.player_list.add(hero)
#variables.building_list.add(house)
#
##random obstacles
#def add_obstacles(int):
#    count = 0
#    while count < 75:
#        collides = True
#        w = Building('obstacles',0,random.choice(variables.obs_list),random.randint(25,1800),random.randint(75,1800),1000)
#        collide_list = []
#        test = pygame.sprite.spritecollideany(w, variables.all_sprites_list, collided = None)
#        if test is None:
#            variables.building_list.add(w)
#            variables.all_sprites_list.add(w)
#            count += 1
#        
##Random ennemies
#def add_ennemies(int):
#    count = 0           
#    while count < 10: #number of wanted enemies
#        o = ch.Skeleton(random.randint(450,1500),random.randint(450,1000))
#        if random.randint(0,1) == 1:
#            o.equipement.contents.append(Potion(random.randint(7,10),random.randint(-3,5)))
#        test = pygame.sprite.spritecollideany(o, variables.all_sprites_list, collided = None)
#        if test is None:      
#            count += 1
#            variables.char_list.add(o)
#            variables.ennemi_list.add(o)
#            variables.all_sprites_list.add(o)
#        
##random objects
#def add_chests(int):
#    obj = [wp.Sword(),wp.Bow(),wp.Arrow(), ar.Helm()]
#    count = 0
#    while count < 10:
#        collides = False
#        chest_contents = []
#        for n in range(0,random.randint(0,3)):
#            chest_contents.append(random.choice(obj))
#        pos = Rect(random.randint(50,variables.background.get_rect()[2]),random.randint(80,variables.background.get_rect()[3]),variables.chest_img.get_rect().width,variables.chest_img.get_rect().height)
#        w = it.Chest(0,0, chest_contents)
#        w.rect = pos
#    
#        for c in variables.all_sprites_list:
#            if isinstance(c,it.Chest) and w.rect.colliderect((c.rect.inflate(200,200))) == True:
#                collides = True
#                break
#        test = pygame.sprite.spritecollideany(w, variables.all_sprites_list, collided = None)
#        if test is None and collides == False:
#            variables.building_list.add(w)
#            variables.all_sprites_list.add(w)
#            count +=1
        


