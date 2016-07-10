# -*- coding: utf-8 -*-
"""
Created on Wed May 11 18:54:14 2016

@author: Julien
"""
import pygame
import variables, random
from functions import d10
from classes import Weapon, Projectile

class Arrow(Projectile):
    def __init__(self, ammo): #name, value, image, x, y, dmg
        self.raw_name = 'Arrows'
        self.name = '{} {}'.format(ammo, self.raw_name)
        self.value = 5
        self.range = 400
        self.image = variables.quiver_img
        self.speed = 4
        self.dmg = 1
        self.dmg_modif = 1
        super(Arrow, self).__init__(self.name, self.value, self.image, 200, 150, self.speed, self.dmg, self.dmg_modif, ammo , self.range)

class Sword(Weapon):
    def __init__(self): #name, value, image, x, y, dmg
        self.type = 'CC'
        self.wield = 'one_handed'
        self.range = 7
        self.dmg = 1
        self.dmg_modif = 1
        self.name = 'Sword'
        self.value = 12
        self.image = variables.items_ss.image_at(pygame.Rect(64,128,32,32))
        self.icon = variables.weapon_icons.image_at(pygame.Rect(542,242,56,56))
        self.description = 'A short iron sword. Damage of 1d10+1.'
        super(Sword, self).__init__(self.name, self.value, self.image, self.icon, 150, 150, self.dmg, self.dmg_modif)

class Axe(Weapon):
    def __init__(self): #name, value, image, x, y, dmg
        self.type = 'CC'
        self.wield = 'two_handed'
        self.range = 5
        self.dmg = 3
        self.dmg_modif = 1
        self.name = 'Axe'
        self.value = 24
        self.image = variables.axe_img
        self.icon = variables.weapon_icons.image_at(pygame.Rect(122,2,56,56))
        self.description = 'A war axe. Damage of 1d10+3.'
        super(Axe, self).__init__(self.name, self.value, self.image, self.icon, 150, 150, self.dmg, self.dmg_modif)

class Mace(Weapon):
    def __init__(self): #name, value, image, x, y, dmg
        self.type = 'CC'
        self.wield = 'one_handed'
        self.range = 5
        self.dmg = 2
        self.dmg_modif = 1
        self.name = 'Mace'
        self.value = 16
        self.image = variables.items_ss.image_at(pygame.Rect(66,296,32,32))
        self.icon = variables.weapon_icons.image_at(pygame.Rect(298,298,56,56))
        self.description = 'A steel mace. Damage of 1d10+2.'
        super(type(self), self).__init__(self.name, self.value, self.image, self.icon, 150, 150, self.dmg, self.dmg_modif)
        
class Bow(Weapon):
    def __init__(self): #name, value, image, x, y, dmg
        self.type = 'CT'
        self.wield = 'two_handed'
        self.range = 400+d10(2)
        self.dmg = 1
        self.dmg_modif = 1
        self.name = 'Bow'
        self.value = 12
        self.image = variables.items_ss.image_at(pygame.Rect(161,33,30,30))
        self.icon = variables.weapon_icons.image_at(pygame.Rect(542,2,56,56))
        self.description = 'A simple bow. Damage of 1d10+1. Range of 400+2d10'
        super(Bow, self).__init__(self.name, self.value, self.image, self.icon, 250, 250, self.dmg, self.dmg_modif)
        
class Longbow(Bow):
    def __init__(self):
        super(Longbow, self).__init__()
        self.range = 450+d10(2)
        self.dmg = 2
        self.dmg_modif = 1
        self.name = 'Longbow'
        self.value = 16
        self.image = variables.bow_img
        self.icon = variables.weapon_icons.image_at(pygame.Rect(2,62,56,56))
        self.description = 'A yew longbow. Damage of 1d10+2. Range of 450+2d10'
