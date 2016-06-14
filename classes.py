# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 10:35:10 2016

@author: Julien
"""
import pygame, sys, random
import functions as fn
import variables as var
from pygame.locals import *
import itertools
import numpy as np

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
        #var.screen.blit(self.sheet, (0,0), rect)
#        if colorkey is not None:
#            if colorkey is -1:
#                colorkey = image.get_at((0,0))
#            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
#    def load_strip(self, rect, image_count, colorkey = None):
#        "Loads a strip of images and returns them as a list"
#        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
#                for x in range(image_count)]
#        return self.images_at(tups, colorkey)
        
    def load_strip(self,spacing, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
#        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
#                for x in range(image_count)]:
        tups = []          
        for x in range(image_count):
            if x != 0:
                tups += [(rect[0]+(rect[2]+spacing)*x, rect[1], rect[2], rect[3])]
            else:
                tups += [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])]
        return self.images_at(tups, colorkey)  
        
class SpriteStripAnim(object):
    """sprite strip animator
    
    This class provides an iterator (iter() and next() methods), and a
    __add__() method for joining strips which comes in handy when a
    strip wraps to the next row.
    """
    def __init__(self, filename, spacing, rect, count, colorkey=None, loop=False, frames=1):
        """construct a SpriteStripAnim
        
        filename, rect, count, and colorkey are the same arguments used
        by spritesheet.load_strip.
        
        loop is a boolean that, when True, causes the next() method to
        loop. If False, the terminal case raises StopIteration.
        
        frames is the number of ticks to return the same image before
        the iterator advances to the next image.
        """
        #self.filename = filename
        #ss = spritesheet(filename)
        ss = filename
        self.images = ss.load_strip(spacing, rect, count, colorkey)
        self.i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames
    def iter(self):
        self.i = 0
        self.f = self.frames
        return self
    def next(self):
        if self.i >= len(self.images):
            if not self.loop:
                raise StopIteration
            else:
                self.i = 0
        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image
    def __add__(self, ss):
        self.images.extend(ss.images)
        return self
        
class Level(object):
    def __init__(self, lvl_num):
        var.current_level = self
        var.level_list.append(self)

        self.lvl_num = lvl_num
        self.run = False
        #create sprite groups
        self.player_list = pygame.sprite.Group()
        self.char_list = pygame.sprite.Group()
        self.ennemi_list = pygame.sprite.Group()
        self.item_list = pygame.sprite.Group()
        self.building_list = pygame.sprite.Group()
        self.projectile_list = pygame.sprite.Group()
        self.projectile_ennemy_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.deleted_list = pygame.sprite.Group()
        self.dead_sprites_list = pygame.sprite.Group()
        self.message_list = pygame.sprite.Group()
        self.to_blit_list = pygame.sprite.Group()
        
        self.sprite_group_list = []
        self.sprite_group_list.extend([self.player_list,self.char_list, self.projectile_list, self.dead_sprites_list, self.ennemi_list, self.item_list,self.building_list, self.all_sprites_list, self.to_blit_list, self.deleted_list])

    def go_to(self,new_lvl, pair):
        '''change level'''
        
        new_level = var.level_list[new_lvl-1]
        paired_portal_list = [y for y in [x for x in new_level.all_sprites_list if isinstance (x,Level_Change)] if y.pair == pair]
        
        if len(paired_portal_list) > 0:
            player = [x for x in self.player_list][0]
            self.run = False
            player.level = new_level
            new_level.run = True
            var.current_level = new_level
            
            dest_port = random.choice(paired_portal_list) #select a random destination amongst the paired portals
        
            refx = dest_port.rect.bottomright[0]-var.screenWIDTH/2
            refy = dest_port.rect.bottomright[1]+50-var.screenHEIGHT/2
            for sprite in new_level.all_sprites_list:
                sprite.rect = sprite.rect.move(-refx,-refy)
                
            new_level.scroll_map.rect =  new_level.scroll_map.rect.move(-refx,-refy) 
            player.rect.center = (var.screenWIDTH/2,var.screenHEIGHT/2)
            player.dest = player.rect.topleft
            
            
    def execute(self):
            var.current_level = self
            [x for x in self.player_list][0].level = self
            
    #random obstacles
    def add_obstacles(self,int,obs_list):
        count = 0
        while count < 75:
            choice = random.choice(obs_list)
            choice = choice if random.randint(0,1) == 1 else pygame.transform.flip(choice, True, False)
            w = Building('obstacles',0,choice,random.randint(25,1800),random.randint(75,1800),1000)
            old_rect = w.rect
            w.rect = w.rect.inflate(150,150)
            test = pygame.sprite.spritecollideany(w, self.all_sprites_list, collided = None)
            if test is None:
                w.rect = old_rect
                self.building_list.add(w)
                self.all_sprites_list.add(w)
                count += 1
                
    #Random ennemies
    def add_ennemies(self,int,list):
        count = 0           
        while count < 10: #number of wanted enemies
            o = random.choice(list)(random.randint(450,1500),random.randint(450,1000))
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
    def add_chests(self,int,chest,obj):
        count = 0
        while count < int:
            #obj = [wp.Arrow(random.randint(2,5)),wp.Sword(),wp.Bow(), ar.Helm()]
            collides = False
            chest_contents = []
            for n in range(0,random.randint(1,3)):
                chest_contents.append(random.choice(obj))
            pos = Rect(random.randint(50,var.background.get_rect()[2]),random.randint(80,var.background.get_rect()[3]),var.chest_img.get_rect().width,var.chest_img.get_rect().height)
            w = chest(0,0, chest_contents)
            w.rect = pos
        
            for c in self.all_sprites_list:
                if isinstance(c,chest) and w.rect.colliderect((c.rect.inflate(750,750))) == True:
                    collides = True
                    break
            test = pygame.sprite.spritecollideany(w, self.all_sprites_list, collided = None)
            if test is None and collides == False:
                self.building_list.add(w)
                self.all_sprites_list.add(w)
                for item in w.inventory.contents:
                    self.all_sprites_list.add(item)
                count +=1        
        
class Lifebar(object):
    def __init__(self,character):
        self.value = character.hp*10 if character.hp >= 0 else 0
        self.rect = Rect(10,var.screenHEIGHT-30,self.value,10)
        pygame.draw.rect(var.screen, (245,0,0) , self.rect)
    
class MySprite(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
 
        # Call the parent class (Sprite) constructor
        super(MySprite, self).__init__()
        self.image = image
        self.rect = self.image.get_rect().move(x, y) #initial placement
        self.top_cp = (self.rect[0]+self.rect[2]/2,self.rect[1])
        self.bot_cp = (self.top_cp[0],self.rect[1]+self.rect[3])
        self.left_cp = (self.rect[0],self.rect[1]+self.rect[3]/2)
        self.right_cp = (self.left_cp[0]+self.rect[2],self.left_cp[1])
        self.center = self.rect.center
        self.pos = self.rect.topleft
        self.blit_order = 1
        self.level =  var.current_level #Level(1)#level to which sprite belongs
        
    def pop_around(self,item,xzone,yzone):
        collides = True
        while collides == True:
            item.rect = Rect((random.randint(self.rect.x-xzone,self.rect.x+self.rect.width+xzone),random.randint(self.rect.y-yzone,self.rect.y+self.rect.height+yzone)),(item.rect.width,item.rect.height))
            for c in self.level.all_sprites_list:
                if c.rect.inflate(-5,-5).collidepoint(item.rect.center) == False and self.rect.inflate(xzone,yzone).contains(item.rect) == True:
                    collides = False
                    break
        return item.rect
    
        
    def highlight(self):
#        s = pygame.Surface((self.rect[2]*2,self.rect[3]*2))
#        s.fill((0,0,0))
##        s = s.convert_alpha()
##        s.set_alpha(100)
        pygame.draw.circle(var.screen, (255,0,0,80), self.rect.center, 20, 0)
        #var.screen.blit(s, (self.rect[0]-self.rect[2]/2,self.rect[1]-self.rect[3]/2))
        
    def delete(self):
        for group in self.level.sprite_group_list: #removes sprites from all groups
            if self in group:
                    group.remove(self)
                    print 'sprite deleted'
                    print self.level.item_list
        self.level.deleted_list.add(self) #adds the sprite to deleted list
        
        
class Character(MySprite):
    def __init__(self, hp, walk_images, attack_images, speed, x, y, CC, CT):
        self.walk_images = walk_images
        self.attack_images = attack_images
        self.image_list = self.attack_images[0]
        self.image = self.image_list[0]
        self.dead_image = var.dead_ennemi if random.randint(0,1) == 0 else pygame.transform.flip(var.dead_ennemi, True, False)
        # Call the parent class (Sprite) constructor
        super(Character, self).__init__(self.image,x,y)
        self.speed = int(speed)
        self.hp_max = hp
        self.hp = hp
        self.dest = (self.rect[0],self.rect[1])
        self.move_speed = self.speed
        self.inventory = Inventory()
        self.equipement = Inventory()
        self.CC = CC
        self.CT = CT
        self.attack_time = pygame.time.Clock()
        self.attack_time_left = 0        
        self.attack_speed = 750
        self.E = 35
        self.F = 30
        '''anim timer'''
        self.anim_time = pygame.time.Clock()
        self.anim_time_left = 0        
        self.anim_speed = 100
        self.anim_counter = 0
        self.orientation = 0
        self.has_attack = False
        self.anim_shot = False
        
        '''setting dest timer'''
        self.dest_time = pygame.time.Clock()
        self.dest_time_left = 0        
        self.dest_speed = 2000
        
        '''Mvt timer'''
        self.mvt_time = pygame.time.Clock()
        self.mvt_time_left = 0        
        self.mvt_speed = int(1000/(var.FPS*0.7))
        
        self.is_moving = False
        
        '''inventory opening attributes'''
        self.do_once = True
        self.buttons_list = []
        self.selected_button = 0
        self.selected = False
        self.start_pos = (0,0)
        self.inventory_opened = False 
        self.m_down = False
        self.m_up = True
        
        self.inv_time = pygame.time.Clock()
        self.inv_time_left = 0        
        self.inv_delay = 400
        
    def merge_ammo(self):
        self.inventory.combine_ammo() #merges all the ammo in the inventory only
        '''merges the ammo from inv with equipped ammo'''
        inv_projs = [x for x in self.inventory.contents if isinstance (x,Projectile)]
        equiped = [y for y in self.equipement.contents if isinstance (y,Projectile)]
        if len(equiped) > 0:
            equiped = equiped[0]
            for proj in inv_projs:
                if type(equiped) == type(proj):
                    equiped.ammo += proj.ammo
                    self.inventory.contents.remove(proj)
#                    equiped.name = '{} {}'.format(equiped.ammo,equiped.raw_name)
                    
                    
                    
    def anim_move(self):
        #updates anim timer
        self.anim_time.tick()
        self.anim_time_left += self.anim_time.get_time()
        #checks which anim to display based on the direction and if sprite is moving and alive
        if self.anim_time_left >= self.anim_speed and self.is_alive() == True: #checks time to animate
            if self.orientation >= 140 and self.orientation <= 220: #checks orientation
                if self.anim_counter >= 4:
                    self.anim_counter = 0
                self.image = self.image_list[self.anim_counter]
                if self.pos == self.rect.topleft:# and self.has_attack == False:
                    self.image = self.image_list[0]
            elif self.orientation >= 220 and self.orientation <= 320: #checks orientation
                if self.anim_counter >= 4:
                    self.anim_counter = 0
                self.image =self.image_list[self.anim_counter+4]  
                if self.pos == self.rect.topleft:# and self.has_attack == False:
                    self.image = self.image_list[4]
            elif self.orientation >= 320 or self.orientation <= 40: #checks orientation
                if self.anim_counter >= 4:
                    self.anim_counter = 0
                self.image = self.image_list[self.anim_counter+8]
                if self.pos == self.rect.topleft:# and self.has_attack == False:
                    self.image = self.image_list[8]
            elif self.orientation >= 40 and self.orientation <= 140: #checks orientation
                if self.anim_counter >= 4:
                    self.anim_counter = 0
                self.image = self.image_list[self.anim_counter+12]
                if self.pos == self.rect.topleft:# and self.has_attack == False:
                    self.image = self.image_list[12]
            self.anim_time_left = 0
            self.anim_counter += 1
            
            
    def get_dest(self):
        self.dest = pygame.mouse.get_pos() #mouse position tracker
        new_x = self.dest[0]-self.image.get_rect()[2] #adds offset to center player
        new_y = self.dest[1]-self.image.get_rect()[3] #adds offset to center player
        self.dest = (new_x,new_y)
        
        xp = self.rect.x
        yp = self.rect.y
        #print xp,yp
        xm = self.dest[0] 
        ym = self.dest[1]
        
        var.dx = xm-xp
        var.dy= ym-yp 
        
        
    def get_offset(self):
        speed = self.speed #player's speed
        
        xp = self.rect.x#(var.screenWIDTH/2)-(self.image.get_rect()[2]/2.)
        yp = self.rect.y#(var.screenHEIGHT/2)-(self.image.get_rect()[3]/2.)
        #print xp,yp
        xm = self.dest[0]
        ym = self.dest[1]
        
        dx = float(xm-xp)
        dy = float(ym-yp) 
        
        #dist = (var.dx**2+var.dy**2)**0.5 #get lenght to travel
        
        #calculates angle and sets quadrant
        if dx == 0 or dy == 0:
            angle_rad = 0#np.pi/2
            if dx == 0 and ym > yp:
                xoffset = 0
                yoffset = -speed
                self.orientation = 180
            elif dx == 0 and ym < yp:
                xoffset = 0
                yoffset = speed
                self.orientation = 0
            elif dy == 0 and xm > xp:
                xoffset = 0
                yoffset = -speed
                self.orientation = 90
            elif dy == 0 and xm < xp:
                xoffset = 0
                yoffset = speed
                self.orientation = 270
            else:
                xoffset, yoffset = 0,0
                self.orientation = 180
        elif xm > xp and ym > yp:
            angle_rad = np.arctan((abs(dy)/abs(dx)))
            xoffset = -np.cos(angle_rad)*speed
            yoffset = -np.sin(angle_rad)*speed
            self.orientation = angle_rad*(180.0/np.pi)+90
        elif xm < xp and ym > yp:
            angle_rad = np.arctan((abs(dx)/abs(dy)))
            xoffset =  np.sin(angle_rad)*speed
            yoffset = -np.cos(angle_rad)*speed
            self.orientation = angle_rad*(180.0/np.pi)+180
        elif xm < xp and ym < yp:
            angle_rad = np.arctan((abs(dy)/abs(dx)))
            xoffset = np.cos(angle_rad)*speed
            yoffset = np.sin(angle_rad)*speed
            self.orientation = angle_rad*(180.0/np.pi)+270
        else:# xm > xp and ym < yp:
            angle_rad = np.arctan((abs(dx)/abs(dy)))
            xoffset = -np.sin(angle_rad)*speed
            yoffset =  np.cos(angle_rad)*speed
            self.orientation = angle_rad*(180.0/np.pi)
        
        var.xoffset = int(xoffset)
        var.yoffset = int(yoffset)
        
        if var.dx <= 3 and var.dx >= -3:
            var.dx = 0
            var.xoffset = 0
        if var.dy <= 3 and var.dy >= -3:
            var.dy = 0
            var.yoffset = 0
        if var.has_shot == True:
            var.dy, var.dx = 0,0
            var.yoffset, var.xoffset = 0,0
            var.has_shot = False
            self.anim_shot = True
                        
        
    def open_inventory(self):
        while self.inventory_opened == True:
            var.screen.blit(self.inventory.inv_bg, self.inventory.inv_bg.get_rect())
            if self.do_once == True:
                self.merge_ammo()
                self.inventory.create(self,10,10,0,50)
                self.equipement.create(self,var.screenWIDTH/2+50,10,0,50)
                self.dropbut = Button('discard', 50,450,50,20)            
                self.do_once = False
                self.inv_time.tick() #needs to tick it here to reset the tick value or it has kept adding up since last inventory 
                self.inv_time_left = 0
            for b in self.buttons_list:
                b.display()
            self.dropbut.display()
            
            
            for event in pygame.event.get(): #setting up quit
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    self.m_down = True
                    self.m_up = False
                    #print 'mouse down'
                    
                if event.type == MOUSEBUTTONUP:
                    self.m_up = True
                    self.m_down = False
                    #print 'mouse up'
            
            if self.selected == False and self.m_down == True:
                for b in self.buttons_list:
                    if b.rect.collidepoint(pygame.mouse.get_pos()):
                        self.selected = True
                        self.selected_button = self.buttons_list.index(b)
                        self.start_pos = pygame.mouse.get_pos()
                        
            x,y = pygame.mouse.get_pos()            
            if self.selected == True and self.m_down == True:
                width = self.buttons_list[self.selected_button].rect.width
                height = self.buttons_list[self.selected_button].rect.height
                self.buttons_list[self.selected_button].rect = Rect(x-width/2,y-height/2,self.buttons_list[self.selected_button].rect[2],self.buttons_list[self.selected_button].rect[3])
    
            if self.m_up == True:
                if self.selected == True:
                    if self.start_pos[0]<var.screenWIDTH/2:
                        if isinstance(self.inventory.contents[self.selected_button], Potion):
                            self.inventory.contents[self.selected_button].drink(self)
                            print 'attempts potion drinking from inv'
                    if self.buttons_list[self.selected_button].rect.colliderect(self.dropbut.rect) and self.start_pos[0]<var.screenWIDTH/2: #removes item from inv
                        print 'removing inv item'
                        self.inventory.contents[self.selected_button].rect[0] = self.rect.move(random.randint(0,20)+5,0)[0]
                        self.inventory.contents[self.selected_button].rect[1] = self.rect.move(0,random.randint(0,20)+10)[1]
                        self.level.deleted_list.remove(self.buttons_list[self.selected_button]) #put's sprite back in game
                        self.level.item_list.add(self.inventory.contents[self.selected_button]) #add's sprite back to item list for it to behave as item in game
                        self.inventory.contents.pop(self.selected_button) #removes item in player's iventory located at the index specified by the position of the button corresponding to this item in the button list 
                        self.buttons_list.pop(self.selected_button)
                    elif self.buttons_list[self.selected_button].rect.colliderect(self.dropbut.rect) and self.start_pos[0]>var.screenWIDTH/2:  #remove item from equipemnt
                        print 'removing eq item'
                        self.level.deleted_list.remove(self.buttons_list[self.selected_button]) #put's sprite back in game
                        self.level.item_list.add(self.equipement.contents[self.selected_button-len(self.buttons_list)]) #add's sprite back to item list for it to behave as item in game
                        self.equipement.contents[self.selected_button-len(self.buttons_list)].rect[0] = self.rect.move(random.randint(0,20)+5,0)[0]
                        self.equipement.contents[self.selected_button-len(self.buttons_list)].rect[1] = self.rect.move(0,random.randint(0,20)+10)[1]
                        self.equipement.contents.pop(self.selected_button-len(self.buttons_list)) #removes item in player's iventory located at the index specified by the position of the button corresponding to this item in the button list 
                        self.buttons_list.pop(self.selected_button)
                    elif  self.start_pos[0]>var.screenWIDTH/2 and self.buttons_list[self.selected_button].rect[0]<var.screenWIDTH/2 and len(self.inventory.contents) < 32: #moving item from equipement to inv
                        print 'moving from eq to inv'
                        self.inventory.add(self.equipement.contents[self.selected_button-len(self.buttons_list)]) #add's item to inv
                        self.equipement.contents.pop(self.selected_button-len(self.buttons_list)) #removes item in player's equipment located at the index specified by the position of the button corresponding to this item in the button list
                        self.buttons_list.pop(self.selected_button) #remove's the item from it's button list position
                    elif  self.start_pos[0]<var.screenWIDTH/2 and self.buttons_list[self.selected_button].rect[0]>var.screenWIDTH/2: #moving item from inv to eq
                        print 'moving from inv to eq'                   
                        if isinstance(self.inventory.contents[self.selected_button],Armor): #checks if item is an armor
                            x = [item for item in self.equipement.contents if isinstance(item,Armor) == True] #creates a list of all armor items already in  the equipment
                            already_has = False # assumes the player doesn't have any of that armor category
                            for armor in x: #checks if the item to be added is already contained in the equipment
                                if isinstance(armor,Helm)==True and isinstance(self.inventory.contents[self.selected_button],Helm) == True:
                                    print 'already has helm'
                                    already_has = True
                                    break
                                elif isinstance(armor,Torso_armor)==True and isinstance(self.inventory.contents[self.selected_button],Torso_armor) == True:
                                    print 'already has torso'
                                    already_has = True
                                    break
                            if len(x) != 2 and already_has == False: # if the total number of armor items in the equipment is less than 2 and the player doesn't have one of the type it is added to the equ and removed from the inv
                                print 'armor piece added to eq'
                                self.equipement.contents.append(self.inventory.contents[self.selected_button]) #add's item to inv
                                self.inventory.contents.pop(self.selected_button) #removes item in player's equipment located at the index specified by the position of the button corresponding to this item in the button list
                                self.buttons_list.pop(self.selected_button) #remove's the item from it's button list position
                                    
                        elif isinstance(self.inventory.contents[self.selected_button],Weapon): #checks if item is an armor
                            x = [item for item in self.equipement.contents if isinstance(item,Weapon) == True] #creates a list of all weapon items already in  the equipment
                            already_has = False
                            for weapon in x:
                                if weapon.wield == 'two_handed':
                                    already_has = True # doesn't actually have it but can't have more than one 2 handed weapon
                                    print 'Already has a two-handed weapon'
                                if self.inventory.contents[self.selected_button].wield == 'two_handed' and weapon.wield == 'one_handed':
                                    already_has = True # doesn't actually have it but can't have more than one 2 handed weapon
                                    print 'Can t have both a two and one handed weapon'
                            if len(x) != 2 and already_has == False:
                                print 'weapon  added to eq'
                                self.equipement.contents.append(self.inventory.contents[self.selected_button]) #add's item to eq
                                self.inventory.contents.pop(self.selected_button) #removes item in player's equipment located at the index specified by the position of the button corresponding to this item in the button list
                                self.buttons_list.pop(self.selected_button) #remove's the item from it's button list position
                            elif already_has == True:
                                '''send item in eq to inv'''
                                if self.inventory.contents[self.selected_button].wield == 'two_handed':
                                    for item in x: #removes all weapons in eq
                                        self.inventory.contents.append(item) #add's item to inv
                                        self.equipement.contents.remove(item) #removes item in player's equipment located at the index specified by the position of the button corresponding to this item in the button list
                                else: #i.e. one handed
                                    self.inventory.contents.append(x[0]) #add's item to inv
                                    self.equipement.contents.remove(x[0]) #removes item in player's equipment located at the index specified by the position of the button corresponding to this item in the button list
                                '''adds item to eq'''
                                self.equipement.contents.append(self.inventory.contents[self.selected_button]) #add's item to eq
                                self.inventory.contents.pop(self.selected_button) #removes item in player's inv located at the index specified by the position of the button corresponding to this item in the button list
                                self.buttons_list.pop(self.selected_button) #remove's the item from it's button list position
                                
                        elif isinstance(self.inventory.contents[self.selected_button],Projectile): #checks if item is a projectile
                            x = [item for item in self.equipement.contents if isinstance(item,Projectile) == True] #creates a list of all projectile items already in  the equipment
                            if len(x) == 0:
                                print 'projectile added to eq'
                                self.equipement.contents.append(self.inventory.contents[self.selected_button]) #add's item to inv
                                self.inventory.contents.pop(self.selected_button) #removes item in player's equipment located at the index specified by the position of the button corresponding to this item in the button list
                                self.buttons_list.pop(self.selected_button) #remove's the item from it's button list position
                    
                    self.buttons_list = [] #clears buttonlist
                    self.inventory.create(self,10,10,0,50) #resets buttons and button list
                    self.equipement.create(self,var.screenWIDTH/2+50,10,0,50)
                    
                self.selected = False
            for msg in self.level.message_list:
                msg.show()
            pygame.display.update()
                
                
            #update inv shutdown delay:
            self.inv_time.tick()
            self.inv_time_left += self.inv_time.get_time()
            if pygame.key.get_pressed()[pygame.K_i] and self.inv_time_left > self.inv_delay:
                self.inv_time_left = 0
                self.buttons_list = [] #clear's buttons list
                self.do_once = True # to insure buttons are populated again at next inventory opening
                self.inventory_opened = False
        
        
    def offset(self,):
        if (var.dx  == 0 and var.dy == 0) == False:
            self.rect = self.rect.move(var.xoffset,var.yoffset)

    def is_alive(self):
        if self.hp > 0:
            return True
        else:
            self.kill()
            self.level.dead_sprites_list.add(self) #adds the character to the deleted sprite list
            self.level.all_sprites_list.add(self)
            self.image = self.dead_image
            return False
    
    def attack(self, Character):
        self.attack_time.tick()
        self.attack_time_left += self.attack_time.get_time()
        if self.attack_time_left >= self.attack_speed: # needs to be added as a variable
            self.has_attack = False #to prevent endless animation
            if Character.is_alive() == True and self.is_alive() == True and Character.rect.inflate(5,5).colliderect(self.rect):
                self.has_attack = True
                test = random.randint(1,100) <= self.CC
                if test == True:
                    dmg = sum([x.random_dmg() for x in self.equipement.contents if isinstance(x, Weapon) == True]) #sum of the values of all weapons in equipement
                    arm = sum([x.arm for x in Character.equipement.contents if isinstance(x, Armor) == True]) #sum of the values of all weapons in equipement
                    if (dmg+self.F/10)-(arm+Character.E/10) < 0:
                        dmg = 0
                    else:
                        dmg = (dmg+self.F/10)-(arm+Character.E/10)
                    Character.hp -=  dmg
                    print 'mob deals {} dmg'.format(dmg)
                    self.attack_time_left = 0
            elif Character.is_alive() == True and self.is_alive() == True and len([y for y in [x for x in self.equipement.contents if isinstance (x,Projectile)] if y.ammo > 0]) > 0 and len([x for x in [y for y in self.equipement.contents if isinstance (y,Weapon)] if x.type == 'CT']) > 0: #checks clicks ennemi and has ammo 
                range_ = [x for x in [y for y in self.equipement.contents if isinstance (y,Weapon)] if x.type == 'CT'][0].range
                #print fn.in_sight(self,Character, range_, self.level.building_list)
                if self.rect.inflate(range_,range_).colliderect(Character.rect) \
                and self.rect.inflate(300,300).colliderect(Character.rect) == False \
                and fn.in_sight(self,Character, range_, self.level.building_list):
                    print 'shoot'
                    '''creates an instance by getting the type of the proj in eq'''
                    proj_used = type([y for y in [x for x in self.equipement.contents if isinstance (x,Projectile)] if y.ammo > 0][0])(0)
                    for proj in [x for x in self.equipement.contents if isinstance (x,Projectile)]:
                        if proj.ammo > 0:
                            proj.ammo -= 1
                            break
                    wep_used = [x for x in [y for y in self.equipement.contents if isinstance (y,Weapon)] if x.type == 'CT'][0]
                    proj_used.dmg += wep_used.dmg
                    proj_used.fire(self,(var.screenWIDTH/2,var.screenHEIGHT/2),self.level.projectile_ennemy_list) #in this function the pojectile level attribute needs to be already set
                    self.attack_time_left = 0

           
    def set_rand_dest(self):
        self.dest_rect = self.rect.inflate(200,200)
        self.dest = (random.randint(self.dest_rect[0],self.dest_rect[0]+self.dest_rect[2]),random.randint(self.dest_rect[1],self.dest_rect[1]+self.dest_rect[3]))
        
    def set_charge_dest(self,charge_target):
        '''Charge destination randomly changed to allow the seek behaviour
        due to the move_collision function'''
        self.dest = charge_target.rect.x+random.randint(-10,10),charge_target.rect.y+random.randint(-10,10)
        
    def behaviour(self,Character):
        self.dest_time.tick()
        self.dest_time_left += self.dest_time.get_time()
        if self.dest_time_left >= self.dest_speed  and self.has_attack == False: # checks if time to set new dest
            self.dest_time_left = 0 #resets timer
            if self.rect.inflate(250,250).colliderect(Character.rect) == True:
                if self.speed < 2:
                    self.speed *= 2
                self.set_charge_dest(Character)
            elif self.rect.inflate(500,500).colliderect(Character.rect) == True:
                if self.speed > int(48.0/(var.FPS*0.7)):
                    self.speed = int(48.0/(var.FPS*0.7))
                my_list = [self.set_charge_dest(Character),self.set_charge_dest(Character),self.set_charge_dest(Character),self.set_rand_dest()]
                random.choice(my_list)
            else:
                if self.speed > int(48.0/(var.FPS*0.7)):
                    self.speed = int(48.0/(var.FPS*0.7))
                self.set_rand_dest()
                
           
    def move_collision(self,EW,SN):
        test_rect = Rect(self.rect.midleft,(self.rect.width,self.rect.height/2))
        for obstacle in itertools.chain.from_iterable([self.level.building_list,self.level.player_list]):
            if test_rect.colliderect(obstacle.rect.inflate(-obstacle.rect.width/10,-obstacle.rect.height/10)) == True:#len([x for x in char_col_points if obstacle.rect.collidepoint(x)]) >= 1:
                if EW == True:
                    if self.dest[1] > self.rect.y:
                        mvt = self.speed
                    else:
                        mvt = -self.speed
                    self.rect = self.rect.move(-self.move_speed,mvt)
                elif SN == True:
                    if self.dest[0] > self.rect.x:
                        mvt = self.speed
                    else:
                        mvt = -self.speed
                    self.rect = self.rect.move(mvt,-self.move_speed)
                break

    def move_NS(self):
        self.rect = self.rect.move(0, self.move_speed)
        # Check for Collisions
        self.move_collision(False,True)
        
    def move_EW(self):
        self.rect = self.rect.move(self.move_speed,0)
        # Check for Collisions
        self.move_collision(True,False)
    
    def move(self):#,mouse_pos, screen, background
        #updates mvt timer
        self.mvt_time.tick()
        self.mvt_time_left += self.mvt_time.get_time()
        if  self.mvt_time_left >= self.mvt_speed:# checks time to animate
            if self.pos != self.dest: # cheks pos  animate
                self.is_moving = True
                self.mvt_time_left = 0
                if self.dest[0] > self.rect[0]: #move E
                    self.move_speed = self.speed
                    self.move_EW() #moves player
                    self.orientation = 90
                if self.dest[0] < self.rect[0]: #move W
                    self.move_speed = -self.speed
                    self.move_EW() #moves player
                    self.orientation = 270
                if self.dest[1] < self.rect[1]:
                    self.move_speed = -self.speed
                    self.move_NS() #moves player
                    self.orientation = 0
                if self.dest[1] > self.rect[1]:
                    self.move_speed = self.speed
                    self.move_NS() #moves player
                    self.orientation = 180
                if self.rect.collidepoint(self.dest): #check position reset
                    self.pos = self.rect.topleft
            else:
                self.anim_time_left = 0
                self.is_moving = False


    def loot(self,Character):
        if self.rect.collidepoint(pygame.mouse.get_pos()) == True and Character.rect.colliderect(self.rect.inflate(5,5)) == True: 
            has_looted = False
            for inv in [self.inventory.contents,self.equipement.contents]:
                if len(inv) >= 1:
                    has_looted = True
                    for item in inv:
                        self.pop_around(item, 50,50)
                        self.level.item_list.add(item) #add's sprite back to item list for it to behave as item in game
                        inv.remove(item) #removes item from chest
            if has_looted == False:
                w = 150
                h = 30
                msg = Message('Nothing to loot !!',500, 0,0,w,h)
                msg.image = pygame.transform.scale(msg.image, (w, h))
                msg.rect.center = (var.screenWIDTH/2,25)
                self.level.message_list.add(msg)


class Button(pygame.sprite.Sprite):
    def __init__(self, text, x,y,w,h ):
        super(Button, self).__init__()
        self.text = text
        self.image = var.but_bg
        self.text_pos = ((x+w/2),(y+h/2))
        self.rect2 = 0
        self.color = (0,200,0)
        
        #self.surface = pygame.draw.rect(var.screen, self.color , self.rect)
        
        self.smallText = pygame.font.Font("freesansbold.ttf",12)
        self.textSurf = self.smallText.render(self.text, True, (0,0,0))
        self.rect2 = self.textSurf.get_rect()
        self.rect2.center = self.text_pos
        self.image = pygame.transform.scale(self.image, (int(self.rect2.width*1.5),int(self.rect2.height*3)))
        self.rect = Rect(x,y,self.image.get_rect().width,self.image.get_rect().height)

    def display(self):
        #self.surface = pygame.draw.rect(var.screen, self.color , self.rect)
        var.screen.blit(self.image,self.rect)
        var.screen.blit(self.textSurf, Rect(self.rect[0]+(self.rect.centerx-self.rect[0])*0.4,self.rect[1]+self.rect[3]/4,self.rect[2],self.rect[3])) #Rect(self.rect[0]+self.rect[2]/8,self.rect[1]+20,self.rect[2],self.rect[3])
        
class Message(Button):
    def __init__(self, text, display_time, x,y,w,h ):
        super(Message, self).__init__(text, x,y,w,h)
        self.display_time = pygame.time.Clock()
        self.display_time_to = display_time        
        
    def show(self):
        self.display_time.tick()
        self.display_time_to -= self.display_time.get_time()
        if (self.display_time_to <= 0) == False:
            self.display()
            
        
    
class Inventory(object):
    def __init__(self):
        self.contents = []
        self.inv_bg = var.inv_bg
        
    def combine_ammo(self):
        all_projectiles = [x for x in self.contents if isinstance (x,Projectile)]
        for item in all_projectiles:
            temp_projectiles = all_projectiles
            temp_projectiles.remove(item)
            other_projectiles = temp_projectiles
            print other_projectiles
            for other in other_projectiles:
                if type(item) == type(other):
                    item.ammo += other.ammo
                    self.contents.remove(other)
#                    item.name = '{} {}'.format(item.ammo,item.raw_name)
                   
    def add(self, item):
        if len(self.contents) < 32:
            self.contents.append(item)
            item.inv_pos = len(self.contents)
            #self.combine_ammo()
    
    def rem(self, item):
        try:
            self.contents.remove(item)
        except:
            print 'item not in inventory'
    

            
    def create(self,Character,x,y, dx, dy):
        xstart = x
        ystart = y
        for i in range(0,len(self.contents)):
            b = Button(self.contents[i].name,x,y,100,50)
            if i == 7:
                x = xstart+110
                y = ystart-50
            if i == 15:
                x = xstart+220
                y = ystart-50
            if i == 23:
                x = xstart+330
                y = ystart-50
            x += dx
            y += dy
            Character.buttons_list.append(b)
            
#class Equipment(object): #not working yet
#    def __init__(self):
#        self.contents = {
#                'Head':0,'Neck':0, 'Torso':0, 'Right hand':0, 'Left hand':0, 'Ring':0
#        }   
#        
#    def add(self, item): #to check
#        self.contents.append(item)
#        item.inv_pos = len(self.contents)
#    
#    def rem(self, item): #to ckech
#        try:
#            self.contents.remove(item)
#        except:
#            print 'item not in inventory'
#            
#    def create(self,Character,x,y, dx, dy):
#        for i in self.contents:
#            b = Button(i.name,x,y,80,30)
#            x += dx
#            y += dy
#            Character.buttons_list.append(b)

            
class Item(MySprite):
 
    def __init__(self, name, value, image, x, y):
        # Call the parent class (Sprite) constructor
        super(Item, self).__init__(image, x, y)
 
        self.name = name
        self.value = value 
        self.inv_pos = -1
        
    def offset(self):
            if (var.dx  == 0 and var.dy == 0) == False:
                self.rect = self.rect.move(var.xoffset,var.yoffset)
                
    def use(self,player): #needs to be ckecked when E key is down AKA object mode
        if self.rect.inflate(10,10).collidepoint(pygame.mouse.get_pos()) and player.rect.inflate(10,10).colliderect(self.rect) and pygame.key.get_pressed()[pygame.K_e]:
            player.inventory.add(self)
            print 'item added'
            self.delete() #sends to deleted_sprite_list
            
class No_item(object): #creates a blank item
    def __init__(self):
        self.name = 'none'
        
def d10(int):
    rng = range(0,int)
    total = 0
    for x in rng:
        total += random.randint(0,10)
    return total
  
class Weapon(Item):
    def __init__(self, name, value, image, x, y, dmg, dmg_modif):
        super(Weapon, self).__init__(name, value, image, x, y)
        self.dmg_modif = dmg_modif
        self.dmg = dmg
        
    def random_dmg(self):
        attack_dmg = self.dmg+d10(self.dmg_modif)
        return attack_dmg
        
class Armor(Item):
    def __init__(self, name, value, image, x, y, arm):
        super(Armor, self).__init__(name, value, image, x, y)
        self.arm = arm

class Helm(Armor):
    def __init__(self): #name, value, image, x, y, dmg
        self.name = 'Helm'
        self.value = 10
        self.arm = 2
        self.image = var.helm_img
        super(Helm, self).__init__(self.name, self.value, self.image, 200, 150, self.arm)

class Torso_armor(Armor):
    def __init__(self,name,value,image,arm): #name, value, image, x, y, dmg
        self.name = name
        self.value = value
        self.arm = arm
        super(Torso_armor, self).__init__(self.name, self.value, image, 200, 150, self.arm)

class Potion(Item):
    def __init__(self, value, regen):
        if regen == 0:
            regen = 1
        if random.randint(0,4) != 0:
            if 0 < regen <= 3:
                self.name = 'Weak Health Potion'
            elif 3 < regen <= 6:
                self.name = 'Health Potion'
            elif 6 < regen <= 10:
                self.name = 'Strong Health Potion'
            elif 10 < regen:
                self.name = 'Health Elixir'
            elif regen < 0:
                self.name = 'Poison'
        else:
            self.name = 'Unknown potion'
            
        if 'Health' in self.name:
            self.image = var.health_potion_img
        elif self.name == 'Poison':
            self.image = var.poison_potion_img
        else:
            self.image = var.unknown_potion_img
        
        super(Potion, self).__init__(self.name, value, self.image, 150, 225)
        self.regen = regen
        self.confirm = False
        self.timer = pygame.time.Clock()
        self.timer_left = 0        
        self.reset_time = 10000 #10 seconds
        
    def drink(self,Character):
        if Character.hp < Character.hp_max:
            self.timer.tick()
            self.timer_left += self.timer.get_time()
            print self.timer_left
            if self.timer_left >= self.reset_time: # check if confirm needs to be rest
                self.confirm = False
                print 'confirm reset'
                
            if self.confirm == False:
                w = 150
                h = 30
                msg = Message('Clic again to drink', 2000, 0,0,w,h)
                msg.image = pygame.transform.scale(msg.image, (w, h))
                msg.rect.center = (var.screenWIDTH/2,25)
                self.level.message_list.add(msg)
                self.confirm = True
                self.timer_left = 0
                
            elif self.confirm == True and self.timer_left > 100:
                Character.hp = min([Character.hp + self.regen,Character.hp_max])
                Character.inventory.contents.remove(self)
                self.kill()
                print 'potion restores hp to {}'.format(Character.hp)
            
        

class Building(Item):
    def __init__(self, name, value, image, x, y, hp):
        super(Building, self).__init__(name, value, image, x, y)
        self.hp = hp
        #self.image = image
        #self.rect = self.image.get_rect().move(x, y) #initial placement
        
class Projectile(Item):
    def __init__(self, name, value, image, x, y, speed, dmg, dmg_modif, ammo, range_):
        super(Projectile, self).__init__(name, value, image, x, y)
        self.dest = (self.rect[0],self.rect[1])
        self.speed = speed
        self.dmg_modif = dmg_modif
        self.dmg = dmg
        self.orientation = 0
        self.range = range_
        self.ammo = ammo
        
    @property
    def ammo(self):
        return self._ammo

    @ammo.setter
    def ammo(self, ammo):
        raw_name = ''.join([i for i in self.name if not i.isdigit()])
        self.name = str(ammo) + raw_name
        self._ammo = ammo

            
    def random_dmg(self):
        attack_dmg = self.dmg+d10(self.dmg_modif)
        return attack_dmg

    def fire(self,shooter, target_pos, dest_list):
        self.rect.center = shooter.rect.center#place's the projectile at shooter's position
        self.dest = target_pos#pygame.mouse.get_pos() #set's destination, will need to be offset
        self.dmg = int(shooter.F/10.0)
        self.image = var.arrow_img
        dest_list.add(self) #for player firing : self.level.projectile_list, for mobs self.level.projectile_ennemy_list
        var.has_shot = True
        
    def hit_test(self,character):
        test = pygame.sprite.spritecollideany(self, self.level.building_list, collided = None)
        if self.rect.colliderect(character.rect.inflate(-character.rect.width/4,-character.rect.height/4)) == True:
            arm = sum([x.arm for x in character.equipement.contents if isinstance(x, Armor) == True]) #sum of the values of all weapons in equipement
            dmg = self.random_dmg() - (character.E/10+arm)
            if dmg < 0:
                dmg = 0
            character.hp -= dmg
            self.kill()
            print 'has hit ! and dealt = {}'.format(dmg)
        elif test is not None:
            if test.rect.collidepoint(self.rect.center):
                self.kill()

        
    def move(self):
        if self.rect.inflate(2,5).collidepoint(self.dest) == True:
            self.kill()
        m_pos = self.dest
        speed = float(self.speed)
        
        xp = self.rect[0]-self.rect[2] 
        yp = self.rect[1]-self.rect[3]
        xm = m_pos[0]-self.rect[2] 
        ym = m_pos[1]-self.rect[3]
        
        dx = xm-xp
        dy = ym-yp 
        #dist = (dx**2+dy**2)**0.5 #get lenght to travel
        
        #calculates angle and sets quadrant
        if dx == 0 or dy == 0:
            angle_rad = 0#np.pi/2
            if dx == 0 and ym > yp:
                xoffset = 0
                yoffset = -speed
                self.orientation = 180
            elif dx == 0 and ym < yp:
                xoffset = 0
                yoffset = speed
                self.orientation = 0
            elif dy == 0 and xm > xp:
                xoffset = 0
                yoffset = -speed
                self.orientation = 90
            elif dy == 0 and xm < xp:
                xoffset = 0
                yoffset = speed
                self.orientation = 270
            else:
                xoffset, yoffset = 0,0
                self.orientation = 180
        elif xm > xp and ym > yp:
            angle_rad = np.arctan((abs(dy)/abs(dx)))
            xoffset = -np.cos(angle_rad)*speed
            yoffset = -np.sin(angle_rad)*speed
            self.orientation = angle_rad*(180.0/np.pi)+90
        elif xm < xp and ym > yp:
            angle_rad = np.arctan((abs(dx)/abs(dy)))
            xoffset =  np.sin(angle_rad)*speed
            yoffset = -np.cos(angle_rad)*speed
            self.orientation = angle_rad*(180.0/np.pi)+180
        elif xm < xp and ym < yp:
            angle_rad = np.arctan((abs(dy)/abs(dx)))
            xoffset = np.cos(angle_rad)*speed
            yoffset = np.sin(angle_rad)*speed
            self.orientation = angle_rad*(180.0/np.pi)+270
        else:# xm > xp and ym < yp:
            angle_rad = np.arctan((abs(dx)/abs(dy)))
            xoffset = -np.sin(angle_rad)*speed
            yoffset =  np.cos(angle_rad)*speed
            self.orientation = angle_rad*(180.0/np.pi)
        
        self.image = pygame.transform.rotate(var.arrow_img, -self.orientation)
        self.rect = self.rect.move(-xoffset,-yoffset)
        self.dest = (self.dest[0]-xoffset+var.xoffset,self.dest[1]-yoffset+var.yoffset)
        

class Level_Change(Building):
    def __init__(self, name, image, x, y, image_list, pair):
        self.hp = 1000
        self.value = 1000
        self.image_list = image_list
        self.pair = pair
        super(Level_Change, self).__init__(name, self.value, image, x, y, self.hp)
        
        '''anim timer'''
        self.anim_time = pygame.time.Clock()
        self.anim_time_left = 0        
        self.anim_speed = 1000/len(self.image_list)
        self.anim_counter = 0
        
    def anim(self):
        #updates anim timer
        self.anim_time.tick()
        self.anim_time_left += self.anim_time.get_time()
        #checks which anim to display based on the direction and if sprite is moving and alive
        if self.anim_time_left >= self.anim_speed: #checks time to animate
                if self.anim_counter >= len(self.image_list):
                    self.anim_counter = 0
                self.image = self.image_list[self.anim_counter]
                self.anim_time_left = 0
                self.anim_counter += 1
                
        
    def activate(self,char,new_level):
        self.anim()
        if char.rect.collidepoint(self.rect.midbottom):
            self.level.go_to(new_level, self.pair)

            
class Portal(Level_Change):
    def __init__(self, x, y, pair):
        self.name = 'Portal'
        self.image_list = var.portal_images
        self.image = self.image_list[0]
        super(Portal,self).__init__(self.name,self.image,x,y, self.image_list, pair)
        
    
    
    

    
    