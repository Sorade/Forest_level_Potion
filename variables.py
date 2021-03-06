# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 19:06:37 2016

@author: Julien
"""


import pygame, sys
from pygame.locals import *

pygame.mixer.init()
pygame.init()
#Variables
screenRES = pygame.display.Info()
screenWIDTH = screenRES.current_w#800#680
screenHEIGHT = screenRES.current_h#600#480
#screen = pygame.display.set_mode((screenWIDTH, screenHEIGHT), pygame.SRCALPHA, 32)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

'''getting screen corners and segments'''
rct = screen.get_rect()
screen_corners = [rct.topleft,rct.topright,rct.bottomright,rct.bottomleft]
screen_segments = []
xoffset = 0
yoffset = 0
dx = 0
dy = 0
orientation = 0
selected = False
selected_button = 0
start_pos = (0,0)
do_once = True
has_shot = False
game_running = True

class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.set_colorkey((0,0,0))
        image.blit(self.sheet, (0, 0), rect)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
        
    def load_strip(self,spacing, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = []          
        for x in range(image_count):
            if x != 0:
                tups += [(rect[0]+(rect[2]+spacing)*x, rect[1], rect[2], rect[3])]
            else:
                tups += [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])]
        return self.images_at(tups, colorkey)  


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

current_level = Level(1)

level_list = []
#Importing Chars

    
#player attack
p_a_sword_images = []
p_w_sword_images = []
p_a_bow_images = []
p_w_bow_images = []
walk_images = [p_w_sword_images,p_w_bow_images]
attack_images = [p_a_sword_images,p_a_bow_images]

for xyz in ['Down','Left','Up','Right']:
    for n in range(0,4):
        p_a_sword_images.append(pygame.image.load('Character_Sprites\\attack\\sword\\{}_{}.png'.format(xyz,n+1)).convert_alpha())

for xyz in ['Down','Left','Up','Right']:
    for n in range(0,4):
        p_w_sword_images.append(pygame.image.load('Character_Sprites\\walk\\sword\\{}_{}.png'.format(xyz,n+1)).convert_alpha())

for xyz in ['Down','Left','Up','Right']:
    for n in range(0,4):
        p_a_bow_images.append(pygame.image.load('Character_Sprites\\attack\\bow\\{}_{}.png'.format(xyz,n+1)).convert_alpha())

for xyz in ['Down','Left','Up','Right']:
    for n in range(0,4):
        p_w_bow_images.append(pygame.image.load('Character_Sprites\\walk\\bow\\{}_{}.png'.format(xyz,n+1)).convert_alpha())

dead_player = pygame.image.load('Character_Sprites\\dead.png').convert_alpha()
                 

skl_a_sword_images = []
skl_w_sword_images = []

gobm_down_1 = pygame.image.load('Skeleton_Sprites\\walk\\Down_1.png').convert_alpha()
gobm_down_2 = pygame.image.load('Skeleton_Sprites\\walk\\Down_2.png').convert_alpha()
gobm_down_3 = pygame.image.load('Skeleton_Sprites\\walk\\Down_3.png').convert_alpha()
gobm_down_4 = pygame.image.load('Skeleton_Sprites\\walk\\Down_4.png').convert_alpha()

gobm_lat_1 = pygame.image.load('Skeleton_Sprites\\walk\\Left_1.png').convert_alpha()
gobm_lat_2 = pygame.image.load('Skeleton_Sprites\\walk\\Left_2.png').convert_alpha()
gobm_lat_3 = pygame.image.load('Skeleton_Sprites\\walk\\Left_3.png').convert_alpha()
gobm_lat_4 = pygame.image.load('Skeleton_Sprites\\walk\\Left_4.png').convert_alpha()

gobm_up_1 = pygame.image.load('Skeleton_Sprites\\walk\\Up_1.png').convert_alpha()
gobm_up_2 = pygame.image.load('Skeleton_Sprites\\walk\\Up_2.png').convert_alpha()
gobm_up_3 = pygame.image.load('Skeleton_Sprites\\walk\\Up_3.png').convert_alpha()
gobm_up_4 = pygame.image.load('Skeleton_Sprites\\walk\\Up_4.png').convert_alpha()

gobm_right_1 = pygame.transform.flip(gobm_lat_1, True, False)
gobm_right_2 = pygame.transform.flip(gobm_lat_2, True, False)
gobm_right_3 = pygame.transform.flip(gobm_lat_3, True, False)
gobm_right_4 = pygame.transform.flip(gobm_lat_4, True, False)

skl_w_sword_images = [
gobm_down_1,gobm_down_2,gobm_down_3,gobm_down_4,
gobm_lat_1,gobm_lat_2,gobm_lat_3,gobm_lat_4,
gobm_up_1,gobm_up_2,gobm_up_3,gobm_up_4,
gobm_right_1,gobm_right_2,gobm_right_3,gobm_right_4]

goba_down_1 = pygame.image.load('Skeleton_Sprites\\attack\\Down_1.png').convert_alpha()
goba_down_2 = pygame.image.load('Skeleton_Sprites\\attack\\Down_2.png').convert_alpha()
goba_down_3 = pygame.image.load('Skeleton_Sprites\\attack\\Down_3.png').convert_alpha()
goba_down_4 = pygame.image.load('Skeleton_Sprites\\attack\\Down_4.png').convert_alpha()

skl_a_sword_images = [goba_down_1, goba_down_2, goba_down_3, goba_down_4,
                 goba_down_1, goba_down_2, goba_down_3, goba_down_4,
                 goba_down_1, goba_down_2, goba_down_3, goba_down_4,
                 goba_down_1, goba_down_2, goba_down_3, goba_down_4]

skl_walk_images = [skl_w_sword_images]
skl_attack_images = [skl_a_sword_images]

dead_ennemi = pygame.image.load('Skeleton_Sprites\\dead.png').convert_alpha()

'''Spritesheets'''
orc_ss = spritesheet('Orc_Sprites\\Orc_Sprite_Sheet.png')
orc_bow_ss = spritesheet('Orc_Sprites\\Orc_Archer_Sheet.png')
player_sword_ss = spritesheet('Character_Sprites\\Sword_sheet.png')
player_bow_ss =spritesheet('Character_Sprites\\Archer_sheet.png')
player_mace_ss =spritesheet('Character_Sprites\\Mace_sheet.png')

'''start menu imports'''
start_bg = pygame.image.load('Object_Sprites\\startmenu_bg.png').convert_alpha()
start_bg = pygame.transform.smoothscale(start_bg, (screenWIDTH, screenHEIGHT))
start_flash = pygame.image.load('Object_Sprites\\startmenu_flash.png').convert_alpha()
start_flash = pygame.transform.smoothscale(start_flash, (screenWIDTH, screenHEIGHT))
start_rain = pygame.image.load('Object_Sprites\\startmenu_rain.png').convert_alpha()

#start_music = pygame.mixer.music.load("Sounds\\start_music.ogg")
rain_sound = pygame.mixer.Sound("Sounds\\Rain.ogg")
thunder_sounds = []

for x in range(1,4):
    thunder_sounds.append(pygame.mixer.Sound("Sounds\\Thunder{}.wav".format(x)))

'''object import'''

portal_images = []
for x in range(1,7):
    portal_images.append(pygame.image.load('Object_Sprites\\portal{}.png'.format(x)).convert_alpha())

torch_img = pygame.image.load('Object_Sprites\\torch_lit.png').convert_alpha()
chest_img = pygame.image.load('Object_Sprites\\chest.png').convert()
sword_img = pygame.image.load('Object_Sprites\\sword_small.png').convert()
sword_img.set_colorkey((0,0,0))
axe_img = pygame.image.load('Object_Sprites\\axe.png').convert_alpha()


bow_img = pygame.image.load('Object_Sprites\\longbow.png').convert()
bow_img.set_colorkey((0,0,0))

quiver_img = pygame.image.load('Object_Sprites\\quiver.png').convert_alpha()
quiver_img = pygame.transform.rotate(quiver_img, 45.0)

plate_armor_img = pygame.image.load('Object_Sprites\\plate_armor.png').convert_alpha()
leather_armor_img = pygame.image.load('Object_Sprites\\leather_armor.png').convert_alpha()

health_potion_img = pygame.image.load('Object_Sprites\\health_potion.png').convert_alpha()
poison_potion_img = pygame.image.load('Object_Sprites\\poison_potion.png').convert_alpha()
unknown_potion_img = pygame.image.load('Object_Sprites\\unknown_potion.png').convert_alpha()

helm_img = pygame.image.load('Object_Sprites\\Helm_small.png').convert()
helm_img.set_colorkey((0,0,0))

arrow_img = pygame.image.load('Object_Sprites\\crap_arrow.png').convert()
arrow_img = pygame.transform.rotate(arrow_img, 180.0)
arrow_img.set_colorkey((0,0,0))

inv_bg = pygame.image.load('Object_Sprites\\bg_parchment.png').convert()
inv_bg = pygame.transform.smoothscale(inv_bg, (screenWIDTH, screenHEIGHT))

but_bg = pygame.image.load('Object_Sprites\\But_bg.png').convert_alpha()

#importing background
dirt_map = pygame.image.load('Object_Sprites\\dirt_map.png').convert()
dirt_map.set_colorkey((255,255,255))
background = pygame.image.load('Object_Sprites\\grass_map.png').convert()

#importing level_edges
pine_ns = pygame.image.load('Object_Sprites\\2pine_NS.png').convert()
pine_ns.set_colorkey((0,0,0))
tree_pack_ew = pygame.image.load('Object_Sprites\\forest_EW_pack.png').convert_alpha()

#importing forest assets
forest_sample = pygame.image.load('Object_Sprites\\forest_sample.png').convert()
forest_sample.set_colorkey((0,0,0))

rock1 = pygame.image.load('Object_Sprites\\forest\\rock1.png').convert_alpha()
rock2 = pygame.image.load('Object_Sprites\\forest\\rock2.png').convert()
rock2.set_colorkey((0,0,0))
tree_stump = pygame.image.load('Object_Sprites\\forest\\tree_stump.png').convert()
tree_stump.set_colorkey((0,0,0))
mushrooms = pygame.image.load('Object_Sprites\\forest\\mushroom1.png').convert_alpha()
log1 = pygame.image.load('Object_Sprites\\forest\\log1.png').convert_alpha()
log2 = pygame.image.load('Object_Sprites\\forest\\log2.png').convert_alpha()
log3 = pygame.transform.rotate(log1, -90)
log4 = pygame.transform.rotate(log2, -90)

trees = []
for x in range(1,5):
    image = pygame.image.load('Object_Sprites\\forest\\tree{}.png'.format(x)).convert_alpha()
    image = pygame.transform.scale(image,(image.get_rect().width*5,image.get_rect().height*5))
    image = pygame.transform.scale(image,(image.get_rect().width/3,image.get_rect().height/3))
    trees.append(image)
    
obs_list = [rock1, rock2, rock1, tree_stump, mushrooms, log1, log2, log3, log4]+trees*4

#importing dirt assets
rocks = []
for x in range(1,7):
    image = pygame.image.load('Object_Sprites\\dirt\\rock{}.png'.format(x)).convert_alpha()
    image = pygame.transform.scale(image,(image.get_rect().width*5,image.get_rect().height*5))
    image = pygame.transform.scale(image,(image.get_rect().width/3,image.get_rect().height/3))
    rocks.append(image)

crystals = []
for x in range(1,3):
    image = pygame.image.load('Object_Sprites\\dirt\\crystal{}.png'.format(x)).convert_alpha()
    image = pygame.transform.scale(image,(image.get_rect().width*5,image.get_rect().height*5))
    image = pygame.transform.scale(image,(image.get_rect().width/3,image.get_rect().height/3))
    crystals.append(image)
    
mound = pygame.image.load('Object_Sprites\\dirt\\mound1.png').convert_alpha()
bone1 = pygame.image.load('Object_Sprites\\dirt\\bone1.png').convert_alpha()
bone2 = pygame.image.load('Object_Sprites\\dirt\\bone2.png').convert_alpha()

dirt_list = rocks+[mound]*10+[bone1,bone2]+crystals

'''impoting HUD'''
hp_hud = pygame.image.load('HUD\\hp_hud.png').convert_alpha()
hp_partial_hud = pygame.image.load('HUD\\hp_partial_hud.png').convert_alpha()
bar_hud = pygame.image.load('HUD\\bar_hud.png').convert_alpha()


#importing building
house1_img =  pygame.image.load('Object_Sprites\\House1.png').convert()#Object_Sprites\\House1.png
house1_img.set_colorkey((0,0,0))

'''importing icons'''
skill_icons = spritesheet('Icons\\skills_icons.png')
weapon_icons = spritesheet('Icons\\weapon_icons.png')

#create sprite groups
player_list = pygame.sprite.Group()
char_list = pygame.sprite.Group()
ennemi_list = pygame.sprite.Group()
item_list = pygame.sprite.Group()
building_list = pygame.sprite.Group()
projectile_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
deleted_list = pygame.sprite.Group()
dead_sprites_list = pygame.sprite.Group()
message_list = pygame.sprite.Group()
to_blit_list = pygame.sprite.Group()


sprite_group_list = []
sprite_group_list.extend([player_list,char_list, projectile_list, dead_sprites_list, ennemi_list, item_list, building_list, all_sprites_list, to_blit_list, deleted_list])

buttons_list = []

#fix_mouse pos
fix_mouse = (200,200)

#char variables
move_speed = 0

#collision lists
collide_building = []
collide_chest = []

'''importing lighting effect'''
surf_falloff = pygame.image.load('sfx\\light_falloff100.png').convert()

#timers and time info:
FPS = 60
set_ennemies_dest = USEREVENT + 1
set_ennemies_move = USEREVENT + 2
