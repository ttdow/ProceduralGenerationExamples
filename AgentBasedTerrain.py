import pygame
from pygame import mixer

import random
import numpy as np
from PIL import Image
import noise
import scipy.misc

from win32api import GetSystemMetrics

SCR_WIDTH = GetSystemMetrics(0)
SCR_HEIGHT = GetSystemMetrics(1)

# Creates the outline of the landmass.
# 1.) The agent subdivides the land area up to children agents.
# 2.) Each agent is assigned a seed point, a direction, and tokens to 'spend'
# 3.) If the seed point is already surrounded by land, it moves in direction until it find water.
# 4.) Once at the coast, the agent creates 2 points at random: an attractor and a repulsor in different directions.
# 5.) Agents score points (p) as follows:
#       d_r(p) - d_a(p) + 3d_e(p)
#           Where: d_a(p) is squared distance from p to attractor.
#                  d_r(p) is squared distance from p to repulsor.
#                  d_e(p) is the square of the closest distance from p to the edge of the map.
#     These terms encourage an agent to move towards the attractor, move away from the repulsor,
#     and to avoid the edges.
# 6.) Agents expand the landmass by adding points to the edges of the mass. The agent calculates
#     the score for all surrounding points that are not currently part of the landmass, and moves
#     to the the highest scoring point. This point is then elevated above sea level, becoming a part of the coastline.
class CoastlineAgent():
    def __init__(self, grid):

        side = random.randint(0, 3)
        x = 0
        y = 0
        
        if side == 0: # Top
            y = 0
            x = random.randint(0, SCR_WIDTH // 4 - 2)
        elif side == 1: # Bottom
            y = SCR_HEIGHT // 4 - 2
            x = random.randint(0, SCR_WIDTH // 4 - 2)
        elif side == 2: # Left
            x = 0
            y = random.randint(0, SCR_HEIGHT // 4 - 2)
        elif side == 3: # Right
            x = SCR_WIDTH // 4 - 2
            y = random.randint(0, SCR_HEIGHT // 4 - 2)
        
        self.seed_pos = grid[x][y]
        grid[x][y].elevation = 1
        self.dir = side + random.randint(1, 3) # 0 = Up, 1 = Down, 2 = Left, 3 = Right
        self.tokens = random.randint(1, 10)

    def __repr__(self) -> str:
        return "(" + str(self.seed_pos[0]) + ", " + str(self.seed_pos[1]) + ")"
    
    def draw(self, screen, img):
        screen.blit(img, self.seed_pos)

    def coastline_generate(self):
        # if self.tokens >= limit:
        #   create 2 children agents
        #   for child in children:
        #       child.seed_pos = random seed point on parent's border
        #       child.tokens = self.token // 2
        #       child.dir = random
        #       child.coastline_generate()
        # else:
        #   for token in self.tokens:
        #       point = random border point
        #       for n in point.neighbours:
        #           point.score
        #       point.state = land
        
        return 

class Cell():
    def __init__(self, x, y, state=0):
        self.x = x
        self.y = y
        self.elevation = state # 0 = Water, >= 1 = Land
    
    def __repr__(self) -> str:
        return "(" + str(self.x) + ", " + str(self.y) + "), Elevation: " + str(self.elevation)

def create_grid(grid):
    for x in range(0, SCR_WIDTH // 4 - 1):
        grid.append([])
        for y in range(0, SCR_HEIGHT // 4 - 1):
            grid[x].append(Cell(x, y))

def draw_grid(screen, grid, grid_square):
    for x in range(0, SCR_WIDTH // 4 - 1):
        for y in range(0, SCR_HEIGHT // 4 - 1):
            if grid[x][y].elevation > 0:
                screen.blit(grid_square, (x*4, y*4))

def main():
    pygame.init()
    screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
    mixer.init()
    mixer.music.load("bgmusic.mp3")
    mixer.music.set_volume(1.0)
    mixer.music.play()

    bg = pygame.transform.scale(pygame.image.load("wall.jpg"), (SCR_WIDTH, SCR_HEIGHT))
    pixel = pygame.transform.scale(pygame.image.load("grid_square.jpg"), (4, 4))

    grid = []
    create_grid(grid)

    #print((SCR_WIDTH // 4) * (SCR_HEIGHT // 4)) # 86400 cells

    #img = Image.fromarray(noise_array, "L")
    #img.save('noise.jpg')
    #img.show()

    #mike = CoastlineAgent(grid)

    running = True
    while running:

        screen.blit(bg, (0, 0))

        draw_grid(screen, grid, pixel)

        #mike.draw(screen, pixel)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

if __name__=='__main__':
    main()