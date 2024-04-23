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
speedMultiplier = 1
scoreMultiplier = 1

#!!!! Alleen voor development !!!!!! MOET FALSE ZIJN ALS HET SPEL KLAAR IS ANDERS KAN JE NIET DOOD GAAN
godMode = True

Startbutton = 0
Settingsbutton = 0
Exitbutton = 0
retryButton = 0
menuButton = 0

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
    if(scenename == "SettingsScreen"):
        LoadSettingsScene()

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

    pygame.mixer.music.load('Audio/MainGame/MainGame.mp3')

def loadStartScene():
    #Loads the music in pygame so that it can be used later in the scene loop
    pygame.mixer.music.load('Audio\Startscreen\startscreen.mp3')

    global background
    global Startbutton 
    global Settingsbutton 
    global Exitbutton
    #Tries to load the specific background textures
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


def LoadSettingsScene():
    global background
    try:
        background_image = pygame.image.load('Textures/Settings/Settings_Background.png')
        background = pygame.transform.scale(background_image, resolution)
    #if loading fails it will print that in the console
    except pygame.error as e:
        print("startscreen couldn't load")

    pygame.mixer.music.load('Audio\Settings\SettingsPage.mp3')

def loadGameOverScene():
    global astroids, background, retryButton, menuButton
    #Loads the background for game over scene
    try:
        background_image = pygame.image.load('Textures/GameOver Screen/GameOver.png')
        background = pygame.transform.scale(background_image, resolution)
    except pygame.error as e:
        print("Game Over screen failed to load")

    #Loads the music in pygame so that it can be used later in the scene loop
    #Er moet nieuwe muziek hier toegevoegd worden
    #pygame.mixer.music.load('Audio\Startscreen\startscreen.mp3')

    try:
        retryButton_img = pygame.image.load('Textures/GameOver Screen/retryButton.png').convert_alpha()
        menuButton_img = pygame.image.load('Textures/GameOver Screen/menuButton.png').convert_alpha()
    except pygame.error as e:
        print("button images couldn't load")

    #creating button instance
    retryButton = ImageButton(((300/1920)*resolution[0]),((680/1920)*resolution[0]), retryButton_img)
    menuButton = ImageButton(((1000/1920)*resolution[0]),((680/1920)*resolution[0]), menuButton_img)

    
    astroids = []

#Deze wordt om de interval geupdate zodat we dingen kunnen laten spawnen om de zoveel seconden
laatsteTick = 0

#Daadswerkelijke interval
interval = 1000

def mainGameLoop():
    global afterStopAstroids, stopAstroids, delayTime
    screen.blit(background, (0,0))
    #All scene specific stuff in the main game loop needs to be handled here
    if currentScene == "startscreen":

        #Draw de daadwerkelijke knoppen
        Startbutton.draw()
        Settingsbutton.draw()
        Exitbutton.draw()

        #Check voor of er op de knoppen wordt gelickt. Hoe dit precies werkt staat in de button class.
        if Startbutton.checkClicked():
            loadScene("testScene")
            stopAstroids = False
            afterStopAstroids = False

        if Settingsbutton.checkClicked():
            loadScene("SettingsScreen")

        #Invoked de quit event zodat het eigenlijk lijkt alsof de speler op het kruisje heeft geclickt en de main function alles stopt
        if Exitbutton.checkClicked():
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    if currentScene == "testScene":
        #Comments about these functions are at the functions declarations
        global current_time
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
                    if(random.randint(0, 25) == 5):
                        astroid = Astroid(random.randint(0, resolution[0]), 0, random.uniform(1,4), True)
                    else:
                        astroid = Astroid(random.randint(0, resolution[0]), 0, random.uniform(1,4), False)
                    astroids.append(astroid)
        
        #Oke dit kan confusing zijn maar stopAstroids = true zodra een puzzel wordt gecalled. afterStopAstroids is pas true na een bepaalde timer zodat de player nog ff wat tijd heeft 
        #om astroids te ontwijken
        if(stopAstroids and not afterStopAstroids):
            textUI.drawText("Er komt een puzzel aan wees ready!", textUI.testFont, (225,225,225), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-100)
            if (current_time - stopAstroidsTijd >= 2000):
                puzzels.loadRandomPuzzel()
                afterStopAstroids = True

        #Runs collision check (constant)
        checkCol()

        #Print time, score and level on screen
        showTimeScoreLevel()
        
        #Lijst van astroids die de volgende frame weg moeten
        listOfDeletedAstroids = []

        for i in range(len(astroids)):
            astroid = astroids[i]
            #Detect of de astroids buiten het scherm zij
            if(astroid.y > resolution[1]):
                listOfDeletedAstroids.append(i)
            astroid.draw()

        #Delete de astroids van de vorige frame
        for i in range(len(listOfDeletedAstroids)):
            astroids.pop(listOfDeletedAstroids[i])

    if currentScene == "gameOver":
        #Draws retry and main menu button
        retryButton.draw()
        menuButton.draw()   

        #Restarts game and sends to main menu once buttons are clicked
        if retryButton.checkClicked() == True:
            loadScene("testScene")
            stopAstroids = False
            afterStopAstroids = False
            delayTime = 0

            print("Retry button was pressed")
    
        if menuButton.checkClicked() == True:
            loadScene("startscreen")



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

def checkCol():
    global isDead
    playerRect = player.player
    deletedAstroids = []
    for i in range(len(astroids)):
        astroid = astroids[i]
        if playerRect.colliderect(astroid.x, astroid.y, 20*2, 20*2):
            if not astroid.isPuzzel:
                if(not godMode):
                    isDead = True
                    loadScene("gameOver")
            elif astroid.isPuzzel:
                deletedAstroids.append(i)
                global stopAstroids, stopAstroidsTijd
                stopAstroids = True
                stopAstroidsTijd = pygame.time.get_ticks()
        
    for i in range(len(deletedAstroids)):
        astroids.pop(deletedAstroids[i])    

def showTimeScoreLevel():
    global currentScore, currentLevel, speedMultiplier, scoreMultiplier
    currentScore = round((current_time - startTime - delayTime) / 60 * scoreMultiplier, 0) 

    #Increases level once score threshold has been met
    if currentScore <= 1000:
        currentLevel = 1
    elif currentScore <= 2000 and currentScore >= 1000:
        currentLevel = 2
        speedMultiplier = 1.5
    elif currentScore <= 3000 and currentScore >= 2000:
        currentLevel = 3
        speedMultiplier = 2
    elif currentScore <= 4000 and currentScore >= 3000:
        currentLevel = 4
        speedMultiplier = 2.5
    elif currentScore <= 5000 and currentScore >= 4000:
        currentLevel = 5
        speedMultiplier = 3
    elif currentScore >= 5000:
        currentLevel = "???"
    
    #De timer moet niet worden laten zien als we bezig zijn met een puzzel
    if not stopAstroids:
        #Draws Level
        textUI.drawText("Level " + str(currentLevel), textUI.testFont , (255,255,255), resolution[0] / 2, resolution[1] / 2 + resolution[1] / 1080 *-500)
        #Draws Time
        textUI.drawText(str(round((current_time - startTime - delayTime) / 1000, 1)) + "s", textUI.testFont , (255,255,255), resolution[0] / 2, resolution[1] / 2 + resolution[1] / 1080 *-400)
        #Draws Score
        textUI.drawText("Score: "+ str(currentScore), textUI.testFont , (255,255,255), resolution[0] - 1800, resolution[1] / 2 + resolution[1] / 1080 *-400)
