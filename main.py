import pygame
import player

if __name__ == "__main__":

    pygame.init()
    pygame.mixer.init()

    #variable definitions
    resolution = [1080,720] #resolution is done with a list so you can change it easier using code. This can be helpfull for resolution settings.
    playerY = resolution[1] / 2 #defines the starting y position
    playerX = resolution[0] / 2 #defines the starting x position
    playerWidht = 50
    playerHeight = 75
    screen = pygame.display.set_mode((resolution))
    
    music_volume = 0.4 #defines the volume of the music
    music_active = False
    clock = pygame.time.Clock() #initializes the clock
    fps = 120 #defines the amount of frames per second

    #loads the music file for the start screen
    pygame.mixer.music.load('Audio\Startscreen\startscreen.mp3')

    #tries to load textures
    try:
        original_background = pygame.image.load('Textures/StartScreen/homescreen.png')
        background = pygame.transform.scale(original_background, resolution)
        location = "startscreen"
    #if loading fails it will print that in the console
    except pygame.error as e:
        print("startscreen couldn't load")

    run = True
    firstLoadUp = True
    while run:
        #draws the background. You can change the background anywhere in the code by using [background = pygame.image.load('location')]
        screen.blit(background, (0,0))

        #For loading the player on the first startup and loading values for player script in player script
        if firstLoadUp:
            player.loadFirstValues(screen, resolution)
            player.loadPlayer(playerX, playerY, playerWidht, playerHeight, resolution)
            firstLoadUp = False

        #draws the player
        player.drawPlayer(screen)
        #moves the character with wasd and makes sure the character doesn't go out of the screen regardless of the resolution
        player.update_movement()

        player.drawerPlayerTexture()
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
