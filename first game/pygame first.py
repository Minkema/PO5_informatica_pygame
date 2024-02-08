import pygame

pygame.init()
pygame.mixer.init()

#variable definitions
resolution = [1920,1080] #resolution is done with a list so you can change it easier using code. This can be helpfull for resolution settings.
screen = pygame.display.set_mode((resolution))
playerY = resolution[1] / 2 #defines the starting y position
playerX = resolution[0] / 2 #defines the starting x position
playerHeight = 150
playerWidht = 100
player = pygame.Rect((playerX,playerY,playerWidht,playerHeight)) #REMOVE LATER!!!
music_volume = 0.4 #defines the volume of the music
music_active = False
clock = pygame.time.Clock() #initializes the clock
fps = 120 #defines the amount of frames per second
movementspeed = 4

#loads the music file for the start screen
pygame.mixer.music.load('Audio\Startscreen\startscreen.mp3')

#tries to load textures
try:
    original_background = pygame.image.load('Textures/StartScreen/Temp.png')
    background = pygame.transform.scale(original_background, resolution)
    location = "startscreen"
#if loading fails it will print this in the console
except:
    print("startscreen couldn't load")

try:
    original_character = pygame.image.load('Textures/Player/player.png')
    character = pygame.transform.scale(original_character, (playerWidht,playerHeight))
#if loading fails it will print that in the console
except:
    print("player texture couldn't load")
player = character.get_rect()
player.center = (playerX+(playerWidht/2), playerY+(playerHeight/2))

run = True
while run:
    #draws the background. You can change the background anywhere in the code by using [background = pygame.image.load('location')]
    screen.blit(background, (0,0))
    
    #draws the player
    pygame.draw.rect(screen, (255, 0, 100), player)

    #moves the character with wasd and makes sure the character doesn't go out of the screen regardless of the resolution
    key = pygame.key.get_pressed()
    
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

    screen.blit(character, player)

    #updates the screen so you can see changes
    pygame.display.update()

    if (location == "startscreen") and (music_active == False):
        pygame.mixer.music.play()
        print("music started")
        music_active = True
    if (pygame.mixer.music.get_busy()) and (location == "startscreen"):
        pygame.time.Clock().tick(100)
    else:
        pygame.mixer.music.stop()
        music_active = False

    clock.tick(fps)

    #this makes sure that when you click the X your game closes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
pygame.quit()
