import pygame, scenehandler, settings, puzzels, textUI, cv2

playIntro = False

def playOpeningVid():
    if playIntro:
        audioClip = 'Audio/Intro/introaudio.mp3'
        pygame.mixer.music.load(audioClip)
        pygame.mixer.music.play()
    
        cap = cv2.VideoCapture('Videos/intro.mp4')
        if (cap.isOpened()== False):  
            print("File not loaded")
    
        while(cap.isOpened()):
            ret, frame = cap.read() 
            if ret == True: 
            # Display the resulting frame 
                frame = cv2.resize(frame, (settings.resolution[0], settings.resolution[1]))
                cv2.namedWindow('Video', cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow('Video', frame) 
                cv2.waitKey(33)
                if cv2.waitKey(33) == 27:
                    break     
            else: 
                break
        cap.release() 
  
        # Closes all the frames 
        cv2.destroyAllWindows() 
    initGame()   

def initPygame():
    #Initiates some pygame functions
    pygame.init()
    pygame.mixer.init()

def initGame():
    
    pygame.display.set_caption("Space Traversers")

    #Kijk in het testUI.py bestand om te zien wat dit doet
    textUI.init()
        
    clock = pygame.time.Clock() #initializes the clock
    
    #Inits the scene
    scenehandler.loadScene("startscreen")
    #scenehandler.loadScene("testScene")
    
    run = True
    
    #Main game loop
    while run:
        scenehandler.mainGameLoop()
        puzzels.mainGameLoop()
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

if __name__ == "__main__":
    initPygame()
    playOpeningVid()


    


