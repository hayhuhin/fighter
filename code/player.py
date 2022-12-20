import pygame
from settings import *
from support import import_images
from entity import Entity

class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_magic):
        super().__init__(groups)
        self.image = pygame.image.load("graphics/player/movement/down/tile016.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(pos))
        self.hitbox = self.rect.inflate(-20,-20)

        #basic setup
        self.basic_time = 200
        self.cant_move = False



        #graphics setup
        self.import_character_assets()
        self.status = "down"
        self.animation_speed = 0.20

        #directions setup
        self.curr_mouse_pos = pygame.mouse.get_pos()
        self.attacking = False
        self.attack_cooldown = 500
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites
        self.weapon_angle = ""
        self.death = False

        #dash attributes
        self.dash_timer = None
        self.can_dash = True
        self.dash_time = 800
        self.dash_distance = 28

        #weapons
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_Weapon = True
        self.weapon_switch_time = None
        self.switch_cooldown = 140
        self.weapon_animation_ended = True
        # self.combat_style = "long_range"



        #magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(shooting_data["magicwand"])[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None


        #heal/shield spells
        # self.spell_data = list(magic_data)[self.magic_index]
        self.spell_index = 0
        self.curr_spell = list(magic_data.keys())[self.magic_index]
        self.can_switch_spell = True
        self.spell_switch_time = None

        #shield attributes
        self.imune = False
        self.imune_timer = None
        self.imune_duration = 3000



        #click events
        self.clicked = False
        self.clicked_side = ""

        #stats
        self.stats = {"health":100,"energy":60,"attack":10,"magic":4,"speed":3,"regeneration":2}
        self.health = 100
        self.energy = self.stats["energy"]
        self.exp = 0
        self.speed = self.stats["speed"]

        #damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerabillity_duration = 1000

        #MENU setup 
        self.menu = False
        self.menu_timer = None
        self.can_click = True



    def current_click_side(self):
        """returns state of a player after every click
        helps to create in projectiles class normal arrow projectile"""
        if self.clicked:
            self.clicked_side = self.weapon_angle
        else:
            self.clicked = False

    def animate(self):
        if not self.death:
            animation = self.animations[self.status]
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = 0

                #set image
            self.image = animation[int(self.frame_index)]
            self.rect = self.image.get_rect(center = self.hitbox.center)

            if not self.vulnerable and not self.imune:
                alpha = self.wave_value()
                self.image.set_alpha(alpha)
            else:
                self.image.set_alpha(255)

    def get_Status(self):
        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status :
                if "idle" in self.status:
                    self.status = self.status.replace("_idle","_attack")
                else:
                    self.status = self.status + "_attack"
        if not self.can_dash:
            self.status = "dash"

        elif self.attacking == False:
            if "attack" in self.status:
                self.status = self.status.replace("_attack","")

    def import_character_assets(self):
        character_path = "graphics/player/movement/"
        self.animations = {
            "up":[],"down":[],"right":[],"left":[],
            "up_idle":[],"down_idle":[],"right_idle":[],"left_idle":[],
            "up_attack":[],"down_attack":[],"right_attack":[],"left_attack":[],
            "dash":[],
        }

        for animation in self.animations.keys():
            full_path  = character_path + animation
            self.animations[animation] = import_images(full_path)

    def get_weapon_angle(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos_x = mouse_pos[0]
        mouse_pos_y = mouse_pos[1]
        if mouse_pos_x < 160 and mouse_pos_y > 160 :
            self.weapon_angle = "left_down"
        elif mouse_pos_x > 220 and mouse_pos_y > 160:
            self.weapon_angle = "right_down"
        elif mouse_pos_x < 160 and mouse_pos_y < 100 :
            self.weapon_angle = "left_up"
        elif mouse_pos_x > 220 and mouse_pos_y < 100 :
            self.weapon_angle = "right_up"
    
    def create_attack(self):
        if self.clicked:
            self.create_attack()
            self.clicked = False

    def destroy_att(self):
        self.destroy_attack()

    def mouse_pos(self):
        mouse_pos_current = pygame.mouse.get_pos()
        if mouse_pos_current[0] < 160 :
            self.status = "left"
        elif mouse_pos_current[0] > 220 :
            self.status = "right"
        elif mouse_pos_current[1] < 100 :
            self.status = "up"
        elif mouse_pos_current[1] > 160 :
            self.status = "down"
        self.weapon_angle = self.status

    def input(self):
        if not self.attacking and not self.death: 
            keys = pygame.key.get_pressed()
            mouse_click = pygame.mouse.get_pressed()
                #movement input
            if keys[pygame.K_a] :
                self.direction.x = -1
                # self.status = "left"
            elif keys[pygame.K_d] :
                self.direction.x = 1
                # self.status = "right"

            else:
                self.direction.x = 0

            if keys[pygame.K_w] :
                self.direction.y = -1
                # self.status = "up"

            elif keys[pygame.K_s] :
                self.direction.y = 1
                # self.status = "down"

            else:
                self.direction.y = 0

            if keys[pygame.K_b]:
                if self.can_click:
                    self.can_click = False
                    self.menu_timer = pygame.time.get_ticks()
                    if self.menu:
                        self.menu = False
                        self.cant_move = False
                        self.speed = self.stats["speed"]
                    else:
                        self.menu = True
                        self.cant_move = True
                        self.speed = 0
            elif keys[pygame.K_SPACE]:
                self.dash()

                    
                


            if not self.clicked and not self.cant_move :
                self.test = True
                if mouse_click[0] == True:
                    self.attacking = True
                    self.attack_time = pygame.time.get_ticks()
                    self.clicked = True
                    self.create_attack()

                    

                if keys[pygame.K_f]:
                    self.attacking = True
                    self.attack_time = pygame.time.get_ticks()
                    style = list(magic_data.keys())[self.spell_index]
                    strength = list(magic_data.values())[self.spell_index]["strength"] + self.stats["magic"]
                    cost = list(magic_data.values())[self.spell_index]["cost"]
                    self.create_magic(style,strength,cost)

                if keys[pygame.K_g]:
                    if self.can_switch_spell:
                        self.spell_switch_time = pygame.time.get_ticks()
                        if self.spell_index < len(list(magic_data.keys()))-1:
                            self.spell_index +=1
                        else:
                            self.spell_index = 0
                        self.can_switch_spell = False
                        self.curr_spell = list(magic_data.keys())[self.spell_index]


                if keys[pygame.K_q] and self.can_switch_Weapon:
                    self.can_switch_Weapon = False
                    self.weapon_switch_time = pygame.time.get_ticks()
                    if self.weapon_index < len(list(weapon_data.keys())) -1:
                        self.weapon_index += 1
                    else:
                        self.weapon_index = 0

                    self.weapon = list(weapon_data.keys())[self.weapon_index]

                if keys[pygame.K_e] and self.can_switch_magic:
                    self.can_switch_magic = False
                    self.magic_switch_time = pygame.time.get_ticks()
                    if self.magic_index < len(list(shooting_data["magicwand"])) -1:
                        self.magic_index += 1
                    else:
                        self.magic_index = 0

                    self.magic = list(shooting_data["magicwand"])[self.magic_index]

    def dash(self):
        if self.can_dash:
            self.animation_speed = 0.40
            self.can_dash = False
            self.dash_timer = pygame.time.get_ticks()
            dash_direction = self.weapon_angle
            if "right" in dash_direction:
                self.hitbox.x += self.dash_distance
            if "up" in dash_direction:
                self.hitbox.y -= self.dash_distance
            if "down" in dash_direction:
                self.hitbox.y += self.dash_distance
            if "left" in dash_direction:
                self.hitbox.x -= self.dash_distance
                
    def cooldowns(self):
        curr_time = pygame.time.get_ticks()

        if self.attacking:
            if curr_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]["cooldown"]:
                self.attacking = False
                # self.clicked = False
                self.destroy_attack()


        if not self.can_switch_Weapon :
            if curr_time - self.weapon_switch_time >= self.switch_cooldown:
                self.can_switch_Weapon = True

        if not self.can_switch_magic :
            if curr_time - self.magic_switch_time >= self.switch_cooldown:
                self.can_switch_magic = True
    
        if not self.vulnerable:
            if curr_time - self.hurt_time >= self.invulnerabillity_duration:
                self.vulnerable = True

        if not self.can_switch_spell:
            if curr_time - self.spell_switch_time >=self.switch_cooldown:
                self.can_switch_spell = True

        if self.imune:
            self.vulnerable = False
            if curr_time - self.hurt_time >= self.imune_duration:
                self.imune = False

        if not self.can_click:
            if curr_time - self.menu_timer >= self.basic_time:
                self.can_click = True

        if not self.can_dash:
            if curr_time - self.dash_timer >= self.dash_time:
                self.can_dash = True
                self.animation_speed = 0.20

    def get_full_damage_projectile(self,weapon_type):
        if weapon_type == "bow":
            chosen_projectile = "arrow"
            base_damage = weapon_data["bow"]["damage"]
            weapon_damage = shooting_data[weapon_type][chosen_projectile]["strength"]
        elif weapon_type == "magicwand":
            chosen_projectile = self.magic
            base_damage = weapon_data["magicwand"]["damage"]
            weapon_damage = shooting_data[weapon_type][chosen_projectile]["strength"]
        print(base_damage + weapon_damage)
        return base_damage + weapon_damage

    def energy_regeneration(self):
        if self.energy < self.stats["energy"]:
            self.energy += (self.stats["regeneration"])/50

    def get_full_weapon_damage(self):
        base_damage = self.stats["attack"]
        weapon_damage = weapon_data[self.weapon]["damage"]
        print(weapon_damage+base_damage)
        return base_damage + weapon_damage

    def death_animation(self):
        if self.health <= 0 :
            self.direction = pygame.math.Vector2()
            self.death = True
            self.frame_index += 0.12
            animation = import_images("graphics/player/death")
            if self.frame_index >= len(animation)-1:
                self.image = animation[len(animation)-1]
            else:
                self.image = animation[int(self.frame_index)]

    def update(self):
        self.input()
        self.cooldowns()
        self.get_Status()
        self.animate()
        self.death_animation()
        self.mouse_pos()
        self.get_weapon_angle()
        self.current_click_side()
        self.move(self.speed)
        self.energy_regeneration()

        # print(self.menu)










