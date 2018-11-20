from StartUp import *
from Player import *
import Display
import Level
pygame.init()

black = (0,0,0) # FINAL
white = (255,255,255) # FINAL

screen, clock, fps = start()

readUserInput = True

def isPressed(key):
    if key == 'ESCAPE':
        key = 27
    elif key == 'SPACE':
        key = 32
    elif key == 'MOUSEDOWN':
        return pygame.mouse.get_pressed()[0]
    return pygame.key.get_pressed()[key]


player = Player('Regular' , 'MOUSEDOWN')
playing = True
pygame.mixer.music.load('Spider-Man_Movie_Theme_1.mp3')
pygame.mixer.music.set_volume(0.02)
pygame.mixer.music.play(-1)

victory = pygame.mixer.Sound('Pizza_Time.ogg')
defeat = pygame.mixer.Sound('Youre_Trash_Brock.ogg')

pygame.mouse.set_visible(False)



while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or isPressed('ESCAPE'):
            playing = False

    if player.isDead:
        # readUserInput = False
        # playing = False
        player = Player('Regular', 'MOUSEDOWN')
        player.hasWon = False
        defeat.play()
    elif player.hasWon:
        # readUserInput = False
        # playing = False
        victory.play()
        player = Player('Regular', 'MOUSEDOWN')
        player.hasWon = False
        if not Level.gameLevel < Level.numLevels:
            Level.gameLevel = 0
        Level.levelUp()
        Display.refreshPlatforms()
        refreshLevel()
    
    if readUserInput: 
        if isPressed(player.key) and not player.isShootingWeb:
            player.isShootingWeb = True
        if player.isShootingWeb and not isPressed(player.key):
            player.isShootingWeb = False
    player.mouseX, player.mouseY = pygame.mouse.get_pos()
    player.doActions()

    info = player.giveDisplayInfo(width, height)

    Display.display(screen, info, player.mouseX, player.mouseY)


    refreshScreen(screen, clock, fps)

pygame.quit()
sys.exit()
