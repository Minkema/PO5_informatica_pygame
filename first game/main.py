import pygame, player, scenehandler

if __name__ == "__main__":

    #Initiates some pygame functions
    pygame.init()
    pygame.mixer.init()

    #variable definitions
    resolution = [1920,1080] #resolution is done with a list so you can change it easier using code. This can be helpfull for resolution settings.
    playerY = resolution[1] / 2 #defines the starting y position
    playerX = resolution[0] / 2 #defines the starting x position
    playerWidht = (100/1920) * resolution[0]
    playerHeight = (150/1920) * resolution[0]
    screen = pygame.display.set_mode((resolution))
    
    clock = pygame.time.Clock() #initializes the clock
    fps = 120 #defines the amount of frames per second

    scenehandler.initSceneHandler(resolution, screen)
    
    scenehandler.loadScene("startscreen")

    run = True
    firstLoadUp = True

    #Main game loop
    while run:
        scenehandler.mainGameLoop()

        #For loading the player on the first startup and loading values for player script in player script
        if firstLoadUp:
            player.loadFirstValues()
            player.loadPlayer(playerX, playerY, playerWidht, playerHeight)
            firstLoadUp = False

        #Comments about these functions are at the functions declarations
        player.drawPlayer()
        
        player.update_movement()

        player.drawerPlayerTexture()

        #updates the screen so you can see changes
        pygame.display.update()

        clock.tick(fps)

        #this makes sure that when you click the X your game closes
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
    pygame.quit()