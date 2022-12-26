import pygame
from settings import *
from support import import_images
import sys
from particles import Particles

class ImportImages:
    def __init__(self):
        self.player = self.import_player_assets("player")
        self.small_monsters = self.import_small_enemies_asssets(["axolot","beast","bamboo","skull","raccoon"])
        self.big_monster = self.import_big_monsters("raccoon")
        self.attacks = {
			# attacks 
			'claw': import_images('graphics/particles/claw'),
			'slash': import_images('graphics/particles/slash'),
			'sparkle': import_images('graphics/particles/sparkle'),
			'leaf_attack': import_images('graphics/particles/leaf_attack'),
			'thunder': import_images('graphics/particles/thunder'),
			"ice":import_images("graphics/particles/ice"),

			# monster deaths
			'axolot': import_images('graphics/particles/smoke_orange'),
			'raccoon': import_images('graphics/particles/raccoon'),
			'skull': import_images('graphics/particles/nova'),
			'bamboo': import_images('graphics/particles/bamboo'),
			"beast":import_images("graphics/particles/nova"),
			
			# leafs 
			'leaf': (
				import_images('graphics/particles/leaf1'),
				)
			}
     
    def create_particles(self,animation_type,pos,groups):
        animation_frames = self.attacks[animation_type]
        Particles(pos,animation_frames,groups)

    def import_player_assets(self,player):
        character_path = f"graphics/{player}/movement/"
        animations = {
            "up":[],"down":[],"right":[],"left":[],
            "up_idle":[],"down_idle":[],"right_idle":[],"left_idle":[],
            "up_attack":[],"down_attack":[],"right_attack":[],"left_attack":[],
            "dash":[],
        }

        for animation in animations.keys():
            full_path  = character_path + animation
            animations[animation] = import_images(full_path)
        return animations

    def import_small_enemies_asssets(self,small_monsters:list):
        local_dict = {}
        for monster in small_monsters:
            monster_path = f"graphics/enemies/{monster}/"
            animations = {"up":[],"down":[],"right":[],"left":[],"move":[],
                "idle":[],"attack":{},
            }

            for animation in animations.keys():
                full_path  = monster_path + animation
                animations[animation] = import_images(full_path)

            local_dict[monster] = animations
        return local_dict

    def import_big_monsters(self,big_monsters:list):
        local_dict = {}
        for monster in big_monsters:
            monster_path = f"graphics/enemies/{monster}/"
            animations = {"idle":[],"attack":[],"move":[]}#"up":[],"down":[],"right":[],"left":[],

            for animation in animations.keys():
                full_path  = monster_path + animation
                animations[animation] = import_images(full_path)
            local_dict[monster] = animations
        return local_dict

    

        #     #set image
            # self.rect = self.image.get_rect(center = self.hitbox.center)


