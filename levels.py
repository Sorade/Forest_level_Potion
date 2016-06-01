# -*- coding: utf-8 -*-
"""
Created on Wed Jun 01 17:15:33 2016

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

class Level(object):
    def __init__(self, lvl_num):
        self.lvl_num = lvl_num
        self.run = False
        #create sprite groups
        self.player_list = pygame.sprite.Group()
        self.char_list = pygame.sprite.Group()
        self.ennemi_list = pygame.sprite.Group()
        self.item_list = pygame.sprite.Group()
        self.building_list = pygame.sprite.Group()
        self.projectile_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.deleted_list = pygame.sprite.Group()
        self.dead_sprites_list = pygame.sprite.Group()
        self.message_list = pygame.sprite.Group()
        self.to_blit_list = pygame.sprite.Group()
        
        self.sprite_group_list = []
        self.sprite_group_list.extend([self.player_list,self.char_list, self.projectile_list, self.dead_sprites_list, self.ennemi_list, self.item_list,self.building_list, self.all_sprites_list, self.to_blit_list, self.deleted_list])

class Level1(Level):
    def __init__(self, lvl_num):
        super(Level1, self).__init__(1)
        
    def execute(self):
        if self.run == True:
            for event in pygame.event.get(): #setting up quit
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    hero.get_dest() # sets the player's destination
                    
                    for o in self.ennemi_list:
                        hero.attack(o)
                    
                    for i in self.item_list:
                        i.use(hero)
                        
                    for i in self.building_list:
                        if isinstance(i,Chest):
                            i.open_(hero)
                                
                if event.type == v.set_ennemies_dest:
                    #print 'moves'
                    for o in self.char_list: 
                        if isinstance(o, Ranger): #moves characters
                            o.behaviour(hero)
        
                if event.type == v.set_ennemies_move:         
                    for o in self.char_list: 
                        if isinstance(o, Ranger): #moves characters
                            o.move()
            hero.get_offset() # sets the movement offset for the iteration
            #check_null_offset() #if player stops or is firing sets offsets to 0
            group_collision_check(self.building_list,hero) #edits the offest based on hero collision
            
            for o in self.ennemi_list:
                o.attack(hero)
                o.update_images()
                o.anim_move()
                
            for p in self.projectile_list: #moves projectiles
                p.move()
                for o in self.ennemi_list:
                    p.hit_test(o)
                    
            for d in self.dead_sprites_list:
                d.loot(hero)
    
                    
            #animations
            hero.update_images()
            hero.anim_move() #animates hero sprite
            #offset checks
            group_offset(self.building_list) #new building position using offset
            group_offset(self.item_list)
            scroll_map.offset() #offsets grass background map
            group_offset(self.ennemi_list)
            group_offset(self.dead_sprites_list)
            group_offset(self.projectile_list)
            
            #check if characters are dead before blitting:
            for Character in itertools.chain.from_iterable([variables.char_list,variables.player_list]):
                Character.is_alive()
            
            #blitting        
            v.screen.blit(scroll_map.image, scroll_map.rect) # blits the grass map to new pos
            self.building_list.draw(v.screen) #blits the buildings to new pos
            self.projectile_list.draw(v.screen)
                    
            if pygame.key.get_pressed()[pygame.K_e]: #blits highlight if e pressed
                for x in self.item_list:
                    x.highlight()
            
            self.dead_sprites_list.draw(v.screen) #blits corpses
            self.item_list.draw(v.screen) #blitting items
            self.ennemi_list.draw(v.screen) #blits ennemies
            v.screen.blit(hero.image, hero.rect) #blits hero to screen center 
            
            Lifebar(hero)#pygame.draw.rect(variables.screen, (245,0,0) , Rect(10,v.screenHEIGHT-30,hero.hp*10,10))
            for msg in self.message_list:
                msg.show()
            adjust_offset()
            
            if pygame.key.get_pressed()[pygame.K_i]:
                hero.inventory_opened = True
                hero.open_inventory()    