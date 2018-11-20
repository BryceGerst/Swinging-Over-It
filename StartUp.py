import pygame, time, sys

# Reads the settings text file
s = open('settings.txt', 'r')
settings = s.read()
s.close()
settingsList = settings.split('\n')
width = int(settingsList[0].split(' ')[1])
height = int(settingsList[1].split(' ')[1])
fullscreen = settingsList[2].split(' ')[1]
fps = int(settingsList[3].split(' ')[1])

def giveInfo():
    return width, height, fps

def refreshScreen(screen, clock, frameCap):
    pygame.display.update()
    screen.fill((160,220,235))
    clock.tick(frameCap)

def start():
    if fullscreen:
        screen = pygame.display.set_mode([width, height], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode([width, height])
    clock = pygame.time.Clock()
    return screen, clock, fps
    
