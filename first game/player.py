import pygame, settings, scenehandler
from astroids import Astroid

resolution = settings.resolution
screen = settings.screen

#init all player values
playerHeight = settings.playerHeight
playerWidht = settings.playerWidht
character = 0

#movemenet values
playerX = settings.playerX
playerY = settings.playerY
movementspeed = 4

player = pygame.Rect((playerX,playerY,playerWidht,playerHeight))


def loadPlayer():
    #trys to load texture on player
    global character
    try:
        character_image = pygame.image.load('Textures/Player/player.png')
        character = pygame.transform.scale(character_image, (playerWidht,playerHeight))
        #if loading fails it will print that in the console
    except:
        print("player texture couldn't load")
    player = character.get_rect()
    player.center = (playerX+(playerWidht/2), playerY+(playerHeight/2))

#Draws the player
def drawPlayer():
    pygame.draw.rect(screen, (255, 0, 100), player)

#Moves the character with wasd and makes sure the character doesn't go out of the screen regardless of the resolution
def update_movement():
    key = pygame.key.get_pressed()
    global playerX, playerY, character

    if (key[pygame.K_a] == True) and (playerX > 0):
        player.move_ip(-movementspeed,0)
        playerX -= movementspeed
    if (key[pygame.K_w] == True) and (playerY < resolution[1]):
        player.move_ip(0,-movementspeed)
        playerY += movementspeed
    if (key[pygame.K_s] == True) and (playerY > 0+playerHeight):
        player.move_ip(0,movementspeed)
        playerY -= movementspeed
    if (key[pygame.K_d] == True) and (playerX < (resolution[0]-playerWidht)):
        player.move_ip(movementspeed,0)
        playerX += movementspeed
    if (key[pygame.K_p] == True and not scenehandler.stopAstroids):
        scenehandler.stopAstroids = True
        scenehandler.stopAstroidsTijd = pygame.time.get_ticks()

#Draws the acual texture on the player
def drawerPlayerTexture():
    screen.blit(character, player)