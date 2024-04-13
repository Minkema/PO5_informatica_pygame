import pygame, scenehandler, settings

if __name__ == "__main__":

    #Initiates some pygame functions
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Space Traversers")
    
    clock = pygame.time.Clock() #initializes the clock
    
    #Inits the scene
    scenehandler.loadScene("startscreen")
    # scenehandler.loadScene("testScene")
    
    run = True
    
    #Main game loop
    while run:
        scenehandler.mainGameLoop()

        #updates the screen so you can see changes
        pygame.display.update()
        clock.tick(settings.fps)

        #this handles all the types of events that can happen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
    pygame.quit()
