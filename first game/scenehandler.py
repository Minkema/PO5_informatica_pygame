import pygame, settings, player, random, puzzels, textUI
from astroids import Astroid
from button import Button

currentScene = "default"
resolution = settings.resolution
screen = settings.screen
music_active = False
astroids = []
isDead = False
stopAstroids = False
stopAstroidsTijd = 0
afterStopAstroids = False


#!!!! Alleen voor development !!!!!!
godMode = True

Startbutton = 0
Settingsbutton = 0
Exitbutton = 0

def loadScene(scenename):
    #All specific sceneloading stuff needs to be handeld here
    global currentScene
    currentScene = scenename

    if(scenename == "startscreen"):
        loadStartScene()
    if(scenename == "testScene"):
        loadTestScene()
    if(scenename == "gameOver"):
        loadGameOverScene()

def loadTestScene():
    player.loadPlayer()
    textUI.init()
    global background
    global isDead
    #Want de speler is altijd alive als hij spawned
    isDead = False
    #Tries to load the specific background textures
    try:
        background_image = pygame.image.load('Textures/StartScreen/homescreen.png')
        background = pygame.transform.scale(background_image, resolution)
    #if loading fails it will print that in the console
    except pygame.error as e:
        print("startscreen couldn't load")

def loadStartScene():
    #Loads the music in pygame so that it can be used later in the scene loop
    pygame.mixer.music.load('Audio\Startscreen\startscreen.mp3')

    #Tries to load the specific background textures
    global background
    global Startbutton 
    global Settingsbutton 
    global Exitbutton
    try:
        background_image = pygame.image.load('Textures/StartScreen/homescreen.png')
        background = pygame.transform.scale(background_image, resolution)
    #if loading fails it will print that in the console
    except pygame.error as e:
        print("startscreen couldn't load")

    try:
        StartButton_img = pygame.image.load('Textures/StartScreen/StartButton.png').convert_alpha()
        SettingsButton_img = pygame.image.load('Textures/StartScreen/SettingsButton.png').convert_alpha()
        ExitButton_img = pygame.image.load('Textures/StartScreen/ExitButton.png').convert_alpha()
    except pygame.error as e:
        print("button images couldn't load")

    #creating button instance
    Startbutton = Button(((100/1920)*resolution[0]),((800/1920)*resolution[0]), StartButton_img)
    Settingsbutton = Button(((100/1920)*resolution[0]),((600/1920)*resolution[0]), SettingsButton_img)
    Exitbutton = Button(((100/1920)*resolution[0]),((400/1920)*resolution[0]), ExitButton_img)

def loadGameOverScene():
    global astroids
    print("you lasted " + str((pygame.time.get_ticks() - startTime) / 1000) + " seconds")
    astroids = []

#Starttick zodat we de tijd kunnen berekenen als je klaar bent
startTime = pygame.time.get_ticks()

#Deze wordt om de interval geupdate zodat we dingen kunnen laten spawnen om de zoveel seconden
laatsteTick = startTime

#Daadswerkelijke interval
interval = 1000

def mainGameLoop():
    screen.blit(background, (0,0))
    #All scene specific stuff in the main game loop needs to be handled here
    if currentScene == "startscreen":

        global music_active

        #loads the music file for this specific scene
        if music_active == False:
            pygame.mixer.music.play()
            music_active = True
        if pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(100)
        else:
            pygame.mixer.music.stop()
            music_active = False

        Startbutton.draw()
        Settingsbutton.draw()
        Exitbutton.draw()

        if Startbutton.checkClicked():
            loadScene("testScene")

        if Settingsbutton.checkClicked():
            print("settingsbutton pressed")

        if Exitbutton.checkClicked():
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    if currentScene == "testScene":
        #Comments about these functions are at the functions declarations
        global afterStopAstroids
        if(not afterStopAstroids):
            player.drawPlayer()
            player.update_movement()
            player.drawerPlayerTexture()
        global laatsteTick

        current_time = pygame.time.get_ticks()
        if current_time - laatsteTick >= interval:
            for i in range(5):
                if (not isDead and not stopAstroids):
                    laatsteTick = current_time
                    astroid = Astroid(random.randint(0, resolution[0]), 0, random.uniform(1,4))
                    astroids.append(astroid)
        
        if(stopAstroids and not afterStopAstroids):
            if (current_time - stopAstroidsTijd >= 2000):
                puzzels.loadRandomPuzzel()
                afterStopAstroids = True

        checkCol()
        textUI.drawText(str((current_time - startTime) / 1000) + "s", textUI.testFont , (0,0,0), resolution[0] / 2, resolution[1] / 2 + resolution[1] / 1080 *-200)

        for astroid in astroids:
            astroid.draw()

    if currentScene == "gameOver":
        screen.fill((0,0,0))

def checkCol():
    if(not godMode):
        global isDead
        playerRect = player.player
        for astroid in astroids:
            if playerRect.colliderect(astroid.x, astroid.y, 20*2, 20*2):
                isDead = True
                loadScene("gameOver")
            