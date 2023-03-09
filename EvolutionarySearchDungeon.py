import pygame
from pygame import mixer
from PIL import Image
import math
import random
import time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import sys

class Link():
    def __init__(self, row, col, imgPath):
        self.pos = [row, col]
        self.sprite = pygame.image.load(imgPath)

class Gannon():
    def __init__(self, row, col, imgPath):
        self.pos = [row, col]
        self.sprite = pygame.image.load(imgPath)

class Cell():
    def __init__(self, row, col):
        self.col = col
        self.row = row
        self.name = str(row) + str(col)

        self.x = row * 40
        self.y = col * 40

        self.connections = []

        self.blocked = False

    def setConnections(self, connections):
        self.connections = connections

class Board():
    def __init__(self):
        self.grid = [[Cell(0, 0), Cell(0, 1), Cell(0, 2), Cell(0, 3), Cell(0, 4), Cell(0, 5), Cell(0, 6), Cell(0, 7), Cell(0, 8), Cell(0, 9)],
                     [Cell(1, 0), Cell(1, 1), Cell(1, 2), Cell(1, 3), Cell(1, 4), Cell(1, 5), Cell(1, 6), Cell(1, 7), Cell(1, 8), Cell(1, 9)],
                     [Cell(2, 0), Cell(2, 1), Cell(2, 2), Cell(2, 3), Cell(2, 4), Cell(2, 5), Cell(2, 6), Cell(2, 7), Cell(2, 8), Cell(2, 9)],
                     [Cell(3, 0), Cell(3, 1), Cell(3, 2), Cell(3, 3), Cell(3, 4), Cell(3, 5), Cell(3, 6), Cell(3, 7), Cell(3, 8), Cell(3, 9)],
                     [Cell(4, 0), Cell(4, 1), Cell(4, 2), Cell(4, 3), Cell(4, 4), Cell(4, 5), Cell(4, 6), Cell(4, 7), Cell(4, 8), Cell(4, 9)],
                     [Cell(5, 0), Cell(5, 1), Cell(5, 2), Cell(5, 3), Cell(5, 4), Cell(5, 5), Cell(5, 6), Cell(5, 7), Cell(5, 8), Cell(5, 9)],
                     [Cell(6, 0), Cell(6, 1), Cell(6, 2), Cell(6, 3), Cell(6, 4), Cell(6, 5), Cell(6, 6), Cell(6, 7), Cell(6, 8), Cell(6, 9)],
                     [Cell(7, 0), Cell(7, 1), Cell(7, 2), Cell(7, 3), Cell(7, 4), Cell(7, 5), Cell(7, 6), Cell(7, 7), Cell(7, 8), Cell(7, 9)],
                     [Cell(8, 0), Cell(8, 1), Cell(8, 2), Cell(8, 3), Cell(8, 4), Cell(8, 5), Cell(8, 6), Cell(8, 7), Cell(8, 8), Cell(8, 9)],
                     [Cell(9, 0), Cell(9, 1), Cell(9, 2), Cell(9, 3), Cell(9, 4), Cell(9, 5), Cell(9, 6), Cell(9, 7), Cell(9, 8), Cell(9, 9)]]
        
        # Corners
        self.grid[0][0].setConnections([self.grid[0][1], self.grid[1][0]])
        self.grid[0][9].setConnections([self.grid[0][8], self.grid[1][9]])
        self.grid[9][0].setConnections([self.grid[8][0], self.grid[9][1]])
        self.grid[9][9].setConnections([self.grid[8][9], self.grid[9][8]])

        # Top row
        for i in range(1, 8+1):
            self.grid[0][i].setConnections([self.grid[0][i-1], self.grid[0][i+1], self.grid[1][i]])

        # Bottom row
        for i in range(1, 8+1):
            self.grid[9][i].setConnections([self.grid[9][i-1], self.grid[9][i+1], self.grid[8][i]])

        # Left column
        for i in range(1, 8+1):
            self.grid[i][0].setConnections([self.grid[i-1][0], self.grid[i+1][0], self.grid[i][1]])

        # Right column
        for i in range(1, 8+1):
            self.grid[i][9].setConnections([self.grid[i-1][9], self.grid[i+1][9], self.grid[i][8]])

        # Interior columns
        for i in range(1, 8+1):
            for j in range(1, 8+1):
                self.grid[i][j].setConnections([self.grid[i][j-1], self.grid[i][j+1], self.grid[i-1][j], self.grid[i+1][j]])

def detectGridPos(pos):
    row = 0
    col = 0

    if pos[0] > 200:
        if pos[0] > 320:
            if pos[0] > 360:
                col = 9
            else:
                col = 8
        else:
            if pos[0] > 280:
                col = 7
            elif pos[0] > 240:
                col = 6
            else:
                col = 5
    else:
        if pos[0] > 120:
            if pos[0] > 160:
                col = 4
            else:
                col = 3
        else:
            if pos[0] > 80:
                col = 2
            elif pos[0] > 40:
                col = 1
            else:
                col = 0

    if pos[1] > 200:
        if pos[1] > 320:
            if pos[1] > 360:
                row = 9
            else:
                row = 8
        else:
            if pos[1] > 280:
                row = 7
            elif pos[1] > 240:
                row = 6
            else:
                row = 5
    else:
        if pos[1] > 120:
            if pos[1] > 160:
                row = 4
            else:
                row = 3
        else:
            if pos[1] > 80:
                row = 2
            elif pos[1] > 40:
                row = 1
            else:
                row = 0

    return (row, col)

class Pathfinder():
    def __init__(self, grid):
        self.grid = grid
        self.currentPath = []

    def sortFrontier(self, frontier):
        return sorted(frontier, key=lambda x:x[1])
    
    def hCost(self, src, dest):
        pos = (int(src[0]), int(src[1]))

        x = dest.row - pos[0]
        y = dest.col - pos[1]

        x = abs(x)
        y = abs(y)

        return x + y
    
    def backtrack(self, dest, path):
        parent = dest.name

        while True:
            if parent == None:
                break
            
            self.currentPath.append(parent)
            
            try:
                parent = path[parent]
            except:
                print("No path available!")
                return

    def findPath(self, src, dest):
        frontier = []
        frontier.append([src.name, 0])
        frontier = self.sortFrontier(frontier)

        came_from = dict()
        cost_so_far = dict()
        came_from[src.name] = None
        cost_so_far[src.name] = 0

        while len(frontier) != 0:
            current = frontier[0]
            del frontier[0]

            if current[0] == dest.name:
                break

            pos = (int(current[0][0]), int(current[0][1]))

            for i in self.grid[pos[0]][pos[1]].connections:
                new_cost = cost_so_far[current[0]] + 1

                if i.blocked:
                    continue

                if i.name not in cost_so_far or new_cost < cost_so_far[i.name]:
                    cost_so_far[i.name] = new_cost
                    priority = new_cost + self.hCost(i.name, dest)
                    frontier.append([i.name, priority])
                    came_from[i.name] = current[0]

        self.backtrack(dest, came_from)

# -----------------------------------------------------------------------------

# Perturb the copied dungeons slightly to induce diversity in the population
def mutateDungeons(dungeons, bad_dungeons):
    
    #print("mutateDungeons()")
    dungeons, fitness_list, _, _ = evaluateDungeons(dungeons)
    dungeons, sorted_list = sortDungeons(dungeons, fitness_list)

    # Mutate the replacement dungeons
    for i in range(0, int(len(sorted_list) / 2)):
        for j in range(0, 10):
            for k in range(0, 10):
               
                #print(sorted_list[-i-1][0])

                coin_toss = random.randint(0, 1)
                if coin_toss:

                    roll_dice = random.randint(0, 19)
                    if roll_dice > 17:
                        dungeons[sorted_list[-i-1][0]][j][k] = 5 # Treasure
                    elif roll_dice > 15:
                        dungeons[sorted_list[-i-1][0]][j][k] = 4 # Monster
                    elif roll_dice > 7:
                        dungeons[sorted_list[-i-1][0]][j][k] = 1 # Wall
                    else:
                        dungeons[sorted_list[-i-1][0]][j][k] = 0 # Free space

    #print("mutated")
    #_, fitness_list, _, _ = evaluateDungeons(dungeons)
                    
        #new_dungeons.append(np.random.randint(6, size=(10, 10), dtype=np.uint8))

    # Overwrite the bad dungeons with new dungeons
    #for i in range(0, len(bad_dungeons)):
        #dungeons[bad_dungeons[i]] = new_dungeons[i]

    return dungeons

# Replace the removed dungeons with copies of the best dungeons
def reproduceDungeons(dungeons, good_dungeons, bad_dungeons):

    #print("reproduceDungeons()")
    _, fitness_list, _, _ = evaluateDungeons(dungeons)

    for i in range(0, len(bad_dungeons)):
        dungeons[bad_dungeons[i]] = dungeons[good_dungeons[i]]

    return dungeons, bad_dungeons

# Remove the worst lambda dungeons
def cullDungeons(dungeons, fitness_list):

    #print("cullDungeons()")
    _, fitness_list, _, _ = evaluateDungeons(dungeons)

    good_dungeons = []
    bad_dungeons = []

    half_len = int(len(fitness_list) / 2)

    for i in range(0, half_len):
        good_dungeons.append(fitness_list[i][0])
    
    for i in range(len(fitness_list) - half_len, len(fitness_list)):
        bad_dungeons.append(fitness_list[i][0])

    return dungeons, good_dungeons, bad_dungeons

# Sort dungeons by fitness
def sortDungeons(dungeons, fitness_list):

    #print("sortDungeons()")
    #_, fitness_list, _, _ = evaluateDungeons(dungeons)

    sorted_list = sorted(fitness_list, key = lambda x: x[1], reverse=True)

    return dungeons, sorted_list

# Evaluation function for dungeons
def evaluateDungeons(dungeons):

    largest_fitness = 0
    fitness_sum = 0
    fitness_list = []
    counter = 0

    for dungeon in dungeons:
        fitness = 0
        unique, counts = np.unique(dungeon, return_counts=True)
        
        if len(unique) < 6:
            fitness = -250
        else:
            if counts[2] > 1:
                fitness -= 100
            
            if counts[3] > 1:
                fitness -= 100

            if counts[0] > counts[1]:
                fitness += 25

            if counts[4] > counts[5] or counts[5] > counts[4]:
                fitness -= 25
            else:
                fitness += 25

        for i in range(0, dungeon.shape[0]-1):
            for j in range(0, dungeon.shape[1]-1):
                if dungeon[i, j] == 0 and dungeon[i, j+1] == 0:
                    fitness += 5
                elif dungeon[i,j] == 0 and dungeon[i+1, j] == 0:
                    fitness += 5

                if dungeon[i, j] == 1 and dungeon[i, j+1] == 1:
                    fitness += 5
                elif dungeon[i,j] == 1 and dungeon[i+1, j] == 1:
                    fitness += 5

                if dungeon[i, j] == 0 and \
                dungeon[i, j+1] == 0 and \
                dungeon[i+1, j] == 0 and \
                dungeon[i+1,j+1] ==0:
                    fitness += 50
        
        fitness_list.append((counter, fitness))
        counter += 1
        fitness_sum += fitness

        if fitness > largest_fitness:
            largest_fitness = fitness

    avg_fitness = fitness_sum / 100
    #print("Avg. Fitness of Dungeons: ", avg_fitness)

    #print(largest_fitness)

    return dungeons, fitness_list, avg_fitness, largest_fitness

# TODO optional
def shuffleDungeons():
    print()

def makeDungeon():
    dim = 10
    number = 100

    # 0 = free space
    # 1 = wall
    # 2 = starting point
    # 3 = exit
    # 4 = monster
    # 5 = treasure
    dungeons = []

    # Make 100 random 'dungeons'
    for i in range(0, number):
        dungeons.append(np.random.randint(6, size=(dim, dim), dtype=np.uint8))
    
    # For graphing progress of algorithm
    avg_fitness_list = []
    largest_fitness_list = []

    for i in range(0, 100):
        #print("Iteration: ", i)
        dungeons, fitness_list, avg_fitness, largest_fitness = evaluateDungeons(dungeons)
        dungeons, sorted_list = sortDungeons(dungeons, fitness_list)
        dungeons, good_dungeons, bad_dungeons = cullDungeons(dungeons, sorted_list)
        dungeons, bad_dungeons = reproduceDungeons(dungeons, good_dungeons, bad_dungeons)
        dungeons = mutateDungeons(dungeons, bad_dungeons)
        avg_fitness_list.append(avg_fitness)
        largest_fitness_list.append(largest_fitness)

    dungeons, fitness_list, avg_fitness, largest_fitness = evaluateDungeons(dungeons)
    dungeons, sorted_list = sortDungeons(dungeons, fitness_list)

    avg_fitness_list.append(avg_fitness)
    largest_fitness_list.append(largest_fitness)

    #print(sorted_list)

    #plt.plot(largest_fitness_list)
    #plt.show()

    #plt.plot(avg_fitness_list)
    #plt.show()

    return dungeons[sorted_list[0][0]]

    #np.set_printoptions(threshold=sys.maxsize)
    #print(dungeons[sorted_list[0][0]])

oldTime = time.time()

# Start display
pygame.init()
screen = pygame.display.set_mode((400, 400))

# Start audio
mixer.init()
mixer.music.load("bgmusic.mp3")
mixer.music.set_volume(0.3)
mixer.music.play()
mixer.music.pause()
mute = True

link = Link(0, 0, "link.jpg")
gannon = Gannon(9, 9, "enemy.jpg")

bgd = pygame.image.load("grid.jpg")
rock = pygame.image.load("rock.jpg")
door = pygame.image.load("exit.jpg")
chest = pygame.image.load("treasure.jpg")
rocks = []
chests = []
mobs = []
exit_pos = (9, 9)

running = True
doAStar = True

board = Board()
path = Pathfinder(board.grid)

dungeon_layout = makeDungeon()
for i in range(0, 10):
    for j in range(0, 10):
        if dungeon_layout[i][j] == 1: # Wall
            board.grid[i][j].blocked = True
            rocks.append((i, j))
        elif dungeon_layout[i][j] == 2: # Starting point
            link.pos[0] = i
            link.pos[1] = j
        elif dungeon_layout[i][j] == 3: # Exit
            exit_pos = (i, j)
        elif dungeon_layout[i][j] == 4: # Monster
            mobs.append((i, j))
        elif dungeon_layout[i][j] == 5: # Treasure
            chests.append((i, j))
        
# Main game loop
while running:

    step = False

    # Wait for user movement
    while step == False:

        if mute:
            mixer.music.pause()
        else:
            mixer.music.unpause()

        screen.blit(bgd, (0, 0))
        screen.blit(link.sprite, (link.pos[1] * 40, link.pos[0] * 40))
        screen.blit(gannon.sprite, (gannon.pos[1] * 40, gannon.pos[0] * 40))
        screen.blit(door, (exit_pos[1] * 40, exit_pos[0] * 40))

        for i in chests:
            screen.blit(chest, (i[1] * 40, i[0] * 40))

        for i in rocks:
            screen.blit(rock, (i[1] * 40, i[0] * 40))

        for i in mobs:
            screen.blit(gannon.sprite, (i[1] * 40, i[0] * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                step = True

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                pos = detectGridPos(pos)
                if pos not in rocks:
                    rocks.append(pos)
                    board.grid[pos[0]][pos[1]].blocked = True
                else:
                    rocks.remove(pos)
                    board.grid[pos[0]][pos[1]].blocked = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    step = True

                if event.key == pygame.K_w:
                    link.pos[0] -= 1

                    if link.pos[0] < 0:
                        link.pos[0] += 1

                    if board.grid[link.pos[0]][link.pos[1]].blocked:
                        link.pos[0] += 1
                    
                    step = True

                if event.key == pygame.K_s:
                    link.pos[0] += 1

                    if link.pos[0] > 9:
                        link.pos[0] -= 1

                    if board.grid[link.pos[0]][link.pos[1]].blocked:
                        link.pos[0] -= 1

                    step = True

                if event.key == pygame.K_d:
                    link.pos[1] += 1

                    if link.pos[1] > 9:
                        link.pos[1] -= 1
                    
                    if board.grid[link.pos[0]][link.pos[1]].blocked:
                        link.pos[1] -= 1

                    step = True

                if event.key == pygame.K_a:
                    link.pos[1] -= 1

                    if link.pos[1] < 0:
                        link.pos[1] += 1

                    if board.grid[link.pos[0]][link.pos[1]].blocked:
                        link.pos[1] += 1

                    step = True

                if event.key == pygame.K_m:
                    mute = not mute

                if event.key == pygame.K_f:
                    path.findPath()

                if event.key == pygame.K_SPACE:
                    step = True
    
    if doAStar:
        path.currentPath.clear()
        path.findPath(board.grid[gannon.pos[0]][gannon.pos[1]], board.grid[link.pos[0]][link.pos[1]])
        if len(path.currentPath) > 1:
            gannonMove = path.currentPath[len(path.currentPath)-2]
            gannon.pos = (int(gannonMove[0]), int(gannonMove[1]))