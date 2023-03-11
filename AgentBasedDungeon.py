import pygame
from pygame import mixer

import random
import time

from win32api import GetSystemMetrics

SCR_WIDTH = GetSystemMetrics(0)
SCR_HEIGHT = GetSystemMetrics(1)

class Link:
    def __init__(self, screen, image, sword, sheet, x, y):
        self.screen = screen
        self.sprite = pygame.image.load(image)
        self.sheet = pygame.transform.scale(sheet, (600, 416))
        self.sword = sword
        self.x = x
        self.y = y
        self.dir = 0 # 0 - Down, 1 - Up, 2 - Right, 3 - Left

    def draw(self, attack_anim):
        if self.dir == 0:
            self.screen.blit(self.sheet, (self.x*40,self.y*40), (5, 6, 45, 46))
        elif self.dir == 1:
            self.screen.blit(self.sheet, (self.x*40,self.y*40), (5, 114, 45, 46))
        elif self.dir == 2:
            self.screen.blit(self.sheet, (self.x*40,self.y*40), (5, 60, 45, 46))
        elif self.dir == 3:
            self.screen.blit(self.sheet, (self.x*40,self.y*40), (5, 164, 45, 46))

        if attack_anim == 1:
            rotated_sword = pygame.transform.rotate(self.sword, 180)
            self.screen.blit(rotated_sword, (self.x*40+10, self.y*40+30))
        elif attack_anim == 2:
            rotated_sword = pygame.transform.rotate(self.sword, 158)
            self.screen.blit(rotated_sword, (self.x*40+10, self.y*40+30))
        elif attack_anim == 3:
            rotated_sword = pygame.transform.rotate(self.sword, 125)
            self.screen.blit(rotated_sword, (self.x*40+10, self.y*40+30))
        elif attack_anim == 4:
            rotated_sword = pygame.transform.rotate(self.sword, 103)
            self.screen.blit(rotated_sword, (self.x*40+10, self.y*40+30))
        elif attack_anim == 5:
            rotated_sword = pygame.transform.rotate(self.sword, 90)
            self.screen.blit(rotated_sword, (self.x*40+10, self.y*40+30))

    def move(self, direction):
        if direction == "north" and self.y > 0:
            self.y -= 1
        elif direction == "south" and self.y < SCR_HEIGHT // 40 - 1:
            self.y += 1
        elif direction == "east" and self.x < SCR_WIDTH // 40 - 1:
            self.x += 1
        elif direction == "west" and self.x > 0:
            self.x -= 1

    def attack(self, mob_list):
        for i in mob_list:
            if i[1] == link.y+1 and i[0] == link.x:
                mob_list.remove(i)
                break

def draw_grid(screen, wall, grid_square, link_list):
    
    skip = False
    for i in range(0, SCR_WIDTH // 40):
        for j in range(0, SCR_HEIGHT // 40):
            for pos in link_list:
                if pos == (i, j):
                    screen.blit(grid_square, (i*40, j*40))
                    skip = True
            if not skip:
                screen.blit(wall, (i*40, j*40))
            skip = False

def getRandomPos(link_list):
    i = random.randint(0, len(link_list)-1)
    return link_list[i]

pygame.init()
screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
mixer.init()
mixer.music.load("bgmusic.mp3")
mixer.music.set_volume(0.3)
#mixer.music.play()

grid_square = pygame.image.load("grid_square.jpg")
wall = pygame.image.load("wall.jpg")
link_sheet = pygame.image.load("link_sheet.png")
exit = pygame.image.load("exit.jpg")
chest = pygame.image.load("treasure.jpg")
mob = pygame.image.load("enemy.jpg")
sword = pygame.image.load("sword.jpg")

# Randomly place agent to start
x_pos = random.randint(0, SCR_WIDTH // 40)
y_pos = random.randint(0, SCR_HEIGHT // 40)
link = Link(screen, "link.jpg", sword, link_sheet, x_pos, y_pos)
link_list = [(link.x, link.y)] # Hah

dir = random.randint(0, 3)

dir_chance = 5
room_chance = 5

stochastic = False

if stochastic:
    if dir == 0:
        link.move("north")
    elif dir == 1:
        link.move("east")
    elif dir == 2:
        link.move("west")
    elif dir == 3:
        link.move("south")

    link_list.append((link.x, link.y))

    if random.randint(1, 100) > dir_chance:
        dir_chance += 5
    else:
        dir += random.randint(1, 3)
        dir %= 4
        dir_chance = 0

    if random.randint(1, 100) > room_chance:
        room_chance += 5
    else:
        room_width = random.randint(3, 7)
        room_height = random.randint(3, 7)
        
        left = (room_width - 1) // 2
        right = room_width - 1 - left
        up = (room_height - 1) // 2
        down = room_height - 1 - up
        for x in range(-left, right):
            for y in range(-up, down):
                link_list.append((link.x + x, link.y + y))
        room_chance = 0
else:
    for n in range(0, 30):
        room_built = False
        room_width = 7
        room_height = 7
        left = 3
        right = 4
        up = 3
        down = 4
        room_fits = True
        counter = 0
        for x in range(-left, right):
            for y in range(-up, down):
                if (link.x + x, link.y + y) in link_list and not (link.x, link.y) == (link.x + x, link.y + y):
                    counter += 1
                    if counter > 3:
                        room_fits = False

        if room_fits:
            room_width = random.randint(3, 7)
            room_height = random.randint(3, 7)
            
            left = (room_width - 1) // 2
            right = room_width - 1 - left
            up = (room_height - 1) // 2
            down = room_height - 1 - up
            for x in range(-left, right):
                for y in range(-up, down):
                    link_list.append((link.x + x, link.y + y))
            room_built = True

        if not room_fits:
            hall_fits = False
            while not hall_fits:
                dir = random.randint(0, 3)
                length = random.randint(4, 10)
                if dir == 0: # Up
                    if link.y - length >= 0:
                        hall_fits = True
                if dir == 1: # Down
                    if link.y + length < SCR_HEIGHT // 40 - 1:
                        hall_fits = True
                if dir == 2: # Right
                    if link.x + length < SCR_WIDTH // 40 - 1:
                        hall_fits = True
                if dir == 3: # Left
                    if link.x - length >= 0:
                        hall_fits = True

            for i in range(1, length+1):
                if dir == 0: # Up
                    link.y -= 1
                    link_list.append((link.x, link.y))
                if dir == 1: # Down
                    link.y += 1
                    link_list.append((link.x, link.y))
                if dir == 2: # Right
                    link.x += 1
                    link_list.append((link.x, link.y))
                if dir == 3: # Left
                    link.x -= 1
                    link_list.append((link.x, link.y))

start_pos = getRandomPos(link_list)
link.x = start_pos[0]
link.y = start_pos[1]
exit_pos = getRandomPos(link_list)
chest_pos = getRandomPos(link_list)
mob_pos = [getRandomPos(link_list) for i in range(0, 5)]

attack_anim = 0
old_time = time.time()
new_time = 0
accumulator = 0

key = False

running = True
while running:

    new_time = time.time()
    dt = new_time - old_time
    old_time = new_time
    accumulator += dt

    done = False

    draw_grid(screen, wall, grid_square, link_list)

    screen.blit(exit, (exit_pos[0]*40, exit_pos[1]*40))
    
    if key == False:
        screen.blit(chest, (chest_pos[0]*40, chest_pos[1]*40))

    for i in mob_pos:
        screen.blit(mob, (i[0]*40, i[1]*40))

    if (link.x, link.y) == (chest_pos):
        key = True

    

    link.draw(attack_anim)

    if attack_anim > 0:
        if accumulator > 0.1:
            attack_anim = (attack_anim + 1) % 6
            accumulator = 0

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_w:
                link.move("north")
                link.dir = 1
            elif event.key == pygame.K_a:
                link.move("west")
                link.dir = 2
            elif event.key == pygame.K_s:
                link.move("south")
                link.dir = 0
            elif event.key == pygame.K_d:
                link.move("east")
                link.dir = 3
            elif event.key == pygame.K_SPACE:
                if attack_anim == 0:
                    link.attack(mob_pos)
                    attack_anim = 1
                    accumulator = 0

    if (link.x, link.y) == (exit_pos):
        print("YOU WIN")
        running = False