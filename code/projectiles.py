import pygame
from settings import *
from support import import_images
from math import atan2, degrees, pi


class Projectiles(pygame.sprite.Sprite):
    """this class is needed to be called from weapon class"""
    def __init__(self,player,groups):
        super().__init__(groups)
        self.sprite_type = "projectile"
        self.surface = pygame.display.get_surface()
        #weapon setup 
        self.weapon_type = player.weapon
        self.direction = pygame.math.Vector2()

        #player data
        self.player = player
        self.weapon_animation_ended = False

        self.sides = player.status.split("_")[0]


        #animation setup 
        self.frame_index = 0
        self.animation_speed = 0.16
        self.shoot_timer = 1200
        self.speed = 6
        self.launch_timer = None
        self.launch = False

        #mouse position 
        self.mouse_pos = pygame.mouse.get_pos()

        #player angle and current spell check
        self.weapon_spell_choosed()#return self.chosen_spell
        self.update_projectile_angle_advanced()

        #general setup 
        full_path = shooting_data[self.weapon_type][self.chosen_spell]["graphic"] #must be changed to every other spells
        the_surf = pygame.image.load(full_path).convert_alpha()
        reversed_image = pygame.transform.rotate(the_surf,self.angle)
        self.image = reversed_image
        self.rect = self.curr_rect()

    def weapon_spell_choosed(self):
        if self.weapon_type == "bow":
            self.chosen_spell = "arrow"
        elif self.weapon_type == "magicwand":
            self.chosen_spell = self.player.magic
        else:
            self.chosen_spell = "none"

    def terminate_projectile(self):#changes in player.clicked statement to False
            self.kill()
            self.player.clicked = False

    def curr_rect(self):
        self.player_angle = self.player.weapon_angle
        player = self.player
        if "idle" in self.player_angle:
            self.player_angle = self.sides
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
        return self.rect

    def animate_projectile(self,):
        if not self.launch:
            self.launch = True
            self.launch_timer = pygame.time.get_ticks()
            animations = import_images(self.data[self.weapon_type]["data"]["graphic"])
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animations)-1:
                self.frame_index = 0
            else:
                reversed_image = pygame.transform.rotate(animations[int(self.frame_index)],self.angle)
                self.image = reversed_image

    def projectile_movement(self):
        destination_vec = pygame.math.Vector2(self.mouse_pos)
        origin_vec = pygame.math.Vector2(WIDTH//2,HEIGHT//2)
        direction = (origin_vec-destination_vec).normalize()
        self.direction = -direction

    def update_projectile_angle_advanced(self):
        mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        origin_x = WIDTH // 2
        origin_y = HEIGHT // 2
        dx = mouse_pos.x - origin_x
        dy = mouse_pos.y - origin_y
        rads = atan2(-dy,dx)
        rads %= 2*pi
        degs = degrees(rads)
        self.angle = degs -270

    def move(self,speed):
        self.rect.x += self.direction.x * speed
        self.rect.y += self.direction.y * speed

    def cooldowns(self):
        curr_time = pygame.time.get_ticks()
        if curr_time - self.player.attack_time >= self.shoot_timer:
            self.terminate_projectile()
        if self.launch:
            if curr_time - self.launch_timer >= 400:
                self.launch = False
                
    def update(self):
        self.move(self.speed)
        self.projectile_movement()
        self.cooldowns()


