# -*- coding: utf-8 -*-
"""
Created on Fri May 13 19:43:28 2016

@author: Julien
"""
import pygame
import variables
import random
from classes import Character,Projectile,Weapon,Armor
import weapons as wp
import armors as ar

class Ranger(Character):
    def __init__(self, x, y):
        self.hp = 15
        self.speed = 48.0/(variables.FPS*0.7)
        self.CC = 30.0
        self.CT = 50.0
        # Call the parent class (Sprite) constructor
        super(Ranger, self).__init__(self.hp, variables.skl_walk_images, variables.skl_attack_images, self.speed, x, y, self.CC, self.CT)
        self.equipement.contents.extend([wp.Sword(),ar.Leather_armor()])
        self.attack_speed = 1000
        self.F = 20
        self.E = 20
        self.dead_image = variables.dead_ennemi


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
                self.image_list = images[1]
                break
            if isinstance(item,wp.Sword):
                self.image_list = images[0]
#                if isinstance(item,Shied()):
#                    self.image_list = variables.pshield_images
        
#    def anim_move1(self):
#        #updates attack timer
#        self.attack_time.tick()
#        self.attack_time_left += self.attack_time.get_time()
#        #check if attack time has elapsed, if so, ends combat anim by reverting to walk imagelist
#        if  self.attack_time_left <= self.attack_speed and self.has_attack == True: #
#            self.anim_list = self.attack_images
#        else:
#            self.has_attack = False
#            self.anim_list = self.image_list
#
#        self.anim_time.tick()
#        self.anim_time_left += self.anim_time.get_time()
#        if self.anim_time_left >= self.anim_speed: #checks time to animate
#            if self.orientation >= 140 and self.orientation <= 220: #checks orientation
#                if self.anim_counter == 4:
#                    self.anim_counter = 0
#                self.image = self.anim_list[self.anim_counter]
#            elif self.orientation >= 220 and self.orientation <= 320: #checks orientation
#                if self.anim_counter ==4:
#                    self.anim_counter = 0
#                self.image = self.anim_list[self.anim_counter+4]  
#            elif self.orientation >= 321 or self.orientation <= 40: #checks orientation
#                if self.anim_counter == 4:
#                    self.anim_counter = 0
#                self.image = self.anim_list[self.anim_counter+8]
#            elif self.orientation >= 40 and self.orientation <= 140: #checks orientation
#                if self.anim_counter == 4:
#                    self.anim_counter = 0
#                self.image = pygame.transform.flip(self.anim_list[self.anim_counter+4] , True, False)
#            self.anim_time_left = 0
#            self.anim_counter += 1
        
            
class Player(Character):
    def __init__(self):
        self.hp = 14
        self.image = variables.walk_images[0][0]
        self.x = (variables.screenWIDTH/2)-(self.image.get_rect()[2]/2.)
        self.y = (variables.screenHEIGHT/2)-(self.image.get_rect()[3]/2.)
        self.speed = 3
        self.CC = 100.0
        self.CT = 50.0
        # Call the parent class (Sprite) constructor
        super(Player, self).__init__(self.hp, variables.walk_images, variables.attack_images, self.speed, self.x, self.y, self.CC, self.CT)
        self.equipement.contents.extend([wp.Bow(),wp.Arrow()])
        self.attack_speed = 500
        self.F = 35
        self.E = 35
        self.dead_image = variables.dead_player
        
    def attack(self, Character):
        if Character.rect.inflate(10,10).collidepoint(pygame.mouse.get_pos()) == True and len([x for x in self.equipement.contents if isinstance (x,Projectile)]) > 0 and len([x for x in [y for y in self.equipement.contents if isinstance (y,Weapon)] if x.type == 'CT']) > 0:
            variables.has_shot = True
        '''attack timer update is done in the anim method'''
        #self.attack_time.tick()
        #self.attack_time_left += self.attack_time.get_time()
        if self.attack_time_left >= self.attack_speed:
            if Character.is_alive() == True and Character.rect.inflate(15,15).collidepoint(pygame.mouse.get_pos()):
                if Character.rect.colliderect(self.rect.inflate(self.rect.width,self.rect.height)) == True:
                    self.has_attack = True
                    test = random.randint(1,100) <= self.CC
                    if test == True:
                        dmg = sum([x.dmg for x in self.equipement.contents if isinstance(x, Weapon) == True]) #sum of the values of all weapons in equipement
                        arm = sum([x.arm for x in Character.equipement.contents if isinstance(x, Armor) == True]) #sum of the values of all weapons in equipement
                        if (dmg+self.F/10)-(arm+Character.E/10) < 0:
                            dmg = 0
                        else:
                            dmg = (dmg+self.F/10)-(arm+Character.E/10)
                        Character.hp -=  dmg
                        print 'player deals {} dmg'.format(dmg)
                    self.attack_time_left = 0
                    '''make sure if is correct rather than elif, might need a has_shot variable'''
                elif Character.rect.inflate(10,10).colliderect(self.rect) == False and len([x for x in self.equipement.contents if isinstance (x,Projectile)]) > 0 and len([x for x in [y for y in self.equipement.contents if isinstance (y,Weapon)] if x.type == 'CT']) > 0: #checks clicks ennemi and has ammo 
                    wp.Arrow().fire(self)
                    self.attack_time_left = 0
#                if Character.is_alive() == False:
#                    Character.kill()
#                    variables.dead_sprites_list.add(Character) #adds the character to the deleted sprite list
#                    Character.image_list = variables.dead_ennemi
    
    def update_images(self):
        #updates attack timer
        self.attack_time.tick()
        self.attack_time_left += self.attack_time.get_time()
        #check if attack time has elapsed, if so, ends combat anim by reverting to walk imagelist
        self.temp = 0
        if  (self.attack_time_left <= self.attack_speed and self.has_attack == True) or (self.attack_time_left <= self.attack_speed and self.anim_shot == True):
            print 'should'
            self.temp = self.attack_images
            
        else:
            self.has_attack = False
            self.anim_shot = False
            self.temp = self.walk_images
            
        for item in self.equipement.contents:
            if isinstance(item,wp.Bow):
                self.image_list = self.temp[1]
                break
            if isinstance(item,wp.Sword):
                self.image_list = self.temp[0]
#                if isinstance(item,Shied()):
#                    self.image_list = variables.pshield_images

            
    def anim_move(self):
        #updates anim timer
        self.anim_time.tick()
        self.anim_time_left += self.anim_time.get_time()
        #checks which anim to display based on the direction and if sprite is moving and alive
        if self.anim_time_left >= self.anim_speed and self.is_alive() == True: #checks time to animate
            if variables.orientation >= 140 and variables.orientation <= 220: #checks orientation
                if self.anim_counter >= 4:
                    self.anim_counter = 0
                self.image = self.image_list[self.anim_counter]
                if variables.xoffset == 0 and variables.yoffset == 0 and self.has_attack == False and self.anim_shot == False:
                    self.image = self.image_list[0]
            elif variables.orientation >= 220 and variables.orientation <= 320: #checks orientation
                if self.anim_counter >= 4:
                    self.anim_counter = 0
                self.image =self.image_list[self.anim_counter+4]  
                if variables.xoffset == 0 and variables.yoffset == 0 and self.has_attack == False and self.anim_shot == False:
                    self.image = self.image_list[4]
            elif variables.orientation >= 321 or variables.orientation <= 40: #checks orientation
                if self.anim_counter >= 4:
                    self.anim_counter = 0
                self.image = self.image_list[self.anim_counter+8]
                if variables.xoffset == 0 and variables.yoffset == 0 and self.has_attack == False and self.anim_shot == False:
                    self.image = self.image_list[8]
            elif variables.orientation >= 40 and variables.orientation <= 140: #checks orientation
                if self.anim_counter >= 4:
                    self.anim_counter = 0
                self.image = self.image_list[self.anim_counter+12]
                if variables.xoffset == 0 and variables.yoffset == 0 and self.has_attack == False and self.anim_shot == False:
                    self.image = self.image_list[12]#pygame.transform.flip(self.anim_list[4], True, False)
            self.anim_time_left = 0
            self.anim_counter += 1

