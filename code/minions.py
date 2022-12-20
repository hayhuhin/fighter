import pygame
from settings import *
from support import import_images
from entity import Entity

class Minions(Entity):
    def __init__(self,groups,pos,creator_name):
        super().__init__(groups)
        self.import_graphics(creator_name)
        self.display_surf = pygame.display.get_surface()
        self.status = "down"
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=(30,1300))

    def import_graphics(self,name):
        self.animations = {"down":[],"left":[],"right":[],"up":[],"idle":[]}
        main_path = f"graphics/enemies/{name}/summoning/"#TODO must to change 
        for animation in self.animations.keys():
            self.animations[animation] = import_images(main_path+animation)



    def animate(self):
        animations = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animations):
            self.frame_index = 0

        self.image = animations[int(self.frame_index)]
        self.rect = self.image.get_rect(center=(self.rect.center))


    def update(self):
        self.animate()
        print("summond")



        