import pygame, settings, scenehandler
from astroids import Astroid
from settings import resolution

screen = settings.screen

#init all player values
playerHeight = settings.playerHeight
playerWidht = settings.playerWidht
character = 0

#movemenet values
playerX = settings.playerX
playerY = settings.playerY
movementspeed = 4

player = 0

def loadPlayer():
    #Resets all the values for if the game has been started before
    global playerX, playerY, character, player
    playerX = settings.playerX
    playerY = settings.playerY
    character = 0
    player = pygame.Rect((playerX,playerY,playerWidht,playerHeight))

    #trys to load texture on player
    try:
        character_image = pygame.image.load('Textures/Player/player.png')
        character = pygame.transform.scale(character_image, (playerWidht,playerHeight))
        #if loading fails it will print that in the console
    except:
        print("player texture couldn't load")
    player = character.get_rect()
    player.center = (playerX+(playerWidht/2), playerY+(playerHeight/2))

spacePressed = False
ePressed = False

#Moves the character with wasd and makes sure the character doesn't go out of the screen regardless of the resolution
def update_movement():
    key = pygame.key.get_pressed()
    global playerX, playerY, character, spacePressed, ePressed

    if (key[pygame.K_a] == True) and (playerX > 0):
        player.move_ip(-movementspeed * 60/settings.fps,0)
        playerX -= movementspeed * 60/settings.fps
    if (key[pygame.K_w] == True) and (playerY - movementspeed > 0):
        player.move_ip(0,-movementspeed * 60/settings.fps)
        playerY -= movementspeed * 60/settings.fps
    if (key[pygame.K_s] == True) and (playerY < resolution[1] - playerHeight):
        player.move_ip(0,movementspeed * 60/settings.fps)
        playerY += movementspeed * 60/settings.fps
    if (key[pygame.K_d] == True) and (playerX < (resolution[0]-playerWidht)):
        player.move_ip(movementspeed * 60/settings.fps,0)
        playerX += movementspeed * 60/settings.fps
    if(key[pygame.K_SPACE] == True and not spacePressed):
        spacePressed = True
        if(scenehandler.energyLevel - scenehandler.bulletCost >= 0):
            scenehandler.spawnBullets(playerX, playerY)
            scenehandler.energyLevel = scenehandler.energyLevel - scenehandler.bulletCost
    elif(not key[pygame.K_SPACE]):
        spacePressed = False
    if(key[pygame.K_e] == True and not ePressed):
        ePressed = True
        scenehandler.loadScene("planet")
    elif(not key[pygame.K_e]):
        ePressed = False


    #MOET UIT DE GAME ALS HIJ AF IS, DIT ZORGT ERVOOR DAT JE EEN PUZZEL IN JE SCHERM KRIJGT ALS JE P INDRUKT
    if (key[pygame.K_p] == True and not scenehandler.stopAstroids):
        scenehandler.stopAstroids = True
        scenehandler.stopAstroidsTijd = pygame.time.get_ticks()

#Draws the acual texture on the player
def drawerPlayerTexture():
    screen.blit(character, player)