# -*- coding: utf-8 -*-
"""
Created on Wed Jun 01 17:15:33 2016

@author: Julien
"""
import pygame, sys
import variables as var
from pygame.locals import *
from classes import *
from functions import *
import instances as ins
import weapons as wp
import characters as ch
import armors as ar
import items as it
from pygame.locals import *
from classes import *

class Level1(Level):
    def set_level(self, sprite_grp):
        for sprite in sprite_grp:
            sprite.level = self
    
    def __init__(self):
        super(Level1, self).__init__(1)
        
        #Level Edges
        for x in range(0,26):
            y = random.randint(1,2)
            if y == 1:
                image = var.tree_pack_ew
            else:
                image = pygame.transform.flip(var.tree_pack_ew, True, False)
            if x < 13:
                w = Building('top_edge',0,image,x*152,-5, 1000)
            elif x < 50 :
                w = Building('bot_edge',0,var.tree_pack_ew,(x-13)*152,1960, 1000)
            self.building_list.add(w)
            self.all_sprites_list.add(w)
            
        for x in range(0,56):
            if x < 28:
                w = Building('wall_left',0,var.pine_ns,-10,x*74, 1000)
            else:
                w = Building('wall_right',0,var.pine_ns,2018,(x-28)*74, 1000)        
            self.building_list.add(w)
            self.all_sprites_list.add(w)
            
           
        #Objects
        house = Building('House',10, var.house1_img, 350, 80, 80)
        self.portal = Portal(1500,200,1)
        self.portal2 = Portal(100,1720,1)
        
        self.scroll_map = Item('Map',0,var.background, 0, 0)
        self.all_sprites_list.add(house,ins.hero,self.portal,self.portal2) 
        self.player_list.add(ins.hero)
        self.building_list.add(house,self.portal,self.portal2)
        
        self.add_obstacles(150,var.obs_list)
        self.add_ennemies(10,[ch.Ranger])
        self.add_chests(4,it.Chest,[wp.Arrow(random.randint(2,5)),wp.Sword(),wp.Bow(), ar.Helm()])#,wp.Sword(),wp.Bow(), ar.Helm()
        
        #self.set_level(self.all_sprites_list)
        
        
    def execute(self):
        if self.run == True:
#            var.current_level = self
#            [x for x in self.player_list][0].level = self
            super(Level1, self).execute()
            for event in pygame.event.get(): #setting up quit
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    print 'has quit'
                if event.type == MOUSEBUTTONDOWN:
                    ins.hero.get_dest() # sets the player's destination
                    
                    for o in self.ennemi_list:
                        ins.hero.attack(o)
                    
                    for i in self.item_list:
                        i.use(ins.hero)
                        
                    for i in self.building_list:
                        if isinstance(i,it.Chest):
                            i.open_(ins.hero)
                                
            for o in self.char_list: 
                if isinstance(o, ch.Ranger): #sets mobs dest characters
                    o.behaviour(ins.hero)
        
            for o in self.char_list: 
                if isinstance(o, ch.Ranger): #moves characters
                    o.move()
            
            for p in self.projectile_list: #moves projectiles
                p.move()
                for o in self.ennemi_list:
                    p.hit_test(o)
                            
            ins.hero.get_offset() # sets the movement offset for the iteration if player stops or is firing sets offsets to 0
            ins.hero.group_collision_check(self.building_list) #edits the offest based on ins.hero collision
            ins.hero.character_collisions()
    
            for o in self.ennemi_list:
                o.attack(ins.hero)
                o.update_images()
                o.anim_move()
                
                   
            for d in self.dead_sprites_list:
                d.loot(ins.hero)
    
                    
            #animations
            ins.hero.update_images()
            ins.hero.anim_move() #animates ins.hero sprite
            #offset checks
            group_offset(self.building_list) #new building position using offset
            group_offset(self.item_list)
            self.scroll_map.offset() #offsets grass background map
            group_offset(self.ennemi_list)
            group_offset(self.dead_sprites_list)
            group_offset(self.projectile_list)
            
            #check if characters are dead before blitting:
            for Character in itertools.chain.from_iterable([self.char_list,self.player_list]):
                if Character.is_alive() == True:
                    Character.is_alive() 
            
            #blitting        
            var.screen.blit(self.scroll_map.image, self.scroll_map.rect) # blits the grass map to new pos
            self.building_list.draw(var.screen) #blits the buildings to new pos
            self.projectile_list.draw(var.screen)
                    
            if pygame.key.get_pressed()[pygame.K_e]: #blits highlight if e pressed
                for x in self.item_list:
                    x.highlight()
            
            self.dead_sprites_list.draw(var.screen) #blits corpses
            self.item_list.draw(var.screen) #blitting items
            self.ennemi_list.draw(var.screen) #blits ennemies
            var.screen.blit(ins.hero.image, ins.hero.rect) #blits hero to screen center 
            
            Lifebar(ins.hero)
            for msg in self.message_list:
                msg.show()
                
            adjust_offset()
            
            '''dirty loop to get the player's inv_delay timer values'''
            for player in self.player_list:
                player.inv_time.tick()
                player.inv_time_left += player.inv_time.get_time()
                if pygame.key.get_pressed()[pygame.K_i] and player.inv_time_left > player.inv_delay:
                    ins.hero.inventory_opened = True
                    ins.hero.open_inventory()
            
            #self.go_to(2)
            for x in self.building_list:
                if isinstance(x, Level_Change):
                    x.activate(ins.hero,2)
                    
                    
class Level2(Level):
    def set_level(self, sprite_grp):
        for sprite in sprite_grp:
            sprite.level = self
    
    def __init__(self):
        super(Level2, self).__init__(1)
        self.scroll_map = Item('Map',0,var.dirt_map, 0, 0)
        
        #Level Edges
        for x in range(0,26):
            y = random.randint(1,2)
            if y == 1:
                image = var.mound
            else:
                image = pygame.transform.flip(var.mound, True, False)
            if x < 13:
                w = Building('top_edge',0,image,x*153,-50, 1000)
            elif x < 50 :
                w = Building('bot_edge',0,image,(x-13)*153,1960, 1000)
            self.building_list.add(w)
            self.all_sprites_list.add(w)
            
        for x in range(0,56):
            if x < 28:
                w = Building('wall_left',0,var.rocks[5],-5,x*74, 1000)
            else:
                w = Building('wall_right',0,var.rocks[5],2000,(x-28)*74, 1000)        
            self.building_list.add(w)
            self.all_sprites_list.add(w)
            
           
        #Objects
        self.portal = Portal(50,1000,1)
        self.portal2 = Portal(250,1800,1)
        self.all_sprites_list.add(ins.hero, self.portal,self.portal2) 
        self.player_list.add(ins.hero)
        self.building_list.add(self.portal,self.portal2)
        
        self.add_obstacles(75,var.dirt_list)
        self.add_ennemies(10,[ch.Ranger])
        self.add_chests(5,it.Chest,[wp.Arrow(random.randint(2,5)),wp.Axe(),wp.Bow(), ar.Plate_armor()])
        
    def execute(self):
        if self.run == True:
            super(Level2, self).execute()
            for event in pygame.event.get(): #setting up quit
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    print 'has quit'
                if event.type == MOUSEBUTTONDOWN:
                    ins.hero.get_dest() # sets the player's destination
                    
                    for o in self.ennemi_list:
                        ins.hero.attack(o)
                    
                    for i in self.item_list:
                        i.use(ins.hero)
                        
                    for i in self.building_list:
                        if isinstance(i,it.Chest):
                            i.open_(ins.hero)
                                
            for o in self.char_list: 
                if isinstance(o, ch.Ranger): #sets mobs dest characters
                    o.behaviour(ins.hero)
        
            for o in self.char_list: 
                if isinstance(o, ch.Ranger): #moves characters
                    o.move()
            
            for p in self.projectile_list: #moves projectiles
                p.move()
                for o in self.ennemi_list:
                    p.hit_test(o)
                            
            ins.hero.get_offset() # sets the movement offset for the iteration if player stops or is firing sets offsets to 0
            ins.hero.group_collision_check(self.building_list) #edits the offest based on ins.hero collision
            ins.hero.character_collisions()
    
            for o in self.ennemi_list:
                o.attack(ins.hero)
                o.update_images()
                o.anim_move()
                
                   
            for d in self.dead_sprites_list:
                d.loot(ins.hero)
    
                    
            #animations
            ins.hero.update_images()
            ins.hero.anim_move() #animates ins.hero sprite
            #offset checks
            group_offset(self.building_list) #new building position using offset
            group_offset(self.item_list)
            self.scroll_map.offset() #offsets grass background map
            group_offset(self.ennemi_list)
            group_offset(self.dead_sprites_list)
            group_offset(self.projectile_list)
            
            #check if characters are dead before blitting:
            for Character in itertools.chain.from_iterable([self.char_list,self.player_list]):
                if Character.is_alive() == True:
                    Character.is_alive() 
            
            #blitting        
            var.screen.blit(self.scroll_map.image, self.scroll_map.rect) # blits the grass map to new pos
            self.building_list.draw(var.screen) #blits the buildings to new pos
            self.projectile_list.draw(var.screen)
                    
            if pygame.key.get_pressed()[pygame.K_e]: #blits highlight if e pressed
                for x in self.item_list:
                    x.highlight()
            
            self.dead_sprites_list.draw(var.screen) #blits corpses
            self.item_list.draw(var.screen) #blitting items
            self.ennemi_list.draw(var.screen) #blits ennemies
            var.screen.blit(ins.hero.image, ins.hero.rect) #blits hero to screen center 
            
            Lifebar(ins.hero)
            for msg in self.message_list:
                msg.show()
                
            adjust_offset()
            
            '''dirty loop to get the player's inv_delay timer values'''
            for player in self.player_list:
                player.inv_time.tick()
                player.inv_time_left += player.inv_time.get_time()
                if pygame.key.get_pressed()[pygame.K_i] and player.inv_time_left > player.inv_delay:
                    ins.hero.inventory_opened = True
                    ins.hero.open_inventory()
                    
            for x in self.building_list:
                if isinstance(x, Level_Change):
                    x.activate(ins.hero,1)
        #self.go_to(1)
#        if pygame.key.get_pressed()[pygame.K_v]:
#            new_level = var.level_list[0]
#            self.run = False
#            [x for x in self.player_list][0].level = new_level
#            new_level.run = True
#            var.current_level = new_level