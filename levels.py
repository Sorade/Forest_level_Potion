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
        
        ##Instances
        #Characters
        #Creating the characters
        chars = []
        #hero = ins.hero
        sword_h = wp.Sword()
        sword_h.rect = sword_h.rect.move(50,50)
        
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
        #chest = Chest('Chest',2,var.chest_img, 300, 300, Sword())
        sword = wp.Sword()
        sword.name = 'warhammer'
        sword.wield = 'two_handed'
        sword2 = wp.Sword()
        sword2.name = 'axe'
        sword2.rect = sword2.rect.move(10,10)
        helm = ar.Helm()
        house = Building('House',10, var.house1_img, 350, 80, 80)
        self.scroll_map = Item('Map',0,var.background, 0, 0)
        self.all_sprites_list.add(house,ins.hero) 
        self.player_list.add(ins.hero)
        self.building_list.add(house)
        
        #random obstacles
        def add_obstacles(int):
            count = 0
            while count < 75:
                collides = True
                w = Building('obstacles',0,random.choice(var.obs_list),random.randint(25,1800),random.randint(75,1800),1000)
                collide_list = []
                test = pygame.sprite.spritecollideany(w, self.all_sprites_list, collided = None)
                if test is None:
                    self.building_list.add(w)
                    self.all_sprites_list.add(w)
                    count += 1
                
        #Random ennemies
        def add_ennemies(int):
            count = 0           
            while count < 10: #number of wanted enemies
                o = ch.Ranger(random.randint(450,1500),random.randint(450,1000))
                if random.randint(0,1) == 1:
                    o.equipement.contents.append(Potion(random.randint(7,10),random.randint(-3,5)))
                test = pygame.sprite.spritecollideany(o, self.all_sprites_list, collided = None)
                if test is None:      
                    count += 1
                    self.char_list.add(o)
                    self.ennemi_list.add(o)
                    self.all_sprites_list.add(o)
                    for item in o.equipement.contents: self.all_sprites_list.add(item)
                
        #random objects
        def add_chests(int):
            count = 0
            while count < 10:
                obj = [wp.Sword(),wp.Bow(),wp.Arrow(), ar.Helm()]
                collides = False
                chest_contents = []
                for n in range(0,random.randint(0,3)):
                    chest_contents.append(random.choice(obj))
                pos = Rect(random.randint(50,var.background.get_rect()[2]),random.randint(80,var.background.get_rect()[3]),var.chest_img.get_rect().width,var.chest_img.get_rect().height)
                w = it.Chest(0,0, chest_contents)
                w.rect = pos
            
                for c in self.all_sprites_list:
                    if isinstance(c,it.Chest) and w.rect.colliderect((c.rect.inflate(200,200))) == True:
                        collides = True
                        break
                test = pygame.sprite.spritecollideany(w, self.all_sprites_list, collided = None)
                if test is None and collides == False:
                    self.building_list.add(w)
                    self.all_sprites_list.add(w)
                    for item in w.inventory.contents:
                        self.all_sprites_list.add(item)
                    count +=1
                    
        add_obstacles(75)
        add_ennemies(10)
        add_chests(10)
        
        #self.set_level(self.all_sprites_list)
        
        
    def execute(self):
        if self.run == True:
            var.current_level = self
            [x for x in self.player_list][0].level = self
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
            
            self.leave(2)
                    
                    
class Level2(Level):
    def set_level(self, sprite_grp):
        for sprite in sprite_grp:
            sprite.level = self
    
    def __init__(self):
        super(Level2, self).__init__(1)
        
        ##Instances
        #Characters
        #Creating the characters
        chars = []
        #hero = ins.hero
        sword_h = wp.Sword()
        sword_h.rect = sword_h.rect.move(50,50)
        
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
        #chest = Chest('Chest',2,var.chest_img, 300, 300, Sword())
        sword = wp.Sword()
        sword.name = 'warhammer'
        sword.wield = 'two_handed'
        sword2 = wp.Sword()
        sword2.name = 'axe'
        sword2.rect = sword2.rect.move(10,10)
        helm = ar.Helm()
        house = Building('House',10, var.house1_img, 350, 80, 80)
        self.scroll_map = Item('Map',0,var.background, 0, 0)
        self.all_sprites_list.add(house,ins.hero) 
        self.player_list.add(ins.hero)
        self.building_list.add(house)
        
        #random obstacles
        def add_obstacles(int):
            count = 0
            while count < 75:
                collides = True
                w = Building('obstacles',0,random.choice(var.obs_list),random.randint(25,1800),random.randint(75,1800),1000)
                collide_list = []
                test = pygame.sprite.spritecollideany(w, self.all_sprites_list, collided = None)
                if test is None:
                    self.building_list.add(w)
                    self.all_sprites_list.add(w)
                    count += 1
                
        #Random ennemies
        def add_ennemies(int):
            count = 0           
            while count < 10: #number of wanted enemies
                o = ch.Ranger(random.randint(450,1500),random.randint(450,1000))
                if random.randint(0,1) == 1:
                    o.equipement.contents.append(Potion(random.randint(7,10),random.randint(-3,5)))
                test = pygame.sprite.spritecollideany(o, self.all_sprites_list, collided = None)
                if test is None:      
                    count += 1
                    self.char_list.add(o)
                    self.ennemi_list.add(o)
                    self.all_sprites_list.add(o)
                    for item in o.equipement.contents: self.all_sprites_list.add(item)
                
        #random objects
        def add_chests(int):
            count = 0
            while count < 10:
                obj = [wp.Sword(),wp.Bow(),wp.Arrow(), ar.Helm()]
                collides = False
                chest_contents = []
                for n in range(0,random.randint(0,3)):
                    chest_contents.append(random.choice(obj))
                pos = Rect(random.randint(50,var.background.get_rect()[2]),random.randint(80,var.background.get_rect()[3]),var.chest_img.get_rect().width,var.chest_img.get_rect().height)
                w = it.Chest(0,0, chest_contents)
                w.rect = pos
            
                for c in self.all_sprites_list:
                    if isinstance(c,it.Chest) and w.rect.colliderect((c.rect.inflate(200,200))) == True:
                        collides = True
                        break
                test = pygame.sprite.spritecollideany(w, self.all_sprites_list, collided = None)
                if test is None and collides == False:
                    self.building_list.add(w)
                    self.all_sprites_list.add(w)
                    for item in w.inventory.contents:
                        self.all_sprites_list.add(item)
                    count +=1
                    
        add_obstacles(75)
        add_ennemies(10)
        add_chests(10)
        
        #self.set_level(self.all_sprites_list)
        
        
    def execute(self):
        if self.run == True:
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

        #self.leave(1)
        if pygame.key.get_pressed()[pygame.K_v]:
            self.run = False
            variables.level_list[0].run = True