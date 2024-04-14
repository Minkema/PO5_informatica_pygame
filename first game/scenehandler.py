import pygame, settings, player, random, puzzels, textUI
from astroids import Astroid
from button import ImageButton
from settings import resolution

currentScene = "default"
screen = settings.screen
music_active = False
astroids = []
isDead = False
stopAstroids = False
stopAstroidsTijd = 0
afterStopAstroids = False
delayTime = 0

#!!!! Alleen voor development !!!!!! MOET FALSE ZIJN ALS HET SPEL KLAAR IS ANDERS KAN JE NIET DOOD GAAN
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
    global background, isDead, startTime, laatsteTick
    #Starttime is nodig zodat we kunnen uitrekenen hoelang de speler het heeft overleefd
    startTime = pygame.time.get_ticks()
    #Laatste tick wordt continue veranderd maar moet wel beginnen als de startijd begint daarom worden die hier aanelkaar gelijk gested
    laatsteTick = startTime
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
    Startbutton = ImageButton(((300/1920)*resolution[0]),((400/1920)*resolution[0]), StartButton_img)
    Settingsbutton = ImageButton(((300/1920)*resolution[0]),((575/1920)*resolution[0]), SettingsButton_img)
    Exitbutton = ImageButton(((300/1920)*resolution[0]),((750/1920)*resolution[0]), ExitButton_img)

def loadGameOverScene():
    global astroids
    astroids = []

#Deze wordt om de interval geupdate zodat we dingen kunnen laten spawnen om de zoveel seconden
laatsteTick = 0

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

        #Draw de daadwerkelijke knoppen
        Startbutton.draw()
        Settingsbutton.draw()
        Exitbutton.draw()

        #Check voor of er op de knoppen wordt gelickt. Hoe dit precies werkt staat in de button class.
        if Startbutton.checkClicked():
            loadScene("testScene")

        if Settingsbutton.checkClicked():
            print("settingsbutton pressed")

        #Invoked de quit event zodat het eigenlijk lijkt alsof de speler op het kruisje heeft geclickt en de main function alles stopt
        if Exitbutton.checkClicked():
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    if currentScene == "testScene":
        #Comments about these functions are at the functions declarations
        global afterStopAstroids

        #afterstopAstroids staat iets verder naar beneden uitgelegd
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
        
        #Oke dit kan confusing zijn maar stopAstroids = true zodra een puzzel wordt gecalled. afterStopAstroids is pas true na een bepaalde timer zodat de player nog ff wat tijd heeft 
        #om astroids te ontwijken
        if(stopAstroids and not afterStopAstroids):
            if (current_time - stopAstroidsTijd >= 2000):
                puzzels.loadRandomPuzzel()
                afterStopAstroids = True

        checkCol()
        #De timer moet niet worden laten zien als we bezig zijn met een puzzel
        if not stopAstroids:
            textUI.drawText(str(round((current_time - startTime - delayTime) / 1000, 1)) + "s", textUI.testFont , (255,255,255), resolution[0] / 2, resolution[1] / 2 + resolution[1] / 1080 *-400)

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
            