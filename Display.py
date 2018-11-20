import pygame, math
from StartUp import giveInfo
from Level import getPlatforms, getWinDeath

screenW = giveInfo()[0]
screenH = giveInfo()[1]

winArea = getWinDeath()[0]

midX= int(screenW/2 + .5)
midY= int(screenH/2 + .5)

allPlatforms = getPlatforms()

def refreshPlatforms():
    global winArea
    global allPlatforms
    winArea = getWinDeath()[0]
    allPlatforms = getPlatforms()

playerWidth = int((1920 / 64) + 0.5)
playerHeight = int((1080 / 16) + 0.5)

webMidX = midX + playerWidth

red = (255,0,0)
black = (0,0,0)
white = (255,255,255)
grey = (54, 58, 63)

falling = pygame.image.load('spiderman1.png')
swinging = pygame.image.load('spiderman2.png')
webhair = pygame.image.load('webhair.png')
windowsActivated = False

def display(screen, info, mouseX, mouseY):
    playerX = int(info[0] + 0.5)
    playerY = int(info[1] + 0.5)
    webX1 = int(info[2] + 0.5)
    webY1 = int(info[3] + 0.5)
    webX2 = int(info[4] + 0.5)
    webY2 = int(info[5] + 0.5)
    showWeb = info[6]
    costume = info[7]
    if costume == 'Falling':
        costume = falling
    elif costume == 'Swinging':
        costume = swinging

    for i in range(len(allPlatforms)):
        actualPlatform = allPlatforms[i].copy()
        actualPlatform[0] = allPlatforms[i][0] + (midX - playerX)
        actualPlatform[1] = allPlatforms[i][1] + (midY - playerY)
        if actualPlatform[0] < screenW and actualPlatform[1] < screenH:
            building = actualPlatform.copy()
            building[3] = allPlatforms[i][3] + screenH - building[1]
            pygame.draw.rect(screen, grey, building, 0)
            
        if windowsActivated:
            for x in range(0, 10):
                window = actualPlatform.copy()
                window[0] += 50
                window[1] += 100 + x * 250
                window[2] = allPlatforms[i][2] / 2 - 75
                window[3] = 200
                window2 = actualPlatform.copy()
                window2[0] += allPlatforms[i][2] / 2 + 25
                window2[1] += 100 + x * 250
                window2[2] = allPlatforms[i][2] / 2 - 75
                window2[3] = 200
                pygame.draw.rect(screen, white, window, 0)
                pygame.draw.rect(screen, white, window2, 0)
        pygame.draw.rect(screen, black, actualPlatform, 0)

    actualWin = winArea.copy()
    actualWin[0] = winArea[0] + (midX - playerX)
    actualWin[1] = winArea[1] + (midY - playerY)
    
    pygame.draw.rect(screen, red, actualWin, 0) # win zone

    screen.blit(costume, (midX - playerWidth, midY)) # player
    screen.blit(webhair, (mouseX - 15, mouseY - 15)) # crosshair
    # pygame.draw.circle(screen, red, (midX, midY), playerHeight, 0)
   # pygame.draw.circle(screen, red, (playerX, playerY), playerHeight, 0)

    if showWeb:
        pygame.draw.line(screen, white, (midX, midY),(webX2 + (midX - playerX), webY2 + (midY - playerY)), 2)
