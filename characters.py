# -*- coding: utf-8 -*-
"""
Created on Fri May 13 19:43:28 2016

@author: Julien
"""
import pygame
import variables
import random
from functions import d10
from classes import Character,Projectile,Weapon,Armor,SpriteStripAnim
import weapons as wp
import armors as ar
from pygame.locals import *

class Skeleton(Character):# to change to Orc
    def __init__(self, x, y):
        self.hp = 16
        self.speed = int(48.0/(variables.FPS*0.7))
        self.CC = 30.0
        self.CT = 50.0
        # Call the parent class (Sprite) constructor
        super(Skeleton, self).__init__(self.hp, variables.skl_walk_images, variables.skl_attack_images, self.speed, x, y, self.CC, self.CT)
        self.equipement.contents.extend(random.choice([[wp.Bow(), wp.Arrow(d10(1)), ar.Leather_armor()],[wp.Sword(), ar.Leather_armor()]]))
        self.inventory.contents.extend([ar.Leather_armor()])
        self.attack_speed = 1000
        self.F = 20
        self.E = 20
        
        '''Sprite Sheet Variables'''
        self.strips = [#Walking Mace
                       SpriteStripAnim(variables.orc_ss, 32, (16,524,32,60), 9, None, True, variables.FPS/6),#North
                       SpriteStripAnim(variables.orc_ss, 32, (16,592,32,60), 9, None, True, variables.FPS/6),#West
                       SpriteStripAnim(variables.orc_ss, 32, (16,656,32,60), 9, None, True, variables.FPS/6),#South
                       SpriteStripAnim(variables.orc_ss, 32, (16,710,32,60), 9, None, True, variables.FPS/6),#East
                       #Attacking Mace
                       SpriteStripAnim(variables.orc_ss, 120, (56,1416,71,60), 6, None, True, variables.FPS/8),#North
                       SpriteStripAnim(variables.orc_ss, 120, (56,1608,71,60), 6, None, True, variables.FPS/8),#West
                       SpriteStripAnim(variables.orc_ss, 120, (56,1800,71,60), 6, None, True, variables.FPS/8),#South
                       SpriteStripAnim(variables.orc_ss, 120, (56,2000,71,60), 6, None, True, variables.FPS/8),
                       #Walking Bow
                       SpriteStripAnim(variables.orc_bow_ss, 32, (16,524,32,60), 9, None, True, variables.FPS/6),#North
                       SpriteStripAnim(variables.orc_bow_ss, 32, (16,592,32,60), 9, None, True, variables.FPS/6),#West
                       SpriteStripAnim(variables.orc_bow_ss, 32, (16,656,32,60), 9, None, True, variables.FPS/6),#South
                       SpriteStripAnim(variables.orc_bow_ss, 32, (16,710,32,60), 9, None, True, variables.FPS/6),#East
                       #Attacking Bow
                       SpriteStripAnim(variables.orc_bow_ss, 4, (0,1031,60,60), 13, None, True, variables.FPS/8),#North
                       SpriteStripAnim(variables.orc_bow_ss, 4, (0,1096,60,60), 13, None, True, variables.FPS/8),#West
                       SpriteStripAnim(variables.orc_bow_ss, 4, (0,1157,60,60), 13, None, True, variables.FPS/8),#South
                       SpriteStripAnim(variables.orc_bow_ss, 4, (0,1224,60,60), 13, None, True, variables.FPS/8)]#East
        self.n = 0
        self.strips[self.n].iter()
        self.image = self.strips[self.n].next()

        
    def anim_move(self):
        '''checks equipement to display'''
        x = 0*8 #default value if no item is equiped
        for item in self.equipement.contents:
            if isinstance(item,wp.Bow):
                x = 1*8
                break
            if isinstance(item,wp.Axe):
                x = 2*8
                break
            if isinstance(item,wp.Sword):
                x = 0*8

        '''checks if attack anim needs to terminate'''
        self.attack_time.tick()
        self.attack_time_left += self.attack_time.get_time()
        if self.attack_time_left >= self.attack_speed:
            self.has_attack = False
             
        #checks which anim to display based on the direction and if sprite is moving and alive
        if self.hp > 0:
            if self.is_moving == True: #checks time to animate
                if self.orientation >= 140 and self.orientation <= 220: #South
                    self.n = 2+x
                    self.image = self.strips[self.n].next()
                elif self.orientation >= 220 and self.orientation <= 320: #West
                    self.n = 1+x
                    self.image = self.strips[self.n].next()            
                elif self.orientation >= 320 or self.orientation <= 40: #North
                    self.n = 0+x
                    self.image = self.strips[self.n].next()            
                elif self.orientation >= 40 and self.orientation <= 140: #East
                    self.n = 3+x
                    self.image = self.strips[self.n].next()
                    
            if self.has_attack == True: #checks time to animate
                if self.orientation >= 140 and self.orientation <= 220: #checks orientation
                    self.n = 6+x
                    self.image = self.strips[self.n].next()
                elif self.orientation >= 220 and self.orientation <= 320: #checks orientation
                    self.n = 5+x
                    self.image = self.strips[self.n].next()            
                elif self.orientation >= 320 or self.orientation <= 40: #checks orientation
                    self.n = 4+x
                    self.image = self.strips[self.n].next()            
                elif self.orientation >= 40 and self.orientation <= 140: #checks orientation
                    self.n = 7+x
                    self.image = self.strips[self.n].next()
                    
            '''char is not moving, next is not invoked'''        
            if self.has_attack == False and self.is_moving == False:
                if self.orientation >= 140 and self.orientation <= 220: #checks orientation
                    self.n = 2+x
                    self.image = self.strips[self.n].images[0]
                elif self.orientation >= 220 and self.orientation <= 320: #checks orientation
                    self.n = 1+x
                    self.image = self.strips[self.n].images[0]
                elif self.orientation >= 320 or self.orientation <= 40: #checks orientation
                    self.n = 0+x
                    self.image = self.strips[self.n].images[0]
                elif self.orientation >= 40 and self.orientation <= 140: #checks orientation
                    self.n = 3+x
                    self.image = self.strips[self.n].images[0]
             
            
                
                
                
    def update_images(self):
        pass
#        #updates attack timer
#        self.attack_time.tick()
#        self.attack_time_left += self.attack_time.get_time()
#        #check if attack time has elapsed, if so, ends combat anim by reverting to walk imagelist
#        if  self.attack_time_left <= self.attack_speed and self.has_attack == True:
#            images = self.attack_images
#            
#        else:
#            self.has_attack = False
#            images = self.walk_images
#            
#        for item in self.equipement.contents:
#            if isinstance(item,wp.Bow):
#                self.image_list = images[0]#should be 1
#                break
#            if isinstance(item,wp.Sword):
#                self.image_list = images[0]
##                if isinstance(item,Shied()):
##                    self.image_list = variables.pshield_images

class Orc(Character): #to change to Skeleton
    def __init__(self, x, y):
        self.hp = 15
        self.speed = int(48.0/(variables.FPS*0.7))
        self.CC = 30.0
        self.CT = 50.0
        # Call the parent class (Sprite) constructor
        super(Skeleton, self).__init__(self.hp, variables.skl_walk_images, variables.skl_attack_images, self.speed, x, y, self.CC, self.CT)
        self.equipement.contents.extend(random.choice([[wp.Sword(),wp.Bow(), wp.Arrow(d10(1)), ar.Leather_armor()],[wp.Sword(), ar.Leather_armor()]]))
        self.attack_speed = 1000
        self.F = 20
        self.E = 20
        

    def update_images(self):
        #updates attack timer
        self.attack_time.tick()
        self.attack_time_left += self.attack_time.get_time()
        #check if attack time has elapsed, if so, ends combat anim by reverting to walk imagelist
        if  self.attack_time_left <= self.attack_speed and self.has_attack == True:
            images = self.attack_images
            
        else:
            self.has_attack = False
            images = self.walk_images
            
        for item in self.equipement.contents:
            if isinstance(item,wp.Bow):
                self.image_list = images[0]#should be 1
                break
            if isinstance(item,wp.Sword):
                self.image_list = images[0]
#                if isinstance(item,Shied()):
#                    self.image_list = variables.pshield_images
        
        
            
class Player(Character):
    def __init__(self):
        self.hp = 250
        self.image = variables.walk_images[0][0]
        self.x = (variables.screenWIDTH/2)-(self.image.get_rect()[2]/2.)
        self.y = (variables.screenHEIGHT/2)-(self.image.get_rect()[3]/2.)
        self.speed = 3
        self.CC = 100.0
        self.CT = 50.0
        # Call the parent class (Sprite) constructor
        super(Player, self).__init__(self.hp, variables.walk_images, variables.attack_images, self.speed, self.x, self.y, self.CC, self.CT)
        self.equipement.contents.extend([wp.Sword()])
        self.inventory.contents.extend([wp.Bow(),wp.Arrow(10),wp.Axe()])
        self.attack_speed = 500
        self.F = 35
        self.E = 35
        self.dead_image = variables.dead_player if random.randint(0,1) == 0 else pygame.transform.flip(variables.dead_player, True, False)

        '''Sprite Sheet Variables'''
        self.strips = [#Walking Sword
                       SpriteStripAnim(variables.player_sword_ss, 32, (16,520,32,55), 9, None, True, variables.FPS/8),#North
                       SpriteStripAnim(variables.player_sword_ss, 32, (16,580,32,60), 9, None, True, variables.FPS/8),#West
                       SpriteStripAnim(variables.player_sword_ss, 32, (16,650,32,55), 9, None, True, variables.FPS/8),#South
                       SpriteStripAnim(variables.player_sword_ss, 32, (16,710,32,60), 9, None, True, variables.FPS/8),#East
                       #Attacking Sword
                       SpriteStripAnim(variables.player_sword_ss, 120, (56,1416,71,60), 6, None, True, variables.FPS/8),#North
                       SpriteStripAnim(variables.player_sword_ss, 120, (56,1607,71,60), 6, None, True, variables.FPS/8),#West
                       SpriteStripAnim(variables.player_sword_ss, 120, (56,1800,71,60), 6, None, True, variables.FPS/8),#South
                       SpriteStripAnim(variables.player_sword_ss, 120, (56,1993,71,60), 6, None, True, variables.FPS/8),#East
                       #Walking Bow
                       SpriteStripAnim(variables.player_bow_ss, 32, (16,520,32,55), 9, None, True, variables.FPS/8),#North
                       SpriteStripAnim(variables.player_bow_ss, 32, (16,580,32,60), 9, None, True, variables.FPS/8),#West
                       SpriteStripAnim(variables.player_bow_ss, 32, (16,650,32,55), 9, None, True, variables.FPS/8),#South
                       SpriteStripAnim(variables.player_bow_ss, 32, (16,710,32,60), 9, None, True, variables.FPS/8),#East
                       #Attacking Bow
                       SpriteStripAnim(variables.player_bow_ss, 4, (0,1031,60,60), 13, None, True, variables.FPS/13),#North
                       SpriteStripAnim(variables.player_bow_ss, 4, (0,1096,60,60), 13, None, True, variables.FPS/13),#West
                       SpriteStripAnim(variables.player_bow_ss, 4, (0,1157,60,60), 13, None, True, variables.FPS/13),#South
                       SpriteStripAnim(variables.player_bow_ss, 4, (0,1224,60,60), 13, None, True, variables.FPS/13),
                        #Walking Mace
                       SpriteStripAnim(variables.player_mace_ss, 32, (16,520,32,55), 9, None, True, variables.FPS/8),#North
                       SpriteStripAnim(variables.player_mace_ss, 32, (16,580,32,60), 9, None, True, variables.FPS/8),#West
                       SpriteStripAnim(variables.player_mace_ss, 32, (16,650,32,55), 9, None, True, variables.FPS/8),#South
                       SpriteStripAnim(variables.player_mace_ss, 32, (16,710,32,60), 9, None, True, variables.FPS/8),#East
                       #Attacking Mace
                       SpriteStripAnim(variables.player_mace_ss, 120, (56,1416,71,60), 6, None, True, variables.FPS/6),#North
                       SpriteStripAnim(variables.player_mace_ss, 120, (56,1607,71,60), 6, None, True, variables.FPS/6),#West
                       SpriteStripAnim(variables.player_mace_ss, 120, (56,1800,71,60), 6, None, True, variables.FPS/6),#South
                       SpriteStripAnim(variables.player_mace_ss, 120, (56,1993,71,60), 6, None, True, variables.FPS/6)]#East
        self.n = 0
        self.strips[self.n].iter()
        self.image = self.strips[self.n].next()



    def group_collision_check(self,group):
        for sprite in group: #checks if sprite collide with character using test_rect
            
            if (variables.dx  == 0 and variables.dy == 0) == False:
                #check x xollision
                test_rect = Rect(self.rect.midleft,(self.rect.width,self.rect.height/2))
                test_rect = test_rect.move(-variables.xoffset,0)#.inflate(-test_rect.width/8,-test_rect.height/10)
                if test_rect.colliderect(sprite.rect.inflate(-self.rect.width/1.2,-sprite.rect.height/10)):
                    variables.xoffset = 0 #set x offset to 0 for global use
                    variables.yoffset += variables.xoffset
                #check y collision
                test_rect = Rect(self.rect.midleft,(self.rect.width,self.rect.height/2)) #resets test_rect to initial sprite position
                test_rect = test_rect.move(0,-variables.yoffset)#.inflate(-10,-5)
                if test_rect.colliderect(sprite.rect.inflate(-self.rect.width/1.2,-sprite.rect.height/10)):
                    variables.yoffset = 0 #set y offset to 0 for global use
                    variables.xoffset += variables.yoffset

    def character_collisions(self):
        test_rect = Rect(self.rect.midleft,(self.rect.width,self.rect.height/2))   
        for obstacle in self.level.ennemi_list:
            if test_rect.colliderect(obstacle.rect.inflate(-obstacle.rect.width/2,-obstacle.rect.height/10)) == True:
                dx = obstacle.rect.centerx-self.rect.centerx
                dy = obstacle.rect.centery-self.rect.centery
                if dx > 0 and  0 < self.orientation < 180:
                    variables.xoffset = 0 #set x offset to 0 for global use
                if dx < 0 and  180 < self.orientation < 360:
                    variables.xoffset = 0 #set x offset to 0 for global use
                if dy > 0 and  90 < self.orientation < 270:
                    variables.yoffset = 0 #set y offset to 0 for global use
                if dy < 0 and  (270 < self.orientation < 360) == True or (0 < self.orientation < 90) == True:
                    variables.yoffset = 0 #set y offset to 0 for global use
                break
            
    def attack(self, Character):
        if Character.rect.inflate(10,10).collidepoint(pygame.mouse.get_pos()) == True and len([x for x in self.equipement.contents if isinstance (x,Projectile)]) > 0 and len([x for x in [y for y in self.equipement.contents if isinstance (y,Weapon)] if x.type == 'CT']) > 0:
            variables.has_shot = True
        '''attack timer update is done in the anim method'''
        self.attack_time.tick()
        self.attack_time_left += self.attack_time.get_time()
        if self.attack_time_left >= self.attack_speed:
            #self.has_attack = False
            if Character.is_alive() == True and Character.rect.inflate(15,15).collidepoint(pygame.mouse.get_pos()):
                self.merge_ammo()
                self.has_attack = True
                if Character.rect.inflate(Character.rect.width,Character.rect.height).colliderect(self.rect.inflate(self.rect.width,self.rect.height)) == True:
                    #self.has_attack = True
                    test = random.randint(1,100) <= self.CC
                    if test == True:
                        dmg = sum([x.random_dmg() for x in self.equipement.contents if isinstance(x, Weapon) == True]) #sum of the values of all weapons in equipement
                        arm = sum([x.arm for x in Character.equipement.contents if isinstance(x, Armor) == True]) #sum of the values of all weapons in equipement
                        if (dmg+self.F/10)-(arm+Character.E/10) < 0:
                            dmg = 0
                        else:
                            dmg = (dmg+self.F/10)-(arm+Character.E/10)
                        Character.hp -=  dmg
                        print 'player deals {} dmg'.format(dmg)
                    self.attack_time_left = 0
                    '''make sure if is correct rather than elif, might need a has_shot variable'''
                elif Character.rect.inflate(10,10).colliderect(self.rect) == False and len([y for y in [x for x in self.equipement.contents if isinstance (x,Projectile)] if y.ammo > 0]) > 0 and len([x for x in [y for y in self.equipement.contents if isinstance (y,Weapon)] if x.type == 'CT']) > 0: #checks clicks ennemi and has ammo 
                    for proj in [x for x in self.equipement.contents if isinstance (x,Projectile)]:
#                        proj.name = '{} {}'.format(proj.ammo, proj.raw_name)
                        if proj.ammo > 0:
                            proj.ammo -= 1
                            break
                    projectile = wp.Arrow(0)
                    projectile.fire(self,pygame.mouse.get_pos(),self.level.projectile_list) #in this function the pojectile level attribute needs to be already set
                    self.attack_time_left = 0
        
    def update_images(self):
        pass
#        #updates attack timer
#        self.attack_time.tick()
#        self.attack_time_left += self.attack_time.get_time()
#        #check if attack time has elapsed, if so, ends combat anim by reverting to walk imagelist
#        self.temp = 0
#        if  (self.attack_time_left <= self.attack_speed and self.has_attack == True) or (self.attack_time_left <= self.attack_speed and self.anim_shot == True):
#            self.temp = self.attack_images
#            
#        else:
#            self.has_attack = False
#            self.anim_shot = False
#            self.temp = self.walk_images
#            
#        for item in self.equipement.contents:
#            if isinstance(item,wp.Bow):
#                self.image_list = self.temp[1]
#                break
#            if isinstance(item,wp.Axe):
#                self.image_list = self.temp[0]
#                break
#            if isinstance(item,wp.Sword):
#                self.image_list = self.temp[0]


            
#    def anim_move(self):
#        #updates anim timer
#        self.anim_time.tick()
#        self.anim_time_left += self.anim_time.get_time()
#        #checks which anim to display based on the direction and if sprite is moving and alive
#        if self.anim_time_left >= self.anim_speed and self.is_alive() == True: #checks time to animate
#            if self.orientation >= 135 and self.orientation <= 225: # goes south checks orientation
#                if self.anim_counter >= 4:
#                    self.anim_counter = 0
#                self.image = self.image_list[self.anim_counter]
#                if variables.xoffset == 0 and variables.yoffset == 0 and self.has_attack == False and self.anim_shot == False:
#                    self.image = self.image_list[0]
#            elif self.orientation >= 225 and self.orientation <= 315: #goes west checks orientation
#                if self.anim_counter >= 4:
#                    self.anim_counter = 0
#                self.image =self.image_list[self.anim_counter+4]  
#                if variables.xoffset == 0 and variables.yoffset == 0 and self.has_attack == False and self.anim_shot == False:
#                    self.image = self.image_list[4]
#            elif self.orientation >= 315 or self.orientation <= 45: # goes North checks orientation
#                if self.anim_counter >= 4:
#                    self.anim_counter = 0
#                self.image = self.image_list[self.anim_counter+8]
#                if variables.xoffset == 0 and variables.yoffset == 0 and self.has_attack == False and self.anim_shot == False:
#                    self.image = self.image_list[8]
#            elif self.orientation >= 45 and self.orientation <= 135: #goes East checks orientation
#                if self.anim_counter >= 4:
#                    self.anim_counter = 0
#                self.image = self.image_list[self.anim_counter+12]
#                if variables.xoffset == 0 and variables.yoffset == 0 and self.has_attack == False and self.anim_shot == False:
#                    self.image = self.image_list[12]#pygame.transform.flip(self.anim_list[4], True, False)
#            self.anim_time_left = 0
#            self.anim_counter += 1
            
    def anim_move(self):
        '''checks equipement to display'''
        x = 0*8 #default value if no item is equiped
        for item in self.equipement.contents:
            if isinstance(item,wp.Bow):
                x = 1*8
                break
            if isinstance(item,wp.Axe):
                x = 2*8
                break
            if isinstance(item,wp.Sword):
                x = 0*8

        '''checks if attack anim needs to terminate'''
        self.attack_time.tick()
        self.attack_time_left += self.attack_time.get_time()
        if self.attack_time_left >= self.attack_speed:
            self.has_attack = False
        
        '''checks if player is stopped'''
        if variables.xoffset == 0 and variables.yoffset == 0:
            self.is_moving = False
        else:
            self.is_moving = True
            
        '''checks which anim to display based on the direction
        and if sprite is moving and alive'''
        if self.hp > 0:
            if self.is_moving == True: #checks time to animate
                if self.orientation >= 140 and self.orientation <= 220: #South
                    self.n = 2+x
                    self.image = self.strips[self.n].next()
                elif self.orientation >= 220 and self.orientation <= 320: #West
                    self.n = 1+x
                    self.image = self.strips[self.n].next()            
                elif self.orientation >= 320 or self.orientation <= 40: #North
                    self.n = 0+x
                    self.image = self.strips[self.n].next()            
                elif self.orientation >= 40 and self.orientation <= 140: #East
                    self.n = 3+x
                    self.image = self.strips[self.n].next()
                    
            if self.has_attack == True: #checks time to animate
                if self.orientation >= 140 and self.orientation <= 220: #checks orientation
                    self.n = 6+x
                    self.image = self.strips[self.n].next()
                    #self.strips[self.n].iter()
                elif self.orientation >= 220 and self.orientation <= 320: #checks orientation
                    self.n = 5+x
                    self.image = self.strips[self.n].next()            
                elif self.orientation >= 320 or self.orientation <= 40: #checks orientation
                    self.n = 4+x
                    self.image = self.strips[self.n].next()            
                elif self.orientation >= 40 and self.orientation <= 140: #checks orientation
                    self.n = 7+x
                    self.image = self.strips[self.n].next()
                    
            if self.has_attack == False and self.is_moving == False:
                if self.orientation >= 140 and self.orientation <= 220: #checks orientation
                    self.n = 2+x
                    self.image = self.strips[self.n].images[0]
                elif self.orientation >= 220 and self.orientation <= 320: #checks orientation
                    self.n = 1+x
                    self.image = self.strips[self.n].images[0]
                elif self.orientation >= 320 or self.orientation <= 40: #checks orientation
                    self.n = 0+x
                    self.image = self.strips[self.n].images[0]
                elif self.orientation >= 40 and self.orientation <= 140: #checks orientation
                    self.n = 3+x
                    self.image = self.strips[self.n].images[0]
