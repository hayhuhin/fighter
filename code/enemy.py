import pygame
from settings import *
from entity import Entity
from support import *
from pictures import ImportImages


class Enemy(Entity):
    def __init__(self,monster_type,pos,groups,obstacle_sprites,damage_player,trigger_death):
        super().__init__(groups)
        #general setup
        # self.import_graphics(monster_type)
        pic = ImportImages()
        self.animations = pic.small_monsters[monster_type]
        self.sprite_type = "enemy"
        self.status = "idle"
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=(pos))
        self.hitbox = self.rect.inflate(-10,-10)
        self.pos = pos

        #movement
        self.obstacle_sprites = obstacle_sprites
        
        #stats
        self.monster_name = monster_type
        self.monster_info = monster_data[self.monster_name]
        self.health = self.monster_info['health']
        self.exp = self.monster_info['exp']
        self.speed = self.monster_info['speed']
        self.attack_damage = self.monster_info['damage']
        self.resistance = self.monster_info['resistance']
        self.attack_radius = self.monster_info['attack_radius']
        self.notice_radius = self.monster_info['notice_radius']
        self.attack_type = self.monster_info['attack_type']
        self.attack_sound = self.monster_info["attack_sound"]

        #player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death = trigger_death
        self.aggro = False


        #invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invinvibility_duration = 300

        #spell casting setup
        self.cast_skill = True
        self.cast_skill_timer = None
        self.cast_skill_time = 400
        self.spawn = True

        self.attack_music = pygame.mixer.Sound(self.attack_sound)
        self.attack_music.set_volume(0.2)

    def import_graphics(self,name):
        if name == "raccoon":
            self.animations = {"idle":[],"move":[],"attack":[],"attack_1":[],"attack_2":[]}
            main_path = f"graphics/enemies/{name}/"
            for animation in self.animations.keys():
                self.animations[animation] = import_images(main_path+animation)

        else:
            self.animations = {"idle":[],"down":[],"left":[],"right":[],"up":[],"attack":[]}
            main_path = f"graphics/enemies/{name}/"
            for animation in self.animations.keys():
                self.animations[animation] = import_images(main_path+animation)

    def animate(self):
        animations = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animations):
            self.frame_index = 0
            if self.status == "attack":
                self.can_attack = False

        self.image = animations[int(self.frame_index)]
        self.rect = self.image.get_rect(center=(self.hitbox.center))

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
            #flicker
        else:
            self.image.set_alpha(255)

    def enemy_attack_logic(self):#effects raccoon for attacking animate  destroyable objects
        if self.monster_name != "raccoon":
            self.status = "attack"

        if self.monster_name == "raccoon":
            self.status = "attack"
            self.hitbox = self.rect.inflate(+10,+10)
            if self.health >= self.monster_info['health']//2:
                self.spawn = True
                self.speed = 0
            self.speed = self.monster_info["speed"]

    def destroy_objects(self):#check every enemy col and obstacle
        for coll_sprite in self.obstacle_sprites:
            if coll_sprite.sprite_type == "destroyable":
                if coll_sprite.rect.colliderect(self.hitbox):
                    coll_sprite.deal_damage()

    def get_player_distance_direction(self,player):
        enemy_rect = (WIDTH//2,HEIGHT//2)
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        # direction = pygame.math.Vector2(0,0)

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            # direction = pygame.math.Vector2(0,0)
            direction = pygame.math.Vector2()


        return(distance,direction)

    def get_status(self,player):
        distance = self.get_player_distance_direction(player)[0]
        if self.monster_name == "raccoon":
            if not player.death:
                if distance <= self.attack_radius and self.can_attack:
                    if self.status != "attack":
                        self.frame_index = 0
                    self.enemy_attack_logic()
                elif distance <= self.notice_radius :
                    self.status = "move"
                else:
                    self.status = "idle"
            if self.health <= 0:
                self.kill()
        else:
            if distance <= self.attack_radius and self.can_attack:
                    if self.status != "attack":
                        self.frame_index = 0
                    self.enemy_attack_logic()
            elif distance <= self.notice_radius :
                self.status = self.side
            else:
                self.status = "idle"
        if self.health <= 0:
            self.kill()

    def actions(self,player):
        if self.status == "attack":
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage,self.attack_type)
            self.attack_music.play(0)

        elif self.status == "move":
            self.direction = self.get_player_distance_direction(player)[1]

        
        elif self.aggro:
            self.direction = self.get_player_distance_direction(player)[1]
        
        elif self.status in ["right","left","up","down"]:
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            self.hitbox.x += self.direction.x *speed
            self.collision("horizontal")
            self.hitbox.y += self.direction.y * speed
            self.collision("vertical")

    def check_death(self):
        if self.health <= 0:
            self.trigger_death(self.rect.center,self.monster_name)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >=self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >=self.invinvibility_duration:
                self.vulnerable = True

    def get_damage(self,player,attack_type):
        if self.vulnerable:
            self.aggro = True
            self.direction = self.get_player_distance_direction(player)[1]

            if attack_type == "weapon":
                self.health -= player.get_full_weapon_damage()

            if attack_type == "projectile":
                self.health -= player.get_full_damage_projectile(player.weapon)

            else:
                pass #magic damage
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.move(self.speed)
        self.animate()
        self.destroy_objects()
        self.cooldown()
        self.direction_side()
        self.check_death()

    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)




