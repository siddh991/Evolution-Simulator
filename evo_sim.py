import pygame
import neat
import time
import os
import random
from scipy.spatial import distance

WIN_WIDTH = 800
WIN_HEIGHT = 600

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Evolution Simulator")

bot_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bot.png")), (25, 25))
food_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","food.png")), (10, 10))

class Bot:
    BOT_IMG = bot_img

    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.vel = 1
        self.hunger = 10
        self.direction = dir

        if self.direction == 3:
            self.img = pygame.transform.flip(self.BOT_IMG, True, False)
        else:
            self.img = self.BOT_IMG

    def up(self):
        self.y -= self.vel
        self.direction = 0
    def right(self):
        self.x += self.vel
        self.direction = 1
    def down(self):
        self.y += self.vel
        self.direction = 2
    def left(self):
        self.x -= self.vel
        self.direction = 3

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

        if c_point:
            return True
        
        return False

def draw_window(win, bots, food):
    win.fill((255,255,255))
    
    for bot in bots:
        bot.draw(win)

    for f in food:
        f.draw(win)

    pygame.display.update()

def find_closest_food(curr_x, curr_y, food):
    p1 = (curr_x, curr_y)
    distance_to_food = []

    for x, f in enumerate(food):
        p2 = (f.x, f.y)
        distance_to_food.append(distance.euclidean(p1, p2))
    
    return  distance_to_food.index(min(distance_to_food))

def main(genomes, config):
    nets = []
    ge = []
    #bots = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        ge.append(g)

    bots_x_a = ([10] * 5)
    bots_x_b = ([740] * 5) 
    bots_y_a = random.sample(range(10, 550), 5)
    bots_y_b = random.sample(range(10, 550), 5)

    food_x = random.sample(range(100, 700), 10)
    food_y = random.sample(range(100, 500), 10)

    bots = []
    food = []

    for i in range(len(bots_x_a)):
        bots.append(Bot(bots_x_a[i], bots_y_a[i], 1))

    for i in range(len(bots_x_b)):
        bots.append(Bot(bots_x_b[i], bots_y_b[i], 3))

    for i in range(len(food_x)):
        food.append(Food(food_x[i], food_y[i]))

    score = 0

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    win.fill((255,255,255))

    clock = pygame.time.Clock()

    run = True

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        for x, bot in enumerate(bots):
            index_closest_food = find_closest_food(bot.x, bot.y, food)
            output = nets[bots.index(bot)].activate((bot.x, bot.y, food[index_closest_food].x, food[index_closest_food].y))
            
            if output[0] > 0.5:
                bot.up()
            if output[1] > 0.5:
                bot.right()
            if output[2] > 0.5:
                bot.down()
            if output[3] > 0.5:
                bot.left()

            print("output: ")
            print(output)

        for x, bot in enumerate(bots):
            for y, f in enumerate(food):
                if f.collide(bot):
                    ge[x].fitness += 1
                    food.pop(y)

        draw_window(win, bots, food)


#main()

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
    neat.DefaultSpeciesSet, neat.DefaultStagnation, 
    config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-nn.txt")
    run(config_path)