from StartUp import giveInfo
from ProperCoords import *
import pygame

gameLevel = 1

screenW = giveInfo()[0]
screenH = giveInfo()[1]

standardUnit = screenW / 192
# On a 1920 by 1080 screen, a standardUnit is 10 pixels

def initPlatform(platform):
    newPlat = [0,0,0,0]
    for i in range(4):
        newPlat[i] = platform[i] * standardUnit
    return newPlat

ld = open('levelData.txt', 'r')
levelData = ld.read()
ld.close()
levels = levelData.split('----- NEW LEVEL -----')
numLevels = len(levels) - 1

def winZone(num):
    win = levels[num].split('\n')
    win = win[len(win) - 2]
    win = win.split('WIN: ')[1]
    win = eval(win)
    realWin = initPlatform(win)
    realWin[0], realWin[1] = toGameCoords(realWin[0], realWin[1], screenW, screenH)
    realWin = pygame.Rect(realWin[0], realWin[1], realWin[2], realWin[3])
    return realWin

def deathZone(num):
    death = levels[num].split('\n')
    death = death[len(death) - 3]
    death = death.split('DEATH: ')[1]
    death = int(int(death) * standardUnit)
    return death

def platformsOnLevel(num):
    platforms = levels[num].split('\n')
    platforms.pop(0)
    platforms.pop(len(platforms) -1)
    platforms.pop(len(platforms) -1)
    if len(platforms) > 1:
        platforms.pop(len(platforms) - 1)
    return platforms

testPlatforms = platformsOnLevel(gameLevel)
winArea = winZone(gameLevel)
deathArea = deathZone(gameLevel)

def makePlatformList(platList):
    newList = []
    for i in range(len(platList)):
        newList.append(0)
    for i in range(len(platList)):
        testPlatform= eval(platList[i])
        testPlatform = initPlatform(testPlatform)
        testPlatform[0], testPlatform[1] = toGameCoords(testPlatform[0], testPlatform[1], screenW, screenH)
        testPlatform = pygame.Rect(testPlatform[0], testPlatform[1], testPlatform[2], testPlatform[3])
        newList[i] = testPlatform
    return newList


platforms = makePlatformList(testPlatforms)

def levelUp():
    global gameLevel
    global testPlatforms
    global winArea
    global deathArea
    global platforms
    gameLevel += 1
    testPlatforms = platformsOnLevel(gameLevel)
    winArea = winZone(gameLevel)
    deathArea = deathZone(gameLevel)
    platforms = makePlatformList(testPlatforms)
    
def getWinDeath():
    return winArea, deathArea


def getPlatforms():
    return platforms
