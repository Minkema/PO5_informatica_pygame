import pygame

pygame.init()

#variable definitions
resolution = [1920,1080] #resolution is done with a list so you can change it easier using code. This can be helpfull for resolution settings.
screen = pygame.display.set_mode((resolution))
playerY = 540 #defines the starting y position
playerX = 960 #defines the starting x position
playerHeight = 75
playerWidht = 50
player = pygame.Rect((playerX,playerY,playerWidht,playerHeight))

#tries to load the image
try:
    original_background = pygame.image.load('Textures/StartScreen/Temp.png')
    background = pygame.transform.scale(original_background, resolution)
#if loading fails it will print that in the console
except pygame.error as e:
    print("Afbeelding kon niet worden geladen:", e)

run = True
while run:
    #draws the background. You can change the background anywhere in the code by using [background = pygame.image.load('location')]
    screen.blit(background, (0,0))
    
    #draws the player
    pygame.draw.rect(screen, (255, 0, 100), player)

    #moves the character with wasd and makes sure the character doesn't go out of the screen regardless of the resolution
    key = pygame.key.get_pressed()
    if (key[pygame.K_a] == True) and (playerX > 0):
        player.move_ip(-1,0)
        playerX -= 1
    if (key[pygame.K_w] == True) and (playerY < resolution[1]):
        player.move_ip(0,-1)
        playerY += 1
    if (key[pygame.K_s] == True) and (playerY > 0+playerHeight):
        player.move_ip(0,1)
        playerY -= 1
    if (key[pygame.K_d] == True) and (playerX < (resolution[0]-playerWidht)):
        player.move_ip(1,0)
        playerX += 1

    #this makes sure that when you click the X your game closes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()
