import pygame
from pygame import mixer

import random

import matplotlib.pyplot as plt

from win32api import GetSystemMetrics

SCR_WIDTH = GetSystemMetrics(0)
SCR_HEIGHT = GetSystemMetrics(1)

def create_grid(grid):
    return

def perlinNoise1D(n, seed, octaves, bias):
    fOutput = list()

    for i in range(0, n):
        fNoise = 0.0
        fScale = 1.0
        fScaleAcc = 0.0
        for k in range(0, octaves):
            nPitch = n // (2**k)
            nSample1 = int((i / int(nPitch)) * int(nPitch))
            nSample2 = int((int(nSample1) + int(nPitch)) % n)

            fBlend = float(i - nSample1) / float(nPitch)
            fSample = (1.0 - fBlend) * seed[nSample1] + fBlend * seed[nSample2]
            fNoise += fSample * fScale
            fScaleAcc += fScale

            fScale /= bias

        fOutput.append(fNoise / fScaleAcc)

    return fOutput

def perlinNoise2D(width, seed, octaves, bias):
    fOutput = [[None] * 512] * 512

    print("Octaves: " + str(octaves))

    for i in range(0, width):
        for k in range(0, width):
            fNoise = 0.0
            fScale = 1.0
            fScaleAcc = 0.0
            for j in range(0, octaves):
                nPitch = width // (2**j)

                nSampleX1 = int((i / int(nPitch)) * int(nPitch))
                nSampleY1 = int((k / int(nPitch)) * int(nPitch))

                nSampleX2 = int((int(nSampleX1) + int(nPitch)) % width)
                nSampleY2 = int((int(nSampleY1) + int(nPitch)) % width)

                fBlendX = float(i - nSampleX1) / float(nPitch)
                fBlendY = float(k - nSampleY1) / float(nPitch)

                fSampleT = (1.0 - fBlendX) * seed[nSampleX1][nSampleY1] + fBlendX * seed[nSampleX2][nSampleY1]
                fSampleB = (1.0 - fBlendX) * seed[nSampleX1][nSampleY2] + fBlendX * seed[nSampleX2][nSampleY2]

                fScaleAcc += fScale
                fNoise += (fBlendY * (fSampleB - fSampleT) + fSampleT) * fScale
                fScale /= bias

            fOutput[i][k] = fNoise / fScaleAcc

    print(str(fOutput[10][10]))

    return fOutput
    
def draw_noise(noise, screen, w_pixel, g_pixel):

    i_ctr = 0
    j_ctr = 0
    for i in noise:
        for j in i:
            if j > 0.5:
                screen.blit(w_pixel, (i_ctr*2, j_ctr*2))
            elif j > 0.1:
                screen.blit(g_pixel, (i_ctr*2, j_ctr*2))
            j_ctr += 1
        i_ctr += 1
        j_ctr = 0
    return

def noise_avg(noise):
    sum = 0
    for i in noise:
        for j in i:
            sum += j
    
    print(sum / 512**2)

def main():
    pygame.init()
    screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
    mixer.init()
    mixer.music.load("bgmusic.mp3")
    mixer.music.set_volume(1.0)
    mixer.music.play()

    bg = pygame.transform.scale(pygame.image.load("wall.jpg"), (SCR_WIDTH, SCR_HEIGHT))
    w_pixel = pygame.transform.scale(pygame.image.load("w_square.jpg"), (2,2))
    g_pixel = pygame.transform.scale(pygame.image.load("g_square.jpg"), (2,2))
    grid = []
    create_grid(grid)

    # Create 1D Perlin noise
    #fNoiseSeed1D = [None] * 256

    #for i in range(0, 256):
    #    fNoiseSeed1D[i] = random.random()

    #pNoise = perlinNoise1D(256, fNoiseSeed1D, 6, 2.0)

    # Create 2D Perlin noise
    fNoiseSeed2D = [[None] * 512] * 512
    for i in range(0, 512):
        for j in range(0, 512):
            fNoiseSeed2D[i][j] = random.random()

    octaves = 1
    noise = perlinNoise2D(512, fNoiseSeed2D, octaves, 2.0)

    running = True
    while running:
        screen.blit(bg, (0,0))

        draw_noise(noise, screen, w_pixel, g_pixel)
        #noise_avg(noise)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_DOWN:
                    octaves += 1
                    #print(octaves)
                    noise = perlinNoise2D(512, fNoiseSeed2D, octaves, 2.0)

                

if __name__=='__main__':
    main()