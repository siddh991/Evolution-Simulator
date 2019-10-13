import pygame
import neat
import time
import os
import random

WIN_WIDTH = 800
WIN_HEIGHT = 600

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Evolution Simulator")

bot_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bot.png")), (50, 50))
food_img = pygame.image.load(os.path.join("imgs","food.png"))

class Bot:
    BOT_IMG = bot_img

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 1
        self.img = self.BOT_IMG
        
    def up(self):
        self.y -= self.vel
    def down(self):
        self.y += self.vel
    def left(self):
        self.x -= self.vel
    def right(self):
        self.x += self.vel

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Food:
    FOOD_IMG = food_img

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f_img = self.FOOD_IMG

    def draw(self, win):
        win.blit(self.f_img, (self.x, self.y))
    
    def collide(self, bot):
        bot_mask = bot.get_mask()
        food_mask = pygame.mask.from_surface(self.f_img)

        food_offset = (self.x - bot.x, self.y - round(bot.y))
        
        c_point = bot_mask.overlap(food_mask, food_offset)

def draw_window(win, bot):
    bot.draw(win)
    pygame.display.update()

def main():
    bot = Bot(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    win.fill((255,255,255))
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
        draw_window(win, bot)
    
    pygame.quit()
    quit()


main()