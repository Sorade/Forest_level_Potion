# -*- coding: utf-8 -*-
"""
Created on Wed Jun 01 17:15:33 2016

@author: Julien
"""
import pygame, sys
import itertools
import random
import variables as var
from pygame.locals import *
from functions import *
from classes import *
import weapons as wp
import armors as ar
import items as it
import characters as ch
import instances as ins


class StartMenu(Level):
    def __init__(self):
        self.run = True
        self.rain_y = -600
        self.do_once = True
        self.start_but = Button('Play Game', var.screenWIDTH/2-len('play ')*5,int(var.screenHEIGHT*(8.5/10)),75,50)  
    
    def execute(self,new_level):
        if self.run == True:
            if self.do_once == True:
                self.do_once = False
                pygame.mixer.music.load("Sounds\\startmusic.ogg")
                pygame.mixer.music.play(-1,0.0)
                pygame.mixer.find_channel().play(var.rain_sound,-1)  
                
                
            for event in pygame.event.get(): #setting up quit
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    print 'has quit'
                elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    print 'has quit'
            
            '''Background of menu and sounds'''
            var.screen.blit(var.start_bg,(0,0))
            var.screen.blit(var.start_rain,(0,self.rain_y))    
            
            
            if random.randint(0,100) == 10:
                var.screen.blit(var.start_flash,(0,0))
                thunder = random.choice(var.thunder_sounds)
                thunder.set_volume(random.random()+0.2)
                pygame.mixer.find_channel().play(thunder)
                

            self.rain_y += 15
            if self.rain_y >= 0:
                self.rain_y = -200
            
            '''Menu buttons'''
            self.start_but.check_select()
            self.start_but.display()
            
            if self.start_but.selected == True:
                print 'go game'
                self.run = False
                new_level.run = True
                pygame.mixer.stop()
                pygame.mixer.music.load("Theme3.ogg")
                pygame.mixer.music.play(-1,0.0)
        



class Level1(Level):
#    def set_level(self, sprite_grp):
#        for sprite in sprite_grp:
#            sprite.level = self
    
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
        
        self.add_obstacles(75,var.obs_list)
        self.add_char(10,[ch.Orc],'ennemy')
        self.add_char(3,[ch.Ranger],'ally')
        self.add_char(1,[ch.Ent],'ennemy')
        self.add_chests(14,it.Chest,[wp.Arrow(random.randint(2,5)),wp.Bow(), ar.Helm()])#,wp.Sword(),wp.Bow(), ar.Helm()
        
#        chest_items = itertools.chain.from_iterable([chest.inventory.contents for chest in self.building_list if isinstance(chest, it.Chest)])

#        '''Night Mask'''
#        self.night_m = Night_Mask()
#        self.assign_occluders(itertools.chain.from_iterable([self.item_list,ins.hero.inventory.contents,chest_items]))
#        self.assign_radius(itertools.chain.from_iterable([self.item_list,ins.hero.inventory.contents,chest_items]))
        
        
    def execute(self):
        if self.run == True:
            super(type(self), self).execute()
            
            if self.do_once == True:
                statsmenu_access = False
                invmenu_access = False
                
            '''check if access to menus are allowed'''
            if pygame.key.get_pressed()[pygame.K_s] == False:
                statsmenu_access = True
            if pygame.key.get_pressed()[pygame.K_i] == False:
                invmenu_access = True
                
            for event in pygame.event.get(): #setting up quit
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    print 'has quit'
                elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
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
                            
#            for o in self.ennemi_list: 
#                o.behaviour(ins.hero)
#                o.move()
                
            for o in self.char_list:
                if o in self.ennemi_list:
                    o.behaviour(itertools.chain.from_iterable([self.ally_list,self.player_list])) #checks is enemy attacks hero or ally
                if o in self.ally_list:
                    o.behaviour(self.ennemi_list) #checks is ally attacks ennemy
                o.move()
                
            for p in self.projectile_list: #moves projectiles
                p.move()
                for o in self.ennemi_list:
                    p.hit_test(o)
                    
            for p in self.projectile_ennemy_list: 
                p.move() #moves enemy projectiles
                for o in itertools.chain.from_iterable([self.ally_list,self.player_list]):
                    p.hit_test(o)
                            
            ins.hero.get_offset() # sets the movement offset for the iteration if player stops or is firing sets offsets to 0
            ins.hero.group_collision_check(self.building_list) #edits the offest based on ins.hero collision
            ins.hero.character_collisions()
    
            for o in self.char_list:
                o.anim_move()
                
                   
            for d in self.dead_sprites_list:
                d.loot(ins.hero)
                
            #check to turn lights on/off
            for i in (x for x in ins.hero.inventory.contents if isinstance(x, Illuminator)):
                i.onoff()
                
            #animations
#            ins.hero.update_images()
            ins.hero.anim_move() #animates ins.hero sprite
            #offset checks
            group_offset(self.building_list) #new building position using offset
            group_offset(self.item_list)
            self.scroll_map.offset() #offsets grass background map
            group_offset(self.char_list)
            group_offset(self.dead_sprites_list)
            group_offset(self.projectile_list)
            group_offset(self.projectile_ennemy_list)
            
            #check if characters are dead before blitting:
            for Character in itertools.chain.from_iterable([self.char_list,self.player_list]):
                if Character.is_alive() == True:
                    Character.is_alive() 
            
            '''blitting  '''      
            var.screen.blit(self.scroll_map.image, self.scroll_map.rect) # blits the grass map to new pos
            self.building_list.draw(var.screen) #blits the buildings to new pos
            self.projectile_list.draw(var.screen)
            self.projectile_ennemy_list.draw(var.screen)
                    
            if pygame.key.get_pressed()[pygame.K_e]: #blits highlight if e pressed
                for x in self.item_list:
                    x.highlight()
                    
            self.dead_sprites_list.draw(var.screen) #blits corpses
            blit_visible(var.screen,self.item_list) #blitting items
            self.char_list.draw(var.screen) #blits ennemies
            var.screen.blit(ins.hero.image, ins.hero.rect) #blits hero to screen center 
            
            for e in self.char_list:
                e.image = e.strips[e.n].next()
                
#            #night mask    
#            self.night_m.day_update(220)
#            self.night_m.apply_shadows([x for x in self.item_list if isinstance(x, Illuminator)],self.building_list,ins.hero)
#            var.screen.blit(self.night_m.surf_lighting,(0,0),special_flags=BLEND_MULT)
            
            '''HUD DISPLAY'''
            Lifebar(ins.hero)
            HUDbar(ins.hero)
           
            for msg in self.message_list:
                msg.show()
                
            adjust_offset()
            
            '''checking access to menus'''
            for player in self.player_list:
                if statsmenu_access == True and pygame.key.get_pressed()[pygame.K_s]:
                    player.stats_menu.execute(player.level,player)
                if invmenu_access == True and pygame.key.get_pressed()[pygame.K_i]:
                    ins.hero.inventory_opened = True
                    ins.hero.open_inventory()
                    
            '''checking Portals'''
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
        self.add_char(15,[ch.Skeleton],'ennemy')
        self.add_chests(5,it.Chest,[wp.Arrow(random.randint(2,5)),wp.Mace(),wp.Bow(), ar.Plate_armor()])
        
    def execute(self):
        if self.run == True:
            super(type(self), self).execute()
            
            if self.do_once == True:
                statsmenu_access = False
                invmenu_access = False
                
            '''check if access to menus are allowed'''
            if pygame.key.get_pressed()[pygame.K_s] == False:
                statsmenu_access = True
            if pygame.key.get_pressed()[pygame.K_i] == False:
                invmenu_access = True
                
            for event in pygame.event.get(): #setting up quit
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    print 'has quit'
                elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
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
                            
#            for o in self.ennemi_list: 
#                o.behaviour(ins.hero)
#                o.move()
                
            for o in self.char_list:
                if o in self.ennemi_list:
                    o.behaviour(itertools.chain.from_iterable([self.ally_list,self.player_list])) #checks is enemy attacks hero or ally
                if o in self.ally_list:
                    o.behaviour(self.ennemi_list) #checks is ally attacks ennemy
                o.move()
                
            for p in self.projectile_list: #moves projectiles
                p.move()
                for o in self.ennemi_list:
                    p.hit_test(o)
                    
            for p in self.projectile_ennemy_list: 
                p.move() #moves enemy projectiles
                for o in itertools.chain.from_iterable([self.ally_list,self.player_list]):
                    p.hit_test(o)
                            
            ins.hero.get_offset() # sets the movement offset for the iteration if player stops or is firing sets offsets to 0
            ins.hero.group_collision_check(self.building_list) #edits the offest based on ins.hero collision
            ins.hero.character_collisions()
    
            for o in self.char_list:
                o.anim_move()
                
                   
            for d in self.dead_sprites_list:
                d.loot(ins.hero)
                
            #check to turn lights on/off
            for i in (x for x in ins.hero.inventory.contents if isinstance(x, Illuminator)):
                i.onoff()
                
            #animations
#            ins.hero.update_images()
            ins.hero.anim_move() #animates ins.hero sprite
            #offset checks
            group_offset(self.building_list) #new building position using offset
            group_offset(self.item_list)
            self.scroll_map.offset() #offsets grass background map
            group_offset(self.char_list)
            group_offset(self.dead_sprites_list)
            group_offset(self.projectile_list)
            group_offset(self.projectile_ennemy_list)
            
            #check if characters are dead before blitting:
            for Character in itertools.chain.from_iterable([self.char_list,self.player_list]):
                if Character.is_alive() == True:
                    Character.is_alive() 
            
            '''blitting  '''      
            var.screen.blit(self.scroll_map.image, self.scroll_map.rect) # blits the grass map to new pos
            self.building_list.draw(var.screen) #blits the buildings to new pos
            self.projectile_list.draw(var.screen)
            self.projectile_ennemy_list.draw(var.screen)
                    
            if pygame.key.get_pressed()[pygame.K_e]: #blits highlight if e pressed
                for x in self.item_list:
                    x.highlight()
                    
            self.dead_sprites_list.draw(var.screen) #blits corpses
            blit_visible(var.screen,self.item_list) #blitting items
            self.char_list.draw(var.screen) #blits ennemies
            var.screen.blit(ins.hero.image, ins.hero.rect) #blits hero to screen center 
            
            for e in self.char_list:
                e.image = e.strips[e.n].next()
                
#            #night mask    
#            self.night_m.day_update(220)
#            self.night_m.apply_shadows([x for x in self.item_list if isinstance(x, Illuminator)],self.building_list,ins.hero)
#            var.screen.blit(self.night_m.surf_lighting,(0,0),special_flags=BLEND_MULT)
            
            '''HUD DISPLAY'''
            Lifebar(ins.hero)
            HUDbar(ins.hero)
           
            for msg in self.message_list:
                msg.show()
                
            adjust_offset()
            
            '''checking access to menus'''
            for player in self.player_list:
                if statsmenu_access == True and pygame.key.get_pressed()[pygame.K_s]:
                    player.stats_menu.execute(player.level,player)
                if invmenu_access == True and pygame.key.get_pressed()[pygame.K_i]:
                    ins.hero.inventory_opened = True
                    ins.hero.open_inventory()
                    
            '''checking Portals'''
            for x in self.building_list:
                if isinstance(x, Level_Change):
                    x.activate(ins.hero,1)