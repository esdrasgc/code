from platform import platform
import pygame as pg

pg.init()
pg.mixer.init()

# Sounds

GAME_SONG = pg.mixer.Sound('game_song.mp3')
MOB_DEATH_SOUND = pg.mixer.Sound('mob_death.mp3')
MOB_DEATH_SOUND.set_volume(0.3)
PLAYER_DEATH_SOUND = pg.mixer.Sound('player_death.mp3')

# game options/settings
TITLE = "Dive or Die"
WIDTH = 800
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'

# Player properties

PLAYER_IMG = pg.image.load('player.png')
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 50

PLAYER_SHOT_DELAY = 150
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12



# Mob properties
MOB_ACC = 0.4
MOB_FRICTION = -0.1
MOB_WIDTH = 40
MOB_HEIGHT = 40
MOB_REPULSION = 0.1
MOB_IMG = pg.image.load('magikarp.png')
MOB_IMG_SCALED = pg.transform.scale(MOB_IMG, (MOB_WIDTH, MOB_HEIGHT))

# Projectile properties

PROJECTILE_FRICTION = -0.12
PROJECTILE_ACC = 0.6
PROJECTILE_WIDTH = 12
PROJECTILE_HEIGHT = 12
PROJECTILE_IMG = pg.image.load('pokeball.png')
PROJECTILE_IMG_SCALED = pg.transform.scale(PROJECTILE_IMG, (PROJECTILE_WIDTH, PROJECTILE_HEIGHT))

# define colors
WHITE = (255, 255, 255)
ORANGE = (212, 114, 17)
BLACK = (10, 10, 10)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE

# Images
BACKGROUND1_IMG = pg.image.load('underwater.jpg')
BACKGROUND1_HEIGHT = 1536
BACKGROUND2_IMG = pg.image.load('back.jpg')
BACKGROUND2_IMG_SCALED = pg.transform.scale(BACKGROUND2_IMG, (WIDTH, HEIGHT))


# plataforms properties
PLATAFORM_HEIGHT = 20
PLATAFORM_IMG = pg.image.load('platform.png')

# TREASUREs properties
TREASURE_WIDTH = 15
TREASURE_HEIGHT = 25
TREASURE_IMG = pg.image.load('coin.png')
TREASURE_IMG_SCALED = pg.transform.scale(TREASURE_IMG, (TREASURE_WIDTH, TREASURE_HEIGHT))

## input text configs
COLOR_INACTIVE = WHITE #pg.Color('lightskyblue3')
COLOR_ACTIVE = (0, 100, 20) #pg.Color('dodgerblue2')
# FONT = pg.font.Font('arial', 32)