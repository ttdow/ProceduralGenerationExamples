import pygame
from pygame import mixer

import random

from win32api import GetSystemMetrics

SCR_WIDTH = GetSystemMetrics(0)
SCR_HEIGHT = GetSystemMetrics(1)

class Link():
    def __init__(self, screen, x, y):
        self.screen = screen
        self.sprite_sheet = pygame.transform.scale(pygame.image.load("link_sheet.png"), (600, 416))
        self.x = x
        self.y = y
        self.dir = 'south'

    def draw(self):
        if self.dir == 'south':
            self.screen.blit(self.sprite_sheet, (self.x*40,self.y*40), (5, 6, 45, 46))
        elif self.dir == 'north':
            self.screen.blit(self.sprite_sheet, (self.x*40,self.y*40), (5, 114, 45, 46))
        elif self.dir == 'east':
            self.screen.blit(self.sprite_sheet, (self.x*40,self.y*40), (5, 164, 45, 46))
        elif self.dir == 'west':
            self.screen.blit(self.sprite_sheet, (self.x*40,self.y*40), (5, 60, 45, 46))

    def move(self, dir):
        if dir == "north" and self.y > 0:
            self.y -= 1
        elif dir == "south" and self.y < SCR_HEIGHT // 40 - 1:
            self.y += 1
        elif dir == "east" and self.x < SCR_WIDTH // 40 - 1:
            self.x += 1
        elif dir == "west" and self.x > 0:
            self.x -= 1

        self.dir = dir

class Cell():
    def __init__(self, x, y, state=0):
        self.x = x
        self.y = y
        self.state = state # 0 = Free, 1 = Rock
        self.wall = False
    
    def __repr__(self) -> str:
        return "(" + str(self.x) + ", " + str(self.y) + "), State: " + str(self.state)

def create_grid(grid):
    for x in range(0, SCR_WIDTH // 40 - 1):
        grid.append([])
        for y in range(0, SCR_HEIGHT // 40 - 1):
            grid[x].append(Cell(x, y))

def seed_rocks(grid):
    for x in range(0, SCR_WIDTH // 40 - 1):
        for y in range(0, SCR_HEIGHT // 40 - 1):
            coin_toss = random.randint(0, 1)
            if coin_toss == 1:
                grid[x][y].state = 1

def draw_grid(screen, grid, grid_square):
    for x in range(0, SCR_WIDTH // 40 - 1):
        for y in range(0, SCR_HEIGHT // 40 - 1):
            if grid[x][y].state == 0:
                screen.blit(grid_square, (x*40, y*40))

def cellular_automaton(grid):

    # Make new grid for output
    new_grid = []
    create_grid(new_grid)

    for x in range(0, SCR_WIDTH // 40 - 2):
        for y in range(0, SCR_HEIGHT // 40 - 2):
            # Get Moore neighbourhood
            n = Cell(0, 0, 1)
            s = Cell(0, 0, 1)
            e = Cell(0, 0, 1)
            w = Cell(0, 0, 1)
            nw = Cell(0, 0, 1)
            ne = Cell(0, 0, 1)
            se = Cell(0, 0, 1)
            sw = Cell(0, 0, 1)

            if x > 0:
                w = grid[x-1][y]
                if y > 0:
                    nw = grid[x-1][y-1]
                if y < (SCR_HEIGHT // 40 - 1):
                    sw = grid[x-1][y+1]
            if x < (SCR_WIDTH // 40 - 1):
                e = grid[x+1][y]
                if y > 0:
                    ne = grid[x+1][y-1]
                if y < (SCR_HEIGHT // 40 - 1):
                    se = grid[x+1][y+1]
            if y > 0:
                n = grid[x][y-1]
            if y < (SCR_HEIGHT // 40 -1):
                s = grid[x][y+1]
            
            # Put updated states in new grid
            moore_value = w.state + nw.state + ne.state + e.state + n.state + s.state + sw.state + se.state
            if moore_value > 4:
                new_grid[x][y].state = 1
            else:
                new_grid[x][y].state = 0

    return new_grid

def main():
    pygame.init()
    screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
    mixer.init()
    mixer.music.load("bgmusic.mp3")
    mixer.music.set_volume(0.3)

    grid_square = pygame.image.load("grid_square.jpg")
    rock = pygame.transform.scale(pygame.image.load("wall.jpg"), (SCR_WIDTH, SCR_HEIGHT))

    grid = []
    create_grid(grid)
    seed_rocks(grid)

    link = Link(screen, 0, 0)

    running = True
    while running:

        screen.blit(rock, (0,0))

        draw_grid(screen, grid, grid_square)

        link.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_w:
                    link.move("north")
                elif event.key == pygame.K_a:
                    link.move("west")
                elif event.key == pygame.K_s:
                    link.move("south")
                elif event.key == pygame.K_d:
                    link.move("east")
                elif event.key == pygame.K_SPACE:
                    grid = cellular_automaton(grid)

if __name__=='__main__':
    main()