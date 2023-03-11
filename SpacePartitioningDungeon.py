import pygame
from pygame import mixer

import random

from win32api import GetSystemMetrics

SCR_WIDTH = GetSystemMetrics(0)
SCR_HEIGHT = GetSystemMetrics(1)

open_space = []

class Scene:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Link:
    def __init__(self, screen, image, x, y):
        self.screen = screen
        self.sprite = pygame.image.load(image)
        self.x = x
        self.y = y

    def draw(self):
        self.screen.blit(self.sprite, (self.x*40,self.y*40))

    def move(self, direction):
        if direction == "north":
            self.y -= 1
        elif direction == "south":
            self.y += 1
        elif direction == "east":
            self.x += 1
        elif direction == "west":
            self.x -= 1

# A point located at (x, y) in 2D space
class Point:
    def __init__(self, x, y, node=None):
        self.x = x
        self.y = y
        self.node = node

    def __repr__(self) -> str:
        return ("(" + str(self.x) + ", " + str(self.y) + ")")

# A rectangle centered at (cx, cy) with width w and heigh h
class Rect:
    def __init__(self, cx, cy, w, h):
        self.cx = cx
        self.cy = cy
        self.w = w
        self.h = h
        self.west_edge = cx - w / 2
        self.east_edge = cx + w / 2
        self.north_edge = cy - h / 2
        self.south_edge = cy + h / 2

    def __repr__(self) -> str:
        return "(" + str(self.cx) + ", " + str(self.cy) + "), Width: " + str(self.w) + ", Height: " + str(self.h)

    # Is point inside this rect?
    def contains(self, point):
        if isinstance(point, Point):
            point_x = point.x
            point_y = point.y
        else:
            point_x = point[0]
            point_y = point[1]

        return (point_x >= self.west_edge and
                point_x < self.east_edge and
                point_y >= self.north_edge and
                point_y < self.south_edge)

class QuadTree:
    def __init__(self, boundary, max_points=4, depth=0, parent=None):
        self.boundary = boundary
        self.max_points = max_points
        self.point = []
        self.depth = depth
        self.leaves = []
        self.parent = parent
        self.room = False
        self.found = None

        # A flag to indicate whether this node has divided
        self.divided = False

    def __repr__(self) -> str:
        return str(self.boundary) + ", Depth: " + str(self.depth) + "\n"

    # Divide this node by spawning four children
    def divide(self):

        cx = self.boundary.cx

        cy = self.boundary.cy

        w = self.boundary.w / 2
        h = self.boundary.h / 2

        # Make quadrants
        self.nw = QuadTree(Rect(cx - w/2, cy - h/2, w, h), self.max_points, self.depth + 1, self)
        self.ne = QuadTree(Rect(cx + w/2, cy - h/2, w, h), self.max_points, self.depth + 1, self)
        self.se = QuadTree(Rect(cx + w/2, cy + h/2, w, h), self.max_points, self.depth + 1, self)
        self.sw = QuadTree(Rect(cx - w/2, cy + h/2, w, h), self.max_points, self.depth + 1, self)

        self.divided = True

    def getLeaves(self, root):

        if self.divided == False:

            # Decide randomly if this leaf is a room
            if random.randint(0, 1):
                self.room = True

            root.leaves.append(self)
        else:
            self.nw.getLeaves(root)
            self.ne.getLeaves(root)
            self.sw.getLeaves(root)
            self.se.getLeaves(root)

    def query(self, point):

        if self.boundary.contains(point):
            if self.divided == True:
                self.nw.query(point)
                self.ne.query(point)
                self.se.query(point)
                self.sw.query(point)
            else:
                if self.room:
                    open_space.append(Point(point.x - 20, point.y - 20))

def draw_grid(screen, wall):
    for i in range(0, SCR_WIDTH // 40):
        for j in range(0, SCR_HEIGHT // 40):
            screen.blit(wall, (i*40, j*40))

pygame.init()
screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
mixer.init()
mixer.music.load("bgmusic.mp3")
mixer.music.set_volume(0.3)
#mixer.music.play()

Scene(SCR_WIDTH // 40, SCR_HEIGHT // 40)

grid_square = pygame.image.load("grid_square.jpg")
wall = pygame.image.load("wall.jpg")
link = Link(screen, "link.jpg", (SCR_WIDTH // 40) / 2, (SCR_HEIGHT // 40) / 2)
rock = pygame.image.load("rock.jpg")

#print(SCR_WIDTH)
#print(SCR_HEIGHT)
#print(SCR_WIDTH // 40)
#print(SCR_HEIGHT // 40)

qt = QuadTree(Rect(SCR_WIDTH / 2, SCR_HEIGHT / 2, SCR_WIDTH, SCR_HEIGHT))

n_divisions = random.randint(10, 20)
for n in range(0, n_divisions):

    # Reset to root of tree
    tree_pointer = qt

    # Loop until you randomly traverse to a lowest depth
    while tree_pointer.divided == True:

        quadrant = random.randint(0, 3)

        if quadrant == 0:
            tree_pointer = tree_pointer.nw
        elif quadrant == 1:
            tree_pointer = tree_pointer.ne
        elif quadrant == 2:
            tree_pointer = tree_pointer.se
        elif quadrant == 3:
            tree_pointer = tree_pointer.sw

    # Divide the node to go deeper
    tree_pointer.divide()

qt.getLeaves(qt)

#print(qt.leaves)

rooms = []
for leaf in qt.leaves:
    if leaf.room == True:
        rooms.append(leaf)

tree_pointer = qt
i = 20
j = 20
while i < SCR_WIDTH:
    while j < SCR_HEIGHT:
        qt.query(Point(i, j))
        j += 40
    i += 40
    j = 20

#print(open_space)

running = True
while running:

    draw_grid(screen, wall)  

    for space in open_space:
        #img = pygame.transform.scale(grid_square, (space.boundary.w, room.boundary.h))
        screen.blit(grid_square, (space.x, space.y))

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