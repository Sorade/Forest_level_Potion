# -*- coding: utf-8 -*-
"""
Created on Fri May 13 19:53:54 2016

@author: Julien
"""

import variables
from classes import Armor, Helm, Torso_armor

#class Helm(Armor):
#    def __init__(self): #name, value, image, x, y, dmg
#        self.name = 'Helm'
#        self.value = 10
#        self.arm = 2
#        self.image = variables.helm_img
#        super(Helm, self).__init__(self.name, self.value, self.image, 200, 150, self.arm)

class Leather_armor(Torso_armor):
    def __init__(self): #name, value, image, x, y, dmg
        self.name = 'Leather armor'
        self.value = 5
        self.arm = 1
        self.image = variables.leather_armor_img
        super(Leather_armor, self).__init__(self.name, self.value, self.image, self.arm)
  
class Plate_armor(Torso_armor):
    def __init__(self): #name, value, image, x, y, dmg
        self.name = 'Plate armor'
        self.value = 5
        self.arm = 3
        self.image = variables.plate_armor_img
        super(Plate_armor, self).__init__(self.name, self.value, self.image, self.arm)

      
