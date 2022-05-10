### sources:
### https://github.com/kidscancode/pygame_tutorials
### https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame
### https://github.com/Insper/pygame-snippets

from turtle import right
import pygame as pg
import random
from settings import *
from sprites import *
import json


class InputBox:
    """
    Class that creates an InputBox 
    Its used in the start game screen so the player can write its name
    """
    def __init__(self,fo, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = fo.render(text, True, self.color)
        self.active = False
        self.fo = fo

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    return self.text 
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.fo.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)



class Game:
    """"
    Class that contains the whole game.
    It contains all the structures needed for a game, like gameloop, update, draw and others functions.
    """
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.game_over = False
        self.load_data()

    
    def load_data(self):
        """
        function to load the data of the highscores.json
        """
        try:
            with open('highscores.json') as json_file:
                self.scores = json.load(json_file)
                print(self.scores)
        except:
            self.scores = {"1° Lugar" : {"---":0},"2° Lugar" : {"---":0},"3° Lugar" : {"---":0},"4° Lugar" : {"---":0},"5° Lugar" : {"---":0},"6° Lugar" : {"---":0},"7° Lugar" : {"---":0},"8° Lugar" : {"---":0},"9° Lugar" : {"---":0},"10° Lugar" : {"---":0}}

    def new(self):
        """
        Function of new game
        here all the variables that should be reseted to a new game are created (or reseted)
        """
        # start a new game
        self.score = 0
        self.now_screen = Screen_underwater(self.screen, self)
        self.back_layer = Backgorund_layer(self.screen, self)
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.projectiles = pg.sprite.Group()#
        self.treasures = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.last_shot = pg.time.get_ticks()
        self.shooting = False
        pg.mixer.music.load('game_song.mp3')
        self.run()

    def run(self):
        """
        Function with the game loop
        """
        pg.mixer.music.play(loops=-1)
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        """
        Function that updates all the game sprites 
        The self.alls_sprites contains all the sprites and the .update() in a group of sprites calls all the update methods
        from all the class sprites contained in the group.
        It also has a hole in the generation of new sprites, like the mobs, plataforms and coins.
        """
        # Game Loop - Updatessssssss
        self.all_sprites.update()
        self.now_screen.update()
        


        # Generate mobs
        while len(self.mobs) < 2 + int(self.now_screen.pos.y/(-500)):
            choice = random.randint(0,1)
            if choice == 0:
                bottom = random.randrange(HEIGHT, HEIGHT + 40)
                top = random.randrange(-40, 0)
                mob = Mob(random.randrange(0, WIDTH), random.choice([bottom, top]), self)
                self.mobs.add(mob)
                self.all_sprites.add(mob)
            else:
                right = -40
                left = WIDTH + 40
                mob = Mob(random.choice([right, left]), random.randrange(0, HEIGHT), self)
                self.mobs.add(mob)
                self.all_sprites.add(mob)

        
        # # if player reaches top 1/4 of screen
        # if self.player.rect.top <= HEIGHT / 4:
        #     self.player.pos.y += abs(self.player.vel.y)

        #     # change the value of the position vector of the screen so the backgroun can be scrooled
        #     self.now_screen.pos.y += abs(self.player.vel.y)

        #     # movement the plataforms and kill the ones that are far away
        #     for plat in self.platforms:
        #         plat.rect.y += abs(self.player.vel.y)
        #         if plat.rect.top >= HEIGHT:
        #             plat.treasure.kill()
        #             plat.kill()

        #     # spawn new platforms from the BOTTOM to keep same average number
        #     while len(self.platforms) < 1:
        #         width = random.randrange(75, 100)
        #         p = Platform(random.randrange(0, WIDTH - width),
        #                     random.randrange(-50, 0),
        #                     width, self)
        #         self.platforms.add(p)
        #         self.all_sprites.add(p)

        
        
        # if player reaches the 1/4 bottom of screen
        if self.player.rect.bottom >= 3*HEIGHT / 4:
            self.player.pos.y -= abs(self.player.vel.y)

            # change the value of the position vector of the screen so the backgroun can be scrooled
            self.now_screen.pos.y -= abs(self.player.vel.y)
            self.back_layer.pos.y -= abs(self.player.vel.y)

            # movement the plataforms and kill the ones that are far away
            for plat in self.platforms:
                plat.rect.y -= abs(self.player.vel.y)
                if plat.rect.bottom <= 0:
                    plat.treasure.kill()
                    plat.kill()

            # spawn new platforms from the BOTTOM to keep same average number
            while len(self.platforms) < 1:
                width = random.randrange(75, 100)
                plat_img = pg.transform.scale(PLATAFORM_IMG, (width, PLATAFORM_HEIGHT))
                p = Platform(plat_img ,random.randrange(0, WIDTH - width),
                            random.randrange(HEIGHT, HEIGHT + 50),
                            width, self)
                self.platforms.add(p)
                self.all_sprites.add(p)

    def events(self):
        """
        get the player actions and respond to it
        """
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                self.shooting = True
                
            if event.type == pg.MOUSEBUTTONUP:
                self.shooting = False

            if event.type == pg.MOUSEMOTION:

                if self.shooting:
                    now = pg.time.get_ticks()
                    if (now - self.last_shot) > PLAYER_SHOT_DELAY:
                        self.last_shot = now
                        mouse_pos = event.pos
                        p = Projectile(self,mouse_pos,self.player.pos.x,self.player.pos.y)
                        self.projectiles.add(p)
                        self.all_sprites.add(p)

            if event.type == pg.KEYDOWN and event.key == pg.K_s and self.game_over:
                self.screen.fill(BGCOLOR)

                self.draw_text("To Restart the game, any key",18,WHITE,WIDTH/2, HEIGHT*3/5)

                self.wait_for_space()

                pg.display.flip()

    def draw(self):
        """
        draw the screen while the game is running (the start screen and in boat screen their own metods to draw in the screen)
        """
        # Game Loop - draw
        self.screen.fill(BLACK)
        # back_posy = int(self.back_layer.pos.y * (-1)) % HEIGHT
        self.screen.blit(self.back_layer.image, (0, int(self.back_layer.pos.y) % HEIGHT))
        self.screen.blit(self.back_layer.image, (0, int(self.back_layer.pos.y) % HEIGHT - HEIGHT))
        #self.screen.blit(self.now_screen.image, self.now_screen.pos)
        self.draw_text('score: '+str(self.score), 14, BLACK, (WIDTH - 40), (30))
        self.draw_text('deeps: ' + str(int(self.now_screen.pos.y / (-10))), 14, BLACK, (WIDTH - 40), (45))
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()
  
    def show_start_screen(self):
        """
        Screen that appers only one time
        Its the first screen, where the player puts its name and see the instructions of the game
        """
        # game splash/start screen
        
        fo = pg.font.Font(self.font_name, 30)
        box_width = WIDTH/4
        input_box = InputBox(fo,WIDTH/2 - box_width/2, 3*HEIGHT/4, WIDTH/4, HEIGHT/15)
        done = False
        clock = pg.time.Clock()
        while not done:
            for event in pg.event.get():
                self.screen.fill(BGCOLOR)
                
                self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
                self.draw_text("WASD to move, aim with the mouse and shot with the left mouse button", 22, WHITE, WIDTH / 2, HEIGHT / 2)
                self.draw_text('Enter with your name.', 22, WHITE, WIDTH/2, 2*HEIGHT/3)
                
                if event.type == pg.QUIT:
                    done = True
                self.player_name = input_box.handle_event(event)
                input_box.update()
                input_box.draw(self.screen)
                if isinstance(self.player_name, str):
                    done = True

            pg.display.flip()
            clock.tick(30)
        # self.player_name = 'josias'
        pg.display.flip()
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 5 / 6)
        pg.display.flip()
        self.wait_for_key()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def in_boat_screen(self):
        """
        Screen that appears after the player loose.
        It shows the option to see the scoreboard or play again
        """
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)


        x = self.scoreboard(self.score,self.player_name)

        while x != 0:
            x = self.scoreboard(x,self.player_name)

        self.game_over = True

        self.draw_text(f"Your score was {self.score}",24,WHITE,WIDTH/2,HEIGHT / 2)
        self.draw_text("To check today's Scoreboard, press (S)",18,WHITE,WIDTH/2, HEIGHT*3/5)

        self.draw_text("Press space to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_space()
        self.wait_for_space()
        self.game_over = False
        pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def wait_for_space(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN and event.key == pg.K_s and self.game_over:           
                    self.screen.fill(BGCOLOR)                  
                    h = 40
                    n = 1

                    for position in self.scores:
                        self.draw_text(f"{n}°Lugar : {self.scores[position]}",18, WHITE, WIDTH / 2, h)
                        h += 40
                        n += 1

                    self.draw_text("To Restart the game, press space.",18,WHITE,WIDTH/2, HEIGHT - 80)
                    self.draw_text("AWSD to move. mouse buttons to fire!",18,WHITE,WIDTH/2, HEIGHT - 50)
                    waiting = False

                    pg.display.flip()
                if (event.type == pg.KEYUP) and (event.key == pg.K_SPACE):
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def scoreboard(self,P_score,name):      
        for position in self.scores:
            for nome in self.scores[position]:
                valor = self.scores[position][nome]
                if valor < P_score:
                    s = valor
                    self.scores[position] = {name : P_score}
                    return s             
        return 0

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.in_boat_screen()

# the json file where the output must be stored 
out_file = open("highscores.json", "w") 
json.dump(g.scores, out_file, indent = 6)
out_file.close() 
pg.quit()
