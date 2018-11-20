import math
from ProperCoords import *
from Level import getPlatforms, getWinDeath
from StartUp import giveInfo

gravity = -9.8 # FINAL, in m/s^2
airResist = 0.9998 # FINAL in percentage

screenW = giveInfo()[0] # FINAL
screenH = giveInfo()[1] # FINAL
frameCap = giveInfo()[2] # FINAL
# Meter to pixel conversions found using Spider-Man taking up 1/16 of a 1920 by 1080 screen, and he is 1.74 m tall
meterToPixel = ((1/16) * screenH)  / 1.74 # FINAL
pixelToMeter = 1/meterToPixel # FINAL

velocityAngleRatio = 0.5 # FINAL
gravityAngleInfluence = 0.1 # FINAL
webIncrease = (screenW / 96) * math.sqrt(2) # length of web increase per frame
webPerFrame = 1 # number of times the game checks for connection per frame

wrongSideAnglePenalty = 0.5 # FINAL

winArea, deathArea = getWinDeath()

platforms = getPlatforms()

def refreshLevel():
    global winArea
    global deathArea
    winArea, deathArea = getWinDeath()
    global platforms
    platforms = getPlatforms()

def velToAngle(velocity, direction):
    #angle = velocity * velocityAngleRatio
    if velocity >=  0:
        angle = math.pow(velocity, velocityAngleRatio)
        if angle > 5:
            angle = 5
        if direction == 'Left':
            angle *= wrongSideAnglePenalty
    else:
        velocity *= -1
        angle = math.pow(velocity, velocityAngleRatio)
        angle *= -1
        if angle < -5:
            angle = -5
        if direction == 'Right':
            angle *= wrongSideAnglePenalty
    return angle

def angleToVel(angle):
    velocity = angle * (1/velocityAngleRatio)
    return velocity

class Web:
    def __init__(self, x1, y1):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1
        self.y2 = y1
        self.length = 0
        self.isConnected = False
        self.angle = 0

    def testConnection(self):
        i = 0
        while i < len(platforms)  and not self.isConnected:
            
            if platforms[i].collidepoint(toGameCoords(self.x2, self.y2, screenW, screenH)):
                self.isConnected = True
            else:
                self.isConnected = False
            i += 1
            
    def addLength(self, magnitude):
        self.length = self.length + magnitude
        self.x2 = self.x1 + (self.length * math.cos(self.angle))
        self.y2 = self.y1 + (self.length * math.sin(self.angle))

    def updatePos(self, x, y):
        self.x1 = x
        self.y1 = y
    def trueLength(self):
        return self.length

def circleDeriv(angle, anglePerFrame, r):
    angle1 = angle
    angle2 = angle + anglePerFrame
    angle1 = math.radians(angle1)
    angle2 = math.radians(angle2)
    x1 = r * math.cos(angle1)
    x2 = r * math.cos(angle2)
    y1 = r* math.sin(angle1)
    y2 = r * math.sin(angle2)

    xVelocity = ((x2 - x1) * pixelToMeter)  * frameCap # because it divides by 1/frameCap, which is multiplying by the frameCap
    yVelocity = ((y2 - y1) * pixelToMeter)  * frameCap

    xVelocity /= 1.75
    yVelocity /= 1.75
    
    return xVelocity, yVelocity

def getAngle(x2, y2):
    angle = 0
    (x1, y1) = (screenW/2, screenH/2)
    if y1 > y2: # QUAD 1 and 2
        angle = abs((math.pi / 2) - math.atan((x2 - x1) / (y1 - y2)))
    elif y2 > y1: # QUAD 3 and 4
        angle = 0 - abs((math.pi / 2) - math.atan((x2 - x1) / (y2 - y1)))
    return angle


class Player:
    def __init__(self, suit, key): # Initializes the player object
        self.suit = suit # suit is the outfit Spider-Man is wearing
        self.key = key # key is the keystroke that shoots out webs
        self.x = -500 # in pixels
        self.y = -100 # in pixels
        self.xVelocity = 10 # in m/s
        self.yVelocity = 10 # in m/s
        self.isShootingWeb= False
        self.isSwinging = False
        self.anglePerFrame = 0 # in degrees
        self.angle = 0 # in degrees
        self.web = Web(self.x, self.y)
        self.isDead = False
        self.hasWon = False
        self.costume = 'Falling'
        self.mouseX = 0
        self.mouseY = 0
        self.direction = 'Right'

    def swing(self, r):
        if self.angle > 90 and self.angle < 270: # Left side on circle
            self.anglePerFrame += gravityAngleInfluence
        elif self.angle < 270 or self.angle > 90 : # Right side on circle
            self.anglePerFrame -= gravityAngleInfluence
        self.angle += self.anglePerFrame
        if self.angle >= 360:
            self.angle -= 360
        if self.angle < 0:
            self.angle += 360
        radAngle = math.radians(self.angle)
        relativeX = r * math.cos(radAngle)
        relativeY = r * math.sin(radAngle)
        self.x = self.web.x2 + relativeX
        self.y = self.web.y2 + relativeY

    def physics(self):
        self.yVelocity += (gravity) * (1/frameCap)
        self.xVelocity *= airResist
        self.x += meterToPixel * (self.xVelocity * (1/frameCap))
        self.y += meterToPixel * (self.yVelocity * (1/frameCap))

    def doActions(self):
        self.gameX, self.gameY = toGameCoords(self.x, self.y, screenW, screenH)
        # Direction
        if self.mouseX < screenW/2:
            self.direction = 'Left'
        else:
            self.direction = 'Right'

        
        # Win / Lose Conditions
        if self.y < deathArea:
            self.isDead = True
        if winArea.collidepoint(self.gameX, self.gameY):
            self.hasWon = True
            
        if self.isSwinging:
            self.costume = 'Swinging'
            if self.isShootingWeb:
                # print('SWINGING')
                self.swing(self.web.trueLength())
                self.web.updatePos(self.x, self.y)
            else:
                self.isSwinging = False
                self.xVelocity, self.yVelocity = circleDeriv(self.angle, self.anglePerFrame, self.web.trueLength())
                self.web.isConnected = False
                
        elif self.isShootingWeb:
            if self.web.angle == 'None':
                self.web.angle = getAngle(self.mouseX, self.mouseY)
            self.costume = 'Swinging'
            self.physics()
            self.web.updatePos(self.x, self.y)
            for i in range(webPerFrame):
                self.web.addLength(webIncrease / webPerFrame)
                self.web.testConnection()
                if self.web.isConnected:
                    i = webPerFrame + 1
                    self.isSwinging = True
                    self.anglePerFrame = velToAngle(self.xVelocity, self.direction)
                    self.angle = 180 + math.degrees(self.web.angle)
        else:
            self.web.angle = 'None'
            self.costume = 'Falling'
            self.web.length = 0
            self.physics()


    def giveDisplayInfo(self, width, height):
        x, y = self.gameX, self.gameY
        x1, y1 = toGameCoords(self.web.x1, self.web.y1, screenW, screenH)
        x2, y2 = toGameCoords(self.web.x2, self.web.y2, screenW, screenH)
        return x, y, x1, y1, x2, y2, self.isShootingWeb, self.costume
        
        
