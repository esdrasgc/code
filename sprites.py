# Sprite classes for platform game
from asyncio.windows_events import NULL
import pygame as pg
from settings import *
vec = pg.math.Vector2


def plataform_collision(sprite_obj):
    """
    Function to apply movement and check if there is a collision with a plataform
    As you can see, the movement its applied in one direction than in the other (first vertical than horizontal).
    """

    ### Update the vertical position 
    sprite_obj.pos.y += int(sprite_obj.vel.y + 0.5 * sprite_obj.acc.y)
    sprite_obj.mask.rect.centery = sprite_obj.pos.y
    ## Check for vertical collisions
    # colision with plataforms

    hits = pg.sprite.spritecollide(sprite_obj.mask, sprite_obj.game.platforms, False)

    if hits:
        if type(sprite_obj) == Projectile:
            sprite_obj.kill()
        else:
            ## Check for collision in the bottom of the plataform (and top of the player)
            if sprite_obj.vel.y < 0:
                sprite_obj.acc.y = 0
                sprite_obj.vel.y = 0
                sprite_obj.pos.y = hits[0].rect.centery + (PLATAFORM_HEIGHT + sprite_obj.height)/2 + 1  ## return to a position where there is no colission
            
            ## Check for collision in the top of the plataform (and bottom of the player)
            if sprite_obj.vel.y > 0:
                sprite_obj.acc.y = 0
                sprite_obj.vel.y = 0
                sprite_obj.pos.y = hits[0].rect.centery - (PLATAFORM_HEIGHT + sprite_obj.height)/2 - 1  ## return to a position where there is no colission

    sprite_obj.mask.rect.centery = sprite_obj.pos.y
    ### Update the horizontal position 
    sprite_obj.pos.x += int(sprite_obj.vel.x + 0.5 * sprite_obj.acc.x)

    ## Limit the horizontal boundaries of the screen (so the player can vanish from the screen)

    if sprite_obj.pos.x < sprite_obj.width/2:
        if type(sprite_obj) == Projectile:
            sprite_obj.kill()
        sprite_obj.acc.x = 0
        sprite_obj.vel.x = 0
        sprite_obj.pos.x = (sprite_obj.width/2) + 1

    if sprite_obj.pos.x > WIDTH - (sprite_obj.width/2):
        if type(sprite_obj) == Projectile:
            sprite_obj.kill()
        sprite_obj.acc.x = 0
        sprite_obj.vel.x = 0
        sprite_obj.pos.x = WIDTH - (sprite_obj.width/2) - 1
    ## Check for horizontal collisions

    sprite_obj.mask.rect.centerx = sprite_obj.pos.x

    # colision with plataforms
    hits = pg.sprite.spritecollide(sprite_obj.mask, sprite_obj.game.platforms, False)

    if hits:
        if type(sprite_obj) == Projectile:
            sprite_obj.kill()
        ## colision with the right side of the plataform
        if sprite_obj.vel.x < 0:
            sprite_obj.acc.x = 0
            sprite_obj.vel.x = 0
            sprite_obj.pos.x = hits[0].rect.centerx + (sprite_obj.width + hits[0].getWidth())/2 + 1

        if sprite_obj.vel.x > 0:
            sprite_obj.acc.x = 0
            sprite_obj.vel.x = 0
            sprite_obj.pos.x = hits[0].rect.centerx - (sprite_obj.width + hits[0].getWidth())/2 - 1

    sprite_obj.mask.rect.centerx = sprite_obj.pos.x
    sprite_obj.rect.center = sprite_obj.pos

class Treasure(pg.sprite.Sprite):
    """
    Class of the coins that appears above the plataforms
    """
    def __init__(self, platform, game):
        self.groups = game.all_sprites, game.treasures
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = platform
        self.image = TREASURE_IMG_SCALED
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.centery = self.plat.rect.centery - (TREASURE_HEIGHT + PLATAFORM_HEIGHT)/2


    def update(self):
        self.rect.centery = self.plat.rect.centery - (TREASURE_HEIGHT + PLATAFORM_HEIGHT)/2

class Mask(pg.sprite.Sprite):
    """
    Class to create masks to be used in the collisions of the game
    """
    def __init__(self, obj):
        pg.sprite.Sprite.__init__(self)
        self.surface = pg.Surface((obj.width, obj.height))
        self.rect = self.surface.get_rect()
        self.rect.center = obj.rect.center

class Screen():
    def __init__(self, screen, game):
        self.width = WIDTH
        self.height = HEIGHT
        self.screen = screen
        self.game = game


class Backgorund_layer(Screen):
    """
    Class that contains the second background (the infinite one)
    """
    def __init__(self, screen, game):
        super().__init__(screen, game)
        self.image = BACKGROUND2_IMG_SCALED
        self.pos = vec(0,0)

class Screen_underwater(Screen):
    """
    Class that contains the first backgorund and some of the game informations
    """
    def __init__(self, screen, game):
        super().__init__(screen, game)
        self.image = BACKGROUND1_IMG
        self.pos = vec(0,0)

    def update(self):
        if self.pos.y > BACKGROUND1_HEIGHT - HEIGHT/2:
            self.image = BACKGROUND2_IMG_SCALED

class Projectile(pg.sprite.Sprite):
    """
    Class to create the 'pokeballs' that the player shoots
    """
    def __init__(self,game,mouse_pos,x,y):
        pg.sprite.Sprite.__init__(self)
        self.width = PROJECTILE_WIDTH
        self.height = PROJECTILE_HEIGHT
        self.image = PROJECTILE_IMG_SCALED
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.pos = vec(x, y) #vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.mask = Mask(self)
        self.game = game
        self.mouse = vec(mouse_pos)
        direct = self.mouse - self.pos
        self.direction = direct.normalize()
        
    def update(self):

        self.acc = self.direction * PROJECTILE_ACC 

        hits = pg.sprite.spritecollide(self.mask, self.game.mobs, False)
        if hits:
            MOB_DEATH_SOUND.play()
            hits[0].kill()
            self.kill()
        hits = pg.sprite.spritecollide(self.mask, self.game.platforms, False)
        if hits:
            self.kill()

        # apply friction
        self.acc += self.vel * PROJECTILE_FRICTION
        # equations of motion
        self.vel += self.acc
        plataform_collision(self)

class Player(pg.sprite.Sprite):
    """
    Class to create the player
    """
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.height = PLAYER_HEIGHT
        self.width = PLAYER_WIDTH
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect()

        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.mask = Mask(self)
        self.game = game

    def update(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_w]:
            self.acc.y = -PLAYER_ACC
        if keys[pg.K_s]:
            self.acc.y = PLAYER_ACC

        # apply friction

        self.acc += self.vel * PLAYER_FRICTION
        # update the velocity
        self.vel += self.acc

        if self.rect.centery <= PLAYER_HEIGHT:
            if self.vel.y < 0:
                self.rect.centery = PLAYER_HEIGHT + 1
                self.vel.y = 0
                self.acc.y = 0

        plataform_collision(self)
        self.check_for_mob_collision()
        self.check_for_treasure_collision()


        self.mask.rect.centerx = self.pos.x
        self.rect.center = self.pos

    def check_for_mob_collision(self):
        hits = pg.sprite.spritecollide(self.mask, self.game.mobs, False)
        if hits:
            PLAYER_DEATH_SOUND.play()
            self.game.playing = False

    def check_for_treasure_collision(self):
        hits = pg.sprite.spritecollide(self.mask, self.game.treasures, False)
        if hits:
            self.game.score += 1
            hits[0].kill()

    def getPos(self):
        return self.pos

class Platform(pg.sprite.Sprite):
    """
    Class to create the plataforms where the player, mob and projectiles collide with
    Also is where the treasures are spawned.
    """
    def __init__(self,plat_img, x, y, w, game):
        pg.sprite.Sprite.__init__(self)
        self.image = plat_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = w
        self.game = game
        self.treasure = Treasure(self, self.game)

    def getWidth(self):
        return self.width

class Mob(pg.sprite.Sprite):
    """
    Class to create the mobs (magikarp) that kills the player
    """
    def __init__(self, x, y, game):
        pg.sprite.Sprite.__init__(self)
        self.width = MOB_WIDTH
        self.height = MOB_HEIGHT
        self.image = MOB_IMG_SCALED
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(x, y) #vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.mask = Mask(self)
        self.game = game

    def update(self):
        posPlayer = self.game.player.getPos()
        self.acc = posPlayer - self.pos
        self.acc = self.acc.normalize() * MOB_ACC
        hits = pg.sprite.spritecollide(self.mask, self.game.mobs, False)
        if hits:
            other_mob = hits[0]
            repulsion_acc = self.pos - other_mob.pos
            self.acc += repulsion_acc * MOB_REPULSION

        # apply friction
        self.acc += self.vel * MOB_FRICTION
        # equations of motion
        self.vel += self.acc
        
        plataform_collision(self)

        self.rect.center = self.pos

    def getPos(self):
        return self.pos