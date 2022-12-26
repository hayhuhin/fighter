from random import choice
import pygame
from settings import *
from tile import Tile
from player import Player
from support import import_csv_layout,import_images
from weapon import Weapon
from ui import Ui
from projectiles import Projectiles
from enemy import Enemy
from magic import Magic
from pictures import ImportImages


class Level:
    def __init__(self):

        #function for getting the display surface
        self.display_surface = pygame.display.get_surface()

        #sprite group setup 
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        #atack sprites
        self.attackable_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()


        #attack sprites
        self.curr_atk = None

        #user interface
        self.ui = Ui()


        #particles 
        self.animation_player = ImportImages()

        #sprite setup 
        self.create_map()

    def create_map(self):
        layout = {
            "boundry": import_csv_layout("level/0/fixed_boundry_green_bg_floor.csv"),
            "grass" : import_csv_layout("level/0/fixed_boundry_grass.csv"),
            "trees" : import_csv_layout("level/0/fixed_boundry_trees.csv"),
            "buildings" : import_csv_layout("level/0/fixed_boundry_buildings.csv"),
            "enemies" : import_csv_layout("level/0/fixed_boundry_player_test.csv"),
        }

        graphics = {
            "trees": import_images("graphics/map/trees/pink_and_yellow")
        }

        for style,layout in layout.items():
            for index_row,row in enumerate(layout):
                for index_col,col in enumerate(row):
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    if style == "boundry":
                        if col == "12" or col == "24":     
                            Tile((x,y),[self.obstacles_sprites],"invisible")

                    if style == "trees":#17,15,19
                        if col in ["17","15","19"]:
                            rand_tree = choice(graphics["trees"])     
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],"invisible",surface=rand_tree)
                        if col == "10":
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],"invisible",surface=pygame.image.load("graphics/map/trees/dark_trees/s_tree3.png"))
                        if col =="5":
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites,self.attackable_sprites],"destroyable",surface=pygame.image.load("graphics/map/trees/triple_dark_trees/tree6.png"))
                        if col == "16":
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],"invisible",surface=pygame.image.load("graphics/map/trees/big_green_tree/green_tree.png"))
                        if col == "11":
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],"invisible",surface=pygame.image.load("graphics/map/trees/small_tree/s_tree4.png"))
                        if col == "8":
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],"invisible",surface=pygame.image.load("graphics/map/trees/small_bush/s_tree1.png"))

                    if style == "buildings":
                        if col == "0":
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],"invisible",surface=pygame.image.load("graphics/map/buildings/0house.png"))
                        if col == "1":
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],"invisible",surface=pygame.image.load("graphics/map/buildings/1house.png"))
                        
                        if col == "4":
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],"invisible",surface=pygame.image.load("graphics/map/buildings/4house.png"))

                        if col =="5":
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],"invisible",surface=pygame.image.load("graphics/map/buildings/5house.png"))

                        if col == "6":
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],"invisible",surface=pygame.image.load("graphics/map/buildings/6house.png"))

                        if col == "7":
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],"invisible",surface=pygame.image.load("graphics/map/buildings/7house.png"))

                        if col == "9":
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],"invisible",surface=pygame.image.load("graphics/map/buildings/9house.png"))

                        if col == "10":
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],"invisible",surface=pygame.image.load("graphics/map/buildings/10house.png"))

                        # if col == "14":
                        #     Tile((x,y),[self.visible_sprites],"invisible",surface=pygame.image.load("graphics/map/buildings/14stairs.png"))

                        if col == "15":
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],"invisible",surface=pygame.image.load("graphics/map/buildings/15pilar.png"))

                    if style == "enemies":
                        if col != "-1":
                            if col == "0":
                                self.player = Player((x,y),
                                [self.visible_sprites],
                                self.obstacles_sprites,
                                self.create_attack,
                                self.destroy_attack,
                                self.create_magic
                                )
                            else:
                                if col == "2":monster_name = "bamboo"
                                elif col == "1":monster_name = "raccoon"
                                elif col == "3":monster_name = "axolot"
                                elif col == "4":monster_name = "skull"
                                elif col == "5":monster_name = "beast"
                                enemy = Enemy(monster_name,(x,y),
                                [self.visible_sprites,self.attackable_sprites],
                                self.obstacles_sprites,self.damage_player,
                                self.trigger_death)

    def create_attack(self):
        if self.player.weapon == "bow" or self.player.weapon == "magicwand":
            self.curr_atk = Weapon(self.player,[self.visible_sprites,self.attack_sprites])
            self.curr_projectile = Projectiles(self.player,[self.visible_sprites,self.attack_sprites])
        else:
            self.curr_atk = Weapon(self.player,[self.visible_sprites,self.attack_sprites])

    def create_magic(self,style,strength,cost):
        if self.player.energy >= cost:
            if style == "heal":
                self.player.energy -= cost
                if self.player.health < self.player.stats["health"]:
                    self.player.health += strength
            elif style == "shield":
                self.player.hurt_time = pygame.time.get_ticks()
                self.player.energy -= cost
                self.player.imune = True
            self.curr_spell = Magic(self.player,[self.visible_sprites])
            self.curr_spell.animate()

    def destroy_attack(self):
        pass

    def player_attack_logic(self):
        if self.attack_sprites:
            for attacking_weapon in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attacking_weapon,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "destroyable":
                            target_sprite.deal_damage()
                            if attacking_weapon.sprite_type == "projectile":
                                attacking_weapon.terminate_projectile()
                            if target_sprite.lives <= 0:
                                target_sprite.kill()


                        else:
                            target_sprite.get_damage(self.player,attacking_weapon.sprite_type)
                            if attacking_weapon.sprite_type == "projectile":
                                attacking_weapon.terminate_projectile()

    def enemy_go_away_after_player_death(self):
        for enemy in self.attackable_sprites:
            if self.player.rect.colliderect(enemy):
                if self.player.death:
                    enemy.direction = pygame.math.Vector2(0,1)
                    enemy.status = "idle"
                    enemy.aggro = False

    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

    def trigger_death(self,pos,particle_type):
        self.animation_player.create_particles(particle_type,pos,[self.visible_sprites])

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.enemy_go_away_after_player_death()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        
        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #creating the floor
        self.floor_surf = pygame.image.load("graphics/map/new.bmp").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,"sprite_type") and sprite.sprite_type == "enemy"]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

    def custom_draw(self,player):
        #player offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #map offset itself
        floor_offset_pos  = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)



        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)