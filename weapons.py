# -*- coding: utf-8 -*-
"""
Created on Wed May 11 18:54:14 2016

@author: Julien
"""
import variables, random
from classes import Weapon, Projectile

class Arrow(Projectile):
    def __init__(self, ammo): #name, value, image, x, y, dmg
        self.name = 'Arrows'
        self.value = 5
        self.image = variables.quiver_img
        self.speed = 4
        self.dmg = 2
        self.dmg_modif = 1
        super(Arrow, self).__init__(self.name, self.value, self.image, 200, 150, self.speed, self.dmg, self.dmg_modif, ammo)

class Sword(Weapon):
    def __init__(self): #name, value, image, x, y, dmg
        self.type = 'CC'
        self.wield = 'one_handed'
        self.range = 15
        self.dmg = 1
        self.dmg_modif = 1
        self.name = 'Sword'
        self.value = 12
        self.image = variables.sword_img
        super(Sword, self).__init__(self.name, self.value, self.image, 150, 150, self.dmg, self.dmg_modif)
        
class Bow(Weapon):
    def __init__(self): #name, value, image, x, y, dmg
        self.type = 'CT'
        self.wield = 'two_handed'
        self.range = 50
        self.dmg = 1
        self.dmg_modif = 1
        self.name = 'Bow'
        self.value = 12
        self.image = variables.bow_img
        super(Bow, self).__init__(self.name, self.value, self.image, 250, 250, self.dmg, self.dmg_modif)
        
class Longbow(Bow):
    def __init__(self): #name, value, image, x, y, dmg
        self.type = 'CT'
        self.wield = 'two_handed'
        self.range = 100
        self.dmg = 2
        self.dmg_modif = 1
        self.name = 'Longbow'
        self.value = 16
        self.image = variables.bow_img
        super(Longbow, self).__init__(self.name, self.value, self.image, 150, 150, self.dmg, self.dmg_modif)
