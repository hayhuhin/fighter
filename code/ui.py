import pygame
from settings import *

class Ui:
    def __init__(self):
        #general
        self.alpha_index = 0
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
        # bar setup
        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10,16,ENERGY_BAR_WIDTH,BAR_HEIGHT)

        self.weapon_graphics = []
        self.mouse_pos = pygame.mouse.get_pos()

        for weapon in weapon_data.values():
            path = weapon["graphic"]
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

    def mainmenu(self,menu_active):
        if menu_active:
            image = pygame.image.load("graphics/HUD/menu/menu.png").convert_alpha()
            

            #text setup "start"
            start_text_surf = self.font.render(str("continue"),False,TEXT_COLOR)
            start_text_rect = start_text_surf.get_rect(center=((WIDTH/2),(HEIGHT/2)-12))
            #text setup "exit"
            exit_text_surf = self.font.render(str("exit"),False,TEXT_COLOR)
            exit_text_rect = exit_text_surf.get_rect(center=((WIDTH/2),(HEIGHT/2)+8))

            width_menu_bar = start_text_rect.width + 18

            #bg menu setup
            bg_menu_surf = pygame.transform.scale(image,(width_menu_bar,66))
            bg_menu_rect = bg_menu_surf.get_rect(center=(WIDTH/2,HEIGHT/2))

            #bar menu rect
            start_bar_image = pygame.image.load("graphics/HUD/menu/bar.png")
            start_bar_scaled = pygame.transform.scale(start_bar_image,(width_menu_bar-6,16))
            start_rect = start_bar_image.get_rect(center=(WIDTH/2-10,HEIGHT/2-10))

            #bar exit text
            exit_var_rect = start_bar_image.get_rect(center=(WIDTH/2-10,HEIGHT/2+10))

            #displaying all surfaces

            self.display_surface.blit(bg_menu_surf,bg_menu_rect)
            self.display_surface.blit(start_bar_scaled,start_rect)
            self.display_surface.blit(start_bar_scaled,exit_var_rect)

            #texts drawing
            self.display_surface.blit(start_text_surf,start_text_rect)
            self.display_surface.blit(exit_text_surf,exit_text_rect)
            
    def show_bar(self,current,max_amount,bg_rect,color):
        #draw bg
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)

        #converting stats to pixels
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        if current_rect.width > bg_rect.width:
            current_rect.width = bg_rect.width
        

        #drawing the bar
        pygame.draw.rect(self.display_surface,color,current_rect,0)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,1)

    def show_exp(self,exp):
        text_surf = self.font.render(str(int(exp)),False,TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomright=((WIDTH)-20,(HEIGHT)-20))

        pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(8,8))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(8,8),1)
    
    def death_message(self,player_dead):

        text_surf = self.font.render(str("YOU ARE DEAD"),False,TEXT_COLOR)
        text_rect = text_surf.get_rect(center=((WIDTH/2),((HEIGHT)/2)-30))

        bg_surf = pygame.Surface((text_rect.width+8,text_rect.height+8))
        bg_surf.fill(UI_BG_COLOR)

        ui_border = pygame.Surface((text_rect.width+8,text_rect.height+8))
        ui_border.fill(UI_BORDER_COLOR)

        if player_dead:
            if self.alpha_index < 255:
                self.alpha_index += 1
                text_surf.set_alpha(int(self.alpha_index))
                bg_surf.set_alpha(int(self.alpha_index))
                ui_border.set_alpha(int(self.alpha_index))

            else:
                self.alpha_index = 255

            self.display_surface.blit(bg_surf,text_rect.inflate(8,8))
            self.display_surface.blit(ui_border,(text_rect.inflate(8,8)))
            self.display_surface.blit(text_surf,text_rect)

    def selection_box(self,left,top,has_switched):
        bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR_ACTIVE,bg_rect,1)

        else:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,1)
        return bg_rect

    def weapon_overlay(self,weapon_index,has_switched,player):
        #left weapon overlay
        bg_rect = self.selection_box(16,215,has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=(bg_rect.center))

        #right skill overlay
        has_switched = False
        magic_bg_rect = self.selection_box(30,222,has_switched)
        magic_surf = self.get_available_magic(player,weapon_index)
        magic_rect = magic_surf.get_rect(center=(magic_bg_rect.center))

        #spell overley setup
        spell_bg_rect = self.selection_box(46,215,has_switched)
        spell_surf = self.get_available_spell(player,"spell")
        spell_rect = spell_surf.get_rect(center=(spell_bg_rect.center))


        #drawing
        self.display_surface.blit(weapon_surf,weapon_rect)#weapon overlay
        self.display_surface.blit(magic_surf,magic_rect)#magic overley/another items related to the weapon
        self.display_surface.blit(spell_surf,spell_rect)#spells overlay(shield or heal)

    def get_available_magic(self,player,weapon_index):
        weapon_type = player.weapon
        spell_index = player.magic_index
        if weapon_type == "bow":
            path  = shooting_data["bow"]["arrow"]["graphic"]
            surf = pygame.image.load(path).convert_alpha()
        elif weapon_type == "magicwand":
            path = shooting_data["magicwand"][player.magic]["graphic"]
            surf = pygame.image.load(path).convert_alpha()
        else:
            surf = self.weapon_graphics[weapon_index]
        return surf

    def get_available_spell(self,player,spell_index):
        curr_spell = player.curr_spell
        full_path = f"graphics/player/icons/all_icons/{curr_spell}.png"
        surf = pygame.image.load(full_path).convert_alpha()
        return surf

    def display(self,player):
        # pygame.draw.rect(self.display_surface,"black",self.health_bar_rect)
        self.show_bar(player.health,player.stats["health"],self.health_bar_rect,HEALTH_COLOR)#max_amount,current,bg_rect,color
        self.show_bar(player.energy,player.stats["energy"],self.energy_bar_rect,ENERGY_COLOR)
        self.show_exp(player.exp)
        self.weapon_overlay(player.weapon_index,not player.can_switch_Weapon,player)
        self.mainmenu(player.menu)

        #player dead
        self.death_message(player.death)