import pygame
from settings import *
from support import import_images

class Magic(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)

        #basic setup
        self.sprite_type = "spell"
        self.player = player
        self.heal_graphic = import_images(magic_data["heal"]["graphic"])
        self.shield_graphic = import_images(magic_data["shield"]["graphic"])
        self.animation_speed = 0.16
        self.frame_index = 0
        self.surface = pygame.display.get_surface()

        #animation setup
        self.spell_time = 300
        self.spell_on = False
        self.spell_timer = None

    def cooldowns(self):
        curr_time = pygame.time.get_ticks()
        if self.spell_on:
            if curr_time - self.spell_timer >= self.spell_time:
                self.spell_on = False

    def animate(self):

        #timer setup
        self.spell_on = True
        self.spell_timer = pygame.time.get_ticks()

        #animation setup
        self.frame_index += self.animation_speed
        player_choosed_spell = self.player.curr_spell
        # player_choosed_spell = "heal"
        if player_choosed_spell == "heal":
            frames = self.heal_graphic
        elif player_choosed_spell == "shield":
            frames = self.shield_graphic
        
        if self.frame_index >= len(frames):
            self.kill()
        else:
            self.image = frames[int(self.frame_index)]
            self.rect = self.image.get_rect(center=(self.player.rect.center + pygame.math.Vector2(2,5)))

    def update(self):
        self.animate()
        self.cooldowns()
