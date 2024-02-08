import pygame

resolution = 0
movementspeed = 4
screen = 0

#init all player values
player = 0
playerHeight = 0
playerWidht = 0
character = 0

#movemenet values
playerX = 0
playerY = 0

def loadFirstValues(screenImport, resolutionImport):
    global screen, resolution
    resolution = resolutionImport
    screen = screenImport

def loadPlayer(x, y, Widht, Height):
    #Global so that in can be changed not local
    global player, playerHeight, playerWidht, playerX, playerY, character
    player = pygame.Rect((x,y,Widht,Height))
    playerHeight = Height
    playerWidht = Widht
    playerX = x
    playerY = y

    try:
        original_character = pygame.image.load('Textures/Player/player.png')
        character = pygame.transform.scale(original_character, (playerWidht,playerHeight))
        #if loading fails it will print that in the console
    except:
        print("player texture couldn't load")
    player = character.get_rect()
    player.center = (playerX+(playerWidht/2), playerY+(playerHeight/2))

def drawPlayer():
    pygame.draw.rect(screen, (255, 0, 100), player)

def update_movement():
    key = pygame.key.get_pressed()
    #Global so that in can be changed not local
    global playerX, playerY
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

def drawerPlayerTexture():
    screen.blit(character, player)