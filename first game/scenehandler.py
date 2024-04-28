import pygame, settings, player, random, puzzels, textUI
from astroids import Astroid
from button import ImageButton
from bullet import Bullet

currentScene = "default"
music_active = False
astroids = []
bullets = []
isDead = False
stopAstroids = False
stopAstroidsTijd = 0
afterStopAstroids = False
delayTime = 0
speedMultiplier = 1
scoreMultiplier = 1
energyLevel = 0
bulletCost = 5

#!!!! Alleen voor development !!!!!! MOET FALSE ZIJN ALS HET SPEL KLAAR IS ANDERS KAN JE NIET DOOD GAAN
godMode = True

Startbutton = 0
Settingsbutton = 0
Exitbutton = 0
retryButton = 0
menuButton = 0
selectedTab = 0

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
    global background, isDead, startTime, laatsteTick, stopAstroids, afterStopAstroids, delayTime, astroids, bullets, energyLevel

    #Starttime is nodig zodat we kunnen uitrekenen hoelang de speler het heeft overleefd
    startTime = pygame.time.get_ticks()

    #Laatste tick wordt continue veranderd maar moet wel beginnen als de startijd begint daarom worden die hier aanelkaar gelijk gested
    laatsteTick = startTime

    #Resets all the values for if the game has been started before
    isDead = False
    stopAstroids = False
    afterStopAstroids = False
    delayTime = 0
    astroids = []
    bullets = []
    energyLevel = 50

    #Tries to load the specific background textures
    try:
        background_image = pygame.image.load('Textures/MainGame/Background.png')
        background = pygame.transform.scale(background_image, settings.resolution)
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
        background = pygame.transform.scale(background_image, settings.resolution)
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
    Startbutton = ImageButton(((300/1920)*settings.resolution[0]),((400/1920)*settings.resolution[0]), StartButton_img)
    Settingsbutton = ImageButton(((300/1920)*settings.resolution[0]),((575/1920)*settings.resolution[0]), SettingsButton_img)
    Exitbutton = ImageButton(((300/1920)*settings.resolution[0]),((750/1920)*settings.resolution[0]), ExitButton_img)

def LoadSettingsScene():
    global background
    global tempResolution
    global tempFramerate
    global tempDifficulty
    global tempVolume

    try:
        background_image = pygame.image.load('Textures/Settings/Settings_Background.png')
        background = pygame.transform.scale(background_image, settings.resolution)
    #if loading fails it will print that in the console
    except pygame.error as e:
        print("startscreen couldn't load")

    pygame.mixer.music.load('Audio\Settings\SettingsPage.mp3')

    tempResolution = settings.resolution
    tempFramerate = settings.fps
    tempDifficulty = settings.difficulty
    tempVolume = settings.volume

def loadGameOverScene():
    global astroids, background, retryButton, menuButton
    #Loads the background for game over scene
    try:
        background_image = pygame.image.load('Textures/GameOver Screen/GameOver.png')
        background = pygame.transform.scale(background_image, settings.resolution)
    except pygame.error as e:
        print("Game Over screen failed to load")

    #Loads the music in pygame so that it can be used later in the scene loop

    try:
        retryButton_img = pygame.image.load('Textures/GameOver Screen/retryButton.png').convert_alpha()
        menuButton_img = pygame.image.load('Textures/GameOver Screen/menuButton.png').convert_alpha()
    except pygame.error as e:
        print("button images couldn't load")

    #creating button instance
    retryButton = ImageButton(((300/1920)*settings.resolution[0]),((680/1920)*settings.resolution[0]), retryButton_img)
    menuButton = ImageButton(((1000/1920)*settings.resolution[0]),((680/1920)*settings.resolution[0]), menuButton_img)

def mainGameLoop():
    settings.screen.blit(background, (0,0))

    #All scene specific stuff in the main game loop needs to be handled here
    if currentScene == "startscreen":
        startSceneMainGameLoop()

    if currentScene == "testScene":
        testSceneMainGameLoop()

    if currentScene == "gameOver":
        gameOverSceneMainGameLoop()
    
    #Scene onafhankelijke dingen worden hier gehandeld

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

    if currentScene == "SettingsScreen":   
        global selectedTab 

        if selectedTab == 0:
            Tab1 = textUI.drawText("<Resolution>", textUI.settingsFont,(153, 204, 255),(300/1920*settings.resolution[0]),(200/1080*settings.resolution[1]))
            Tab2 = textUI.drawText("<FrameRate>", textUI.settingsFont,(140, 141, 143),(295/1920*settings.resolution[0]),(300/1080*settings.resolution[1]))
            Tab3 = textUI.drawText("<Difficulty>", textUI.settingsFont,(140, 141, 143),(278/1920*settings.resolution[0]),(400/1080*settings.resolution[1]))
            Tab4 = textUI.drawText("<Volume>", textUI.settingsFont,(140, 141, 143),(262/1920*settings.resolution[0]),(500/1080*settings.resolution[1]))
        
        if selectedTab == 1:
            Tab1 = textUI.drawText("<Resolution>", textUI.settingsFont,(140, 141, 143),(300/1920*settings.resolution[0]),(200/1080*settings.resolution[1]))
            Tab2 = textUI.drawText("<FrameRate>", textUI.settingsFont,(153, 204, 255),(295/1920*settings.resolution[0]),(300/1080*settings.resolution[1]))
            Tab3 = textUI.drawText("<Difficulty>", textUI.settingsFont,(140, 141, 143),(278/1920*settings.resolution[0]),(400/1080*settings.resolution[1]))
            Tab4 = textUI.drawText("<Volume>", textUI.settingsFont,(140, 141, 143),(262/1920*settings.resolution[0]),(500/1080*settings.resolution[1]))

        if selectedTab == 2:
            Tab1 = textUI.drawText("<Resolution>", textUI.settingsFont,(140, 141, 143),(300/1920*settings.resolution[0]),(200/1080*settings.resolution[1]))
            Tab2 = textUI.drawText("<FrameRate>", textUI.settingsFont,(140, 141, 143),(295/1920*settings.resolution[0]),(300/1080*settings.resolution[1]))
            Tab3 = textUI.drawText("<Difficulty>", textUI.settingsFont,(153, 204, 255),(278/1920*settings.resolution[0]),(400/1080*settings.resolution[1]))
            Tab4 = textUI.drawText("<Volume>", textUI.settingsFont,(140, 141, 143),(262/1920*settings.resolution[0]),(500/1080*settings.resolution[1]))

        if selectedTab == 3:
            Tab1 = textUI.drawText("<Resolution>", textUI.settingsFont,(140, 141, 143),(300/1920*settings.resolution[0]),(200/1080*settings.resolution[1]))
            Tab2 = textUI.drawText("<FrameRate>", textUI.settingsFont,(140, 141, 143),(295/1920*settings.resolution[0]),(300/1080*settings.resolution[1]))
            Tab3 = textUI.drawText("<Difficulty>", textUI.settingsFont,(140, 141, 143),(278/1920*settings.resolution[0]),(400/1080*settings.resolution[1]))
            Tab4 = textUI.drawText("<Volume>", textUI.settingsFont,(153, 204, 255),(262/1920*settings.resolution[0]),(500/1080*settings.resolution[1]))

        TabList = [Tab1, Tab2, Tab3,Tab4]
        settingsList = [tempResolution, tempFramerate, tempDifficulty, tempVolume]


        textUI.drawText(str(tempResolution[0]) +" X "+str(tempResolution[1]), textUI.settingsFont,(153, 204, 255),(650/1920*settings.resolution[0]),(200/1080*settings.resolution[1]))
        textUI.drawText((str(settings.fps)+"FPS"), textUI.settingsFont,(153, 204, 255),(650/1920*settings.resolution[0]),(300/1080*settings.resolution[1]))
        textUI.drawText(str(settings.difficulty), textUI.settingsFont,(153, 204, 255),(650/1920*settings.resolution[0]),(400/1080*settings.resolution[1]))
        textUI.drawText(str(settings.volume), textUI.settingsFont,(153, 204, 255),(650/1920*settings.resolution[0]),(500/1080*settings.resolution[1]))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loadScene("startscreen")
                elif event.key == pygame.K_DOWN:
                    selectedTab += 1
                    if selectedTab > len(TabList)-1:
                        selectedTab = 0
                elif event.key == pygame.K_UP:
                    selectedTab -= 1
                    if selectedTab < 0:
                        selectedTab = len(TabList)-1
                elif event.key == pygame.K_RIGHT:
                    print(settingsList[selectedTab])
                elif event.key == pygame.K_LEFT:
                    print(settingsList[selectedTab])
                elif event.key == pygame.K_a:
                    settings.applysettings()

def startSceneMainGameLoop():
    #Draw de daadwerkelijke knoppen
    Startbutton.draw()
    Settingsbutton.draw()
    Exitbutton.draw()

    #Check voor of er op de knoppen wordt gelickt. Hoe dit precies werkt staat in de button class.
    if Startbutton.checkClicked():
        loadScene("testScene")

    if Settingsbutton.checkClicked():
        loadScene("SettingsScreen")

    #Invoked de quit event zodat het eigenlijk lijkt alsof de speler op het kruisje heeft geclickt en de main function alles stopt
    if Exitbutton.checkClicked():
        pygame.event.post(pygame.event.Event(pygame.QUIT))

#Deze wordt om de interval geupdate zodat we dingen kunnen laten spawnen om de zoveel seconden
laatsteTick = 0

#Daadswerkelijke interval
interval = 1000

def testSceneMainGameLoop():
    global afterStopAstroids, astroids, bullets
    #Comments about these functions are at the functions declarations
    #afterstopAstroids staat iets verder naar beneden uitgelegd
    if(not afterStopAstroids):
        player.update_movement()
        player.drawerPlayerTexture()
    global laatsteTick

    current_time = pygame.time.get_ticks()
    if current_time - laatsteTick >= interval:
        for i in range(5):
            if (not isDead and not stopAstroids):
                laatsteTick = current_time
                if(random.randint(0, 25) == 5):
                    astroid = Astroid(random.randint(0, settings.resolution[0]), 0, random.uniform(1,4), True)
                else:
                    astroid = Astroid(random.randint(0, settings.resolution[0]), 0, random.uniform(1,4), False)
                astroids.append(astroid)
    
    #Oke dit kan confusing zijn maar stopAstroids = true zodra een puzzel wordt gecalled. afterStopAstroids is pas true na een bepaalde timer zodat de player nog ff wat tijd heeft 
    #om astroids te ontwijken
    if(stopAstroids and not afterStopAstroids):
        textUI.drawText("Er komt een puzzel aan wees ready!", textUI.testFont, (225,225,225), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-100)
        if (current_time - stopAstroidsTijd >= 2000):
            puzzels.loadRandomPuzzel()
            afterStopAstroids = True
    

    checkCol()
    #Print time, score and level on screen
    showTimeScoreLevel(current_time)

    #Lijst van astroids die de volgende frame weg moeten
    listOfDeletedAstroids = []
    listOfDeletedBullets = []

    for i in range(len(astroids)):
        astroid = astroids[i]
        #Detect of de astroids buiten het scherm zij
        if(astroid.y > settings.resolution[1]):
            listOfDeletedAstroids.append(i)
        astroid.draw()

    for i in range(len(bullets)):
        bullet = bullets[i]
        for j in range(len(astroids)):
            astroid = astroids[j]
            if bullet.rect1.colliderect(astroid.x - 20, astroid.y - 20, 20*2, 20*2) and bullet.firstAlive:
                listOfDeletedAstroids.append(j)
                bullet.firstAlive = False
            if bullet.rect2.colliderect(astroid.x - 20, astroid.y - 20, 20*2, 20*2) and bullet.secondAlive:
                listOfDeletedAstroids.append(j)
                bullet.secondAlive = False

        #Detect of de astroids buiten het scherm zij
        if(bullet.y < 0):
            listOfDeletedBullets.append(i)
        bullet.draw()

    #Delete de astroids van de vorige frame
    currentOffset = 0
    for i in range(len(listOfDeletedAstroids)):
        astroids.pop(listOfDeletedAstroids[i - currentOffset])
        currentOffset = currentOffset + 1

    currentOffset = 0
    for i in range(len(listOfDeletedBullets)):           
        bullets.pop(listOfDeletedBullets[i - currentOffset])
        currentOffset = currentOffset + 1

def checkCol():
    global isDead
    playerRect = player.player
    deletedAstroids = []
    for i in range(len(astroids)):
        astroid = astroids[i]
        if playerRect.colliderect(astroid.x - 20, astroid.y - 20, 20*2, 20*2):
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

def showTimeScoreLevel(current_time):
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
        textUI.drawText("Level " + str(currentLevel), textUI.testFont , (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-500)
        #Draws Time
        textUI.drawText(str(round((current_time - startTime - delayTime) / 1000, 1)) + "s", textUI.testFont , (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-400)
        #Draws Score
        textUI.drawText("Score: "+ str(currentScore), textUI.testFont , (255,255,255), settings.resolution[0] - 1800, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-400)
        #Draws bullet energy
        textUI.drawText("Energy: "+ str(energyLevel), textUI.testFont , (255,255,255), settings.resolution[0] - 1800, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-300)

def spawnBullets(x,y):
    global bullets
    bullet = Bullet(x,y) 
    bullets.append(bullet)

def gameOverSceneMainGameLoop():
    #Draws retry and main menu button
    retryButton.draw()
    menuButton.draw()   

    #Restarts game and sends to main menu once buttons are clicked
    #Needs to be fixed (loadScene doesnt work properly)
    if retryButton.checkClicked() == True:
        loadScene("testScene")

    if menuButton.checkClicked() == True:
        loadScene("startscreen")
