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

pygame.init()
clock = pygame.time.Clock()

pygame.time.set_timer(v.set_ennemies_dest, 1500) #for ennemi movement
pygame.time.set_timer(v.set_ennemies_move, int(1000/(v.FPS*0.7))) #for ennemi movement
pygame.mixer.init()
pygame.mixer.music.load('Theme3.ogg')
pygame.mixer.music.play(-1)

add_obstacles(75)
add_ennemies(10)
add_chests(10)

#game loop    
while True:
    clock.tick(v.FPS)
    v.screen.fill((0,0,0)) #make background black for map edges

    ####MAIN MAP LOOP
    if v.game_running == True:
        for event in pygame.event.get(): #setting up quit
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                hero.get_dest() # sets the player's destination
                
                for o in v.ennemi_list:
                    hero.attack(o)
                
                for i in v.item_list:
                    i.use(hero)
                    
                for i in v.building_list:
                    if isinstance(i,Chest):
                        i.open_(hero)
                            
            if event.type == v.set_ennemies_dest:
                #print 'moves'
                for o in v.char_list: 
                    if isinstance(o, Ranger): #moves characters
                        o.behaviour(hero)
    
            if event.type == v.set_ennemies_move:         
                for o in v.char_list: 
                    if isinstance(o, Ranger): #moves characters
                        o.move()
                        
        for p in v.projectile_list: #moves projectiles
            p.move()
            for o in v.ennemi_list:
                p.hit_test(o)
                        
        hero.get_offset() # sets the movement offset for the iteration if player stops or is firing sets offsets to 0
        hero.group_collision_check(v.building_list) #edits the offest based on hero collision

        hero.character_collisions()

        for o in v.ennemi_list:
            o.attack(hero)
            o.update_images()
            o.anim_move()
            
               
        for d in v.dead_sprites_list:
            d.loot(hero)

                
        #animations
        hero.update_images()
        hero.anim_move() #animates hero sprite
        print v.orientation
        #offset checks
        group_offset(v.building_list) #new building position using offset
        group_offset(v.item_list)
        scroll_map.offset() #offsets grass background map
        group_offset(v.ennemi_list)
        group_offset(v.dead_sprites_list)
        group_offset(v.projectile_list)
        
        #check if characters are dead before blitting:
        for Character in itertools.chain.from_iterable([variables.char_list,variables.player_list]):
            if Character.is_alive() == True:
                Character.is_alive() 
        
        #blitting        
        v.screen.blit(scroll_map.image, scroll_map.rect) # blits the grass map to new pos
        v.building_list.draw(v.screen) #blits the buildings to new pos
        v.projectile_list.draw(v.screen)
                
        if pygame.key.get_pressed()[pygame.K_e]: #blits highlight if e pressed
            for x in v.item_list:
                x.highlight()
        
        v.dead_sprites_list.draw(v.screen) #blits corpses
        v.item_list.draw(v.screen) #blitting items
        v.ennemi_list.draw(v.screen) #blits ennemies
        v.screen.blit(hero.image, hero.rect) #blits hero to screen center 
        
        Lifebar(hero)#pygame.draw.rect(variables.screen, (245,0,0) , Rect(10,v.screenHEIGHT-30,hero.hp*10,10))
        for msg in v.message_list:
            msg.show()
            
        adjust_offset()
        
        if pygame.key.get_pressed()[pygame.K_i]:
            hero.inventory_opened = True
            hero.open_inventory()
        
    pygame.display.update()
    
#    pos_y = 100
#for k, v in inv.items():
#    text = font.render("{0}: {1}".format(k, v), True, WHITE)
#    screen.blit(text, (30, pos_y))
#    pos_y += 40  # That's the offset.

    
