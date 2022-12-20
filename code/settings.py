WIDTH = 380
HEIGHT = 240
FPS = 40


TILE_SIZE = 16


#ui data
BAR_HEIGHT = 5
HEALTH_BAR_WIDTH = 60
ENERGY_BAR_WIDTH = 40
ITEM_BOX_SIZE = 18
UI_FONT = "graphics/HUD/Font/NormalFont.ttf"
UI_FONT_SIZE = 8

#general colors
WATER_COLOR = "#71DDEE"
UI_BG_COLOR = "#222222"
UI_BORDER_COLOR = "#111111"
TEXT_COLOR = "#EEEEEE"

#ui colors 
HEALTH_COLOR = "red"
ENERGY_COLOR = "blue"
UI_BORDER_COLOR_ACTIVE = "gold"


#weapon data
weapon_data = {
    "bow":{"cooldown":50,"damage":10,"graphic":"graphics/player/weapon/bow/Sprite.png"},
    "sword":{"cooldown":100,"damage":15,"graphic":"graphics/player/weapon/sword/Sprite.png"},
    "axe":{"cooldown":300,"damage":20,"graphic":"graphics/player/weapon/axe/Sprite.png"},
    "hammer":{"cooldown":400,"damage":30,"graphic":"graphics/player/weapon/hammer/Sprite.png"},
    "magicwand":{"cooldown":150,"damage":8,"graphic":"graphics/player/weapon/magicwand/Sprite.png"},
    "pickaxe":{"cooldown":125,"damage":18,"graphic":"graphics/player/weapon/pickaxe/Sprite.png"},
}


#magic
magic_data = {
    "heal":{"strength":20,"cost":25,"graphic":"graphics/player/magic/body_effect/heal/heal_ann"},
    "shield":{"strength":30,"cost":40,"graphic":"graphics/player/magic/body_effect/shield/shield_ann"},
}

shooting_data = {
    "magicwand":{
            "shuriken": {"strength": 5,"cost":20,"graphic": "graphics/player/magic/projectiles/shuriken_magic/shuriken_magic_ann/tile000.png"},
            "fire": {"strength": 20,"cost":20,"graphic": "graphics/player/projectiles/energy_ball/energy_ball_ann/tile000.png"}
    },
    "bow":{
            "arrow" :{"strength": 10,"cost":0,"amount":0,"graphic": "graphics/player/projectiles/arrow/arrow.png"},
    }
}

monster_data = {
	'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'../audio/attack/slash.wav', 'speed': 1, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 30},
	'raccoon': {'health': 400,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'../audio/attack/claw.wav','speed': 2, 'resistance': 0, 'attack_radius': 45, 'notice_radius': 180},
	'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'../audio/attack/fireball.wav', 'speed': 1, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 30},
	'bamboo': {'health': 70,'exp':120,'damage':10,'attack_type': 'leaf_attack', 'attack_sound':'../audio/attack/slash.wav', 'speed': 2, 'resistance': 6, 'attack_radius': 30, 'notice_radius': 80},
    'small_raccoon': {'health': 70,'exp':100,'damage':10,'attack_type': 'slash', 'attack_sound':'../audio/attack/slash.wav', 'speed': 2, 'resistance': 6, 'attack_radius': 30, 'notice_radius': 80}
    }

