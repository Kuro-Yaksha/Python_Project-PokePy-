from pygame import *
from console import *
from os import path
import random
import pygame
import sys
pygame.init()

font = pygame.font.SysFont('sans', 32)


class Battle:
    def __init__(self):
        self.battle_playing = True
        self.player_health = 100
        self.opponent_health = 100
        self.player_poke_name = 'Charmender'
        self.opp_poke_name = 'Bulbasaur'
        self.scr = display.set_mode((1024, 768))
        self.scr.fill(LIGHTGREY)
        self.pokemon_list = ['Bulbasaur', 'Charmender', 'Squirtle', 'Pidgey', 'Pikachu', 'Onix']

    def AAfilledRoundedRect(self, surface, rect, color, radius=0.4):
        """
        AAfilledRoundedRect(surface,rect,color,radius=0.4)
        surface : destination
        rect    : rectangle
        color   : rgb or rgba
        radius  : 0 <= radius <= 1
        """
        rect = Rect(rect)
        color = Color(*color)
        alpha = color.a
        color.a = 0
        pos = rect.topleft
        rect.topleft = 0, 0
        rectangle = Surface(rect.size, SRCALPHA)
        circle = Surface([min(rect.size) * 3] * 2, SRCALPHA)
        draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
        circle = transform.smoothscale(circle, [int(min(rect.size) * radius)] * 2)
        radius = rectangle.blit(circle, (0, 0))
        radius.bottomright = rect.bottomright
        rectangle.blit(circle, radius)
        radius.topright = rect.topright
        rectangle.blit(circle, radius)
        radius.bottomleft = rect.bottomleft
        rectangle.blit(circle, radius)
        rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
        rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))
        rectangle.fill(color, special_flags=BLEND_RGBA_MAX)
        rectangle.fill((255, 255, 255, alpha), special_flags=BLEND_RGBA_MIN)
        return surface.blit(rectangle, pos)

    def draw_health_bar(self, health, x, y, w, h):
        if health > 75:
            col = GREEN
        elif health > 40:
            col = YELLOW
        else:
            col = RED
        width = int(w * health / 100)
        health_bar = Rect(x, y, width, h)
        draw.rect(self.scr, col, health_bar)

    def print_text(self, msg, x, y, colour):
        text = font.render(msg, True, colour)
        self.scr.blit(text, [x, y])

    def load_battle(self):
        self.opp_poke_name = random.choice(self.pokemon_list)
        game_folder = path.dirname(__file__)
        poke_folder = path.join(game_folder, 'Assets\Pokemon')

        bg_img = image.load(path.join(poke_folder, 'battle_background.png'))
        bg_img2 = image.load(path.join(poke_folder, 'dialogbox_background.png'))

        user_poke = image.load(path.join(poke_folder, self.player_poke_name + '_back.png'))
        opp_poke = image.load(path.join(poke_folder, self.opp_poke_name + '_front.png'))

        self.scr.blit(bg_img, (0, 0))  # loading background
        for i in range(0, 871, 290):  # loading lower background
            self.scr.blit(bg_img2, (i, 478))

        # loading black borders on dialog boxes
        self.AAfilledRoundedRect(self.scr, (20, 20, 470, 120), BLACK, 0.5)
        self.AAfilledRoundedRect(self.scr, (530, 340, 470, 120), BLACK, 0.5)
        self.AAfilledRoundedRect(self.scr, (5, 485, 1010, 270), BLACK, 0.3)

        # loading status boxes
        self.AAfilledRoundedRect(self.scr, (30, 30, 450, 100), WHITE, 0.5)
        self.AAfilledRoundedRect(self.scr, (540, 350, 450, 100), WHITE, 0.5)

        # printing details
        self.print_text(self.player_poke_name, 570, 360, BLACK)
        self.print_text(self.opp_poke_name, 60, 40, BLACK)

        # drawing health bars
        # opponent health bar
        self.AAfilledRoundedRect(self.scr, (196, 86, 258, 18), BLACK, 0.7)
        self.AAfilledRoundedRect(self.scr, (200, 90, 250, 10), LIGHTGREY, 0.5)
        self.draw_health_bar(self.opponent_health, 200, 90, 250, 10)

        # player health bar
        self.AAfilledRoundedRect(self.scr, (696, 406, 258, 18), BLACK, 0.7)
        self.AAfilledRoundedRect(self.scr, (700, 410, 250, 10), LIGHTGREY, 0.5)
        self.draw_health_bar(self.player_health, 700, 410, 250, 10)

        # loading pokemon sprites
        self.scr.blit(user_poke, (150, 478 - user_poke.get_height()))
        self.scr.blit(opp_poke, (700, 270 - opp_poke.get_height()))

        # loading main dialog box
        self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
        display.update()
        while event.wait().type != QUIT and self.opponent_health != 0 and self.player_health != 0 and pygame.event != pygame.K_ESCAPE:
           pass

    def battle_run(self):
        # game loop - set self.playing = False to end the game
        while self.battle_playing:
            self.battle_events()
            # self.update()
            # self.draw()

    def quit_battle(self):
        self.battle_playing = False

    def battle_events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_battle()

    def start_battle(self):
        self.load_battle()


'''obj = Battle()
obj.start_battle()'''
