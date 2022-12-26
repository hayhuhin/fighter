from support import import_images
import pygame
from math import atan2, degrees, pi
from settings import *
from projectiles import Projectiles


class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        self.sprite_type = "weapon"
        self.player = player
        self.frame_index = 0
        self.direction = player.status.split("_")[0]
        self.player_angle = player.weapon_angle
        self.surface = pygame.display.get_surface()
        self.attack_type = player.weapon

        #returns self.angle by the player.weapon_angle
        self.all_angle_rotation()


        #graphic
        full_path = f"graphics/player/weapon/{player.weapon}/Sprite.png"
        the_surf = pygame.image.load(full_path).convert_alpha()
        reversed_image = pygame.transform.rotate(the_surf,self.angle)
        self.image = reversed_image
        self.rect = self.curr_rect()

        #bow weapon animation
        self.bow_index = 0
        self.animation_speed = 0.20

        #weapon animation timer
        self.weapon_timer = 600
                  
    def curr_rect(self):
        player = self.player
        if "idle" in self.player_angle:
            self.player_angle = self.direction
        if player.weapon == "bow" or player.weapon == "magicwand":
            if self.player_angle == "right_up":
                self.rect = self.image.get_rect(bottomleft=(player.rect.topright + pygame.math.Vector2(-15,15)))
            if self.player_angle == "right_down":
                self.rect = self.image.get_rect(topleft=(player.rect.bottomright + pygame.math.Vector2(-15,-15)))
            if self.player_angle == "left_up":
                self.rect = self.image.get_rect(bottomright=(player.rect.topleft + pygame.math.Vector2(15,15)))
            if self.player_angle == "left_down":
                self.rect = self.image.get_rect(topright=(player.rect.bottomleft + pygame.math.Vector2(15,-15)))    
            if self.player_angle == "left":
                self.rect = self.image.get_rect(midright=(player.rect.midleft)+ pygame.math.Vector2(10,5))
            if self.player_angle == "up":
                self.rect = self.image.get_rect(midbottom=(player.rect.midtop)+ pygame.math.Vector2(0,10))
            if self.player_angle == "down":
                self.rect = self.image.get_rect(midtop=(player.rect.midbottom)+ pygame.math.Vector2(0,-10))
            if self.player_angle == "right":
                self.rect = self.image.get_rect(midleft=(player.rect.midright)+ pygame.math.Vector2(-10,5))
            # else:
            #     self.rect = self.image.get_rect(center=(player.rect.center))
        else:
            if self.player_angle == "right_up":
                self.rect = self.image.get_rect(bottomleft=(player.rect.topright + pygame.math.Vector2(-7,10)))
            if self.player_angle == "right_down":
                self.rect = self.image.get_rect(topleft=(player.rect.bottomright + pygame.math.Vector2(-15,-15)))
            if self.player_angle == "left_up":
                self.rect = self.image.get_rect(bottomright=(player.rect.topleft + pygame.math.Vector2(15,15)))
            if self.player_angle == "left_down":
                self.rect = self.image.get_rect(topright=(player.rect.bottomleft + pygame.math.Vector2(15,-15)))    
            if self.player_angle == "left":
                self.rect = self.image.get_rect(midright=(player.rect.midleft)+ pygame.math.Vector2(10,5))
            if self.player_angle == "up":
                self.rect = self.image.get_rect(midbottom=(player.rect.midtop)+ pygame.math.Vector2(0,10))
            if self.player_angle == "down":
                self.rect = self.image.get_rect(midtop=(player.rect.midbottom)+ pygame.math.Vector2(0,-10))
            if self.player_angle == "right":
                self.rect = self.image.get_rect(midleft=(player.rect.midright)+ pygame.math.Vector2(-10,5))
        
        return self.rect

    def default_animation(self):
        animation = pygame.image.load(f"graphics/player/weapon/{self.player.weapon}/Sprite.png").convert_alpha()
        reversed_image = pygame.transform.rotate(animation,self.angle-180)
        self.image = reversed_image

    def bow_animation(self):#pos,player,mouse_pos
        animations = import_images("graphics/player/weapon/bow/bow_ann")
        self.bow_index += self.animation_speed
        if self.bow_index >= len(animations):
            # self.player.weapon_animation_ended = True
            self.kill()
        else:
            # self.image = animations[int(self.bow_index)]
            # self.player.weapon_animation_ended = False
            reversed_image = pygame.transform.rotate(animations[int(self.bow_index)],self.angle)
            self.image = reversed_image

    def all_angle_rotation(self):
        mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        origin_x = WIDTH // 2
        origin_y = HEIGHT // 2
        dx = mouse_pos.x - origin_x
        dy = mouse_pos.y - origin_y
        rads = atan2(-dy,dx)
        rads %= 2*pi
        degs = degrees(rads)
        self.angle = degs -270

    def eight_angle_rotation(self):
        curr_angle = self.player_angle 
        if curr_angle == "right_up":
            self.angle = 135
        if curr_angle == "right":
            self.angle = 90
        if curr_angle == "up":
            self.angle = 180
        if curr_angle == "left_up":
            self.angle = 225
        if curr_angle == "left":
            self.angle = 270
        if curr_angle == "left_down":
            self.angle = 315
        if curr_angle == "down":
            self.angle = 0
        if curr_angle == "right_down":
            self.angle = 45
      
    def cooldowns(self):
        curr_time = pygame.time.get_ticks()
        if curr_time - self.player.attack_time  >= self.weapon_timer:
            self.kill()
            self.player.clicked = False

    def weapon_animation(self):
        if self.attack_type == "bow":
            self.bow_animation()
        else:
            self.default_animation()

    def update(self):
        self.weapon_animation()
        self.cooldowns()


