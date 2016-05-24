# -*- coding: utf-8 -*-
"""
Created on Fri May 13 19:52:20 2016

@author: Julien
"""
import pygame
import variables
import random
from classes import Item, Inventory, Message, Potion
import functions as fn

class Chest(Item):
    def __init__(self,x, y, contents_list):
        self.name = 'Chest'
        self.value = 0
        self.image = variables.chest_img
        super(Chest, self).__init__(self.name, self.value, self.image, x, y)
        self.has_opened = False
        self.inventory = Inventory()
        
        for k in contents_list:
            self.inventory.contents.append(k)
            
    def open_(self,Character):
        if self.rect.collidepoint(pygame.mouse.get_pos()) == True and Character.rect.colliderect(self.rect.inflate(5,5)) == True: 
            if len(self.inventory.contents) >= 1:
                for item in self.inventory.contents:
                    print 'removes item from chest'
                    item.rect = self.pop_around(item,45,45)
                    print item.rect
                    variables.item_list.add(item) #add's sprite back to item list for it to behave as item in game
                    self.inventory.contents.remove(item) #removes item from chest
            else:
                w = 150
                h = 30
                msg = Message('The chest is empty !!',2000, 0,0,w,h)
                #msg.image = pygame.transform.scale(msg.image, (w, h))
                msg.rect.center = (variables.screenWIDTH/2,25)
                variables.message_list.add(msg)
                
                
                