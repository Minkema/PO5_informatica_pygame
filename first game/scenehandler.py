import pygame, settings, player, random, puzzels, textUI, main
from asteroids import Asteroid
from asteroids import Planet
from button import ImageButton
from bullet import Bullet

currentScene = "default"
music_active = False
asteroids = []
bullets = []
isDead = False
stopAsteroids = False
stopAsteroidsTijd = 0
afterStopAsteroids = False
delayTime = 0
speedMultiplier = 1
scoreMultiplier = 1
energyLevel = 0
bulletCost = 5
planet = 0
amountOfPlanets = 0
survivalChance = 0
loadedSceneTime = 0
secondsTimer = 0
retryTime = 0
previousScore = 0
amountOfAsteroids = 0
currentLevel = 1
previousLevel = 1
inPuzzle = False

Startbutton = 0
Settingsbutton = 0
Exitbutton = 0
retryButton = 0
menuButton = 0
selectedTab = 0
landButton = 0
continueButton = 0

def loadScene(scenename):
    #All specific sceneloading stuff needs to be handeld here
    global currentScene, loadedSceneTime
    loadedSceneTime = pygame.time.get_ticks()
    currentScene = scenename

    if(scenename == "startscreen"):
        loadStartScene()
    if(scenename == "mainScene"):
        loadMainScene(True)
    if(scenename == "gameOver"):
        loadGameOverScene()
    if(scenename == "gameGewonnen"):
        loadGameGewonnenScene()
    if(scenename == "SettingsScreen"):
        LoadSettingsScene()
    if(scenename == "planet"):
        LoadPlanetScene()  

def loadMainScene(resetValues):
    player.loadPlayer()
    global background, interval, amountOfAsteroids

    pygame.mixer.music.load('Audio\MainGame\MainGame.mp3')

    if resetValues:
        global isDead, startTime, laatsteTick, stopAsteroids, afterStopAsteroids, delayTime, asteroids, bullets, energyLevel
        #Starttime is nodig zodat we kunnen uitrekenen hoelang de speler het heeft overleefd
        startTime = pygame.time.get_ticks()

        #Laatste tick wordt continue veranderd maar moet wel beginnen als de startijd begint daarom worden die hier aanelkaar gelijk gested
        laatsteTick = startTime

        #Resets all the values for if the game has been started before
        isDead = False
        stopAsteroids = False
        afterStopAsteroids = False
        delayTime = 0
        asteroids = []
        bullets = []
        energyLevel = 50

    match(settings.difficultyList.index(settings.difficulty)):
        case 0:
            #Easy
            if currentLevel == 1:
                interval = 1500
                amountOfAsteroids = 3
        case 1:
            #Medium
            if currentLevel == 1:
                interval = 1000
                amountOfAsteroids = 4
        case 2:
            #Hard
            if currentLevel == 1:
                interval = 800
                amountOfAsteroids = 5
        case 3:
            #Antje
            if currentLevel == 1:
                interval = 1500
                amountOfAsteroids = 3

    if(settings.resolutionList.index(settings.resolution) == 4):
        amountOfAsteroids = amountOfAsteroids *2
    
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
    global background, tempResolution, tempFramerate, tempDifficulty, tempVolume

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
    global background, retryButton, menuButton, previousScore, amountOfPlanets, scoreMultiplier
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

    #resets some values
    amountOfPlanets = 0
    previousScore = 0
    scoreMultiplier = 1
    

def LoadPlanetScene():
    global planet, amountOfPlanets, survivalChance, landButton, continueButton
    planet = Planet(settings.resolution[0] / 2, settings.resolution[1] / 2)
    amountOfPlanets = amountOfPlanets + 1
    maxChance = amountOfPlanets * 10
    minChance = (amountOfPlanets - 2) * 10
    if maxChance > 50:
        maxChance = 50
    if minChance < 0:
        minChance = 0
    if minChance > 40:
        minChance = 40
    survivalChance = 50 + random.randint(minChance, maxChance)

    try:
        landButton_img = pygame.image.load('Textures/Planets/StartCivilizationButton.png').convert_alpha()
        continueButton_img = pygame.image.load('Textures/Planets/FindNewPlanetButton.png').convert_alpha()
    except pygame.error as e:
        print("button images couldn't load")

    #creating button instance
    landButton = ImageButton(((240/1920)*settings.resolution[0]),((800/1920)*settings.resolution[0]), landButton_img)
    continueButton = ImageButton(((1080/1920)*settings.resolution[0]),((800/1920)*settings.resolution[0]), continueButton_img)    

    global background
    try:
        background_image = pygame.image.load('Textures/MainGame/Background.png')
        background = pygame.transform.scale(background_image, settings.resolution)
    #if loading fails it will print that in the console
    except pygame.error as e:
        print("startscreen couldn't load")

    pygame.mixer.music.load('Audio/Settings/SettingsPage.mp3')

def loadGameGewonnenScene():
    global  background, menuButton, amountOfPlanets
    #Loads the background for game over scene
    try:
        background_image = pygame.image.load('Textures/MainGame/Background.png')
        background = pygame.transform.scale(background_image, settings.resolution)
    except pygame.error as e:
        print("Game Over screen failed to load")

    try:
        menuButton_img = pygame.image.load('Textures/GameOver Screen/menuButton.png').convert_alpha()
    except pygame.error as e:
        print("button images couldn't load")

    #creating button instance
    menuButton = ImageButton(((660/1920)*settings.resolution[0]),((680/1920)*settings.resolution[0]), menuButton_img)
    #resets some values
    amountOfPlanets = 0

def mainGameLoop():
    settings.screen.blit(background, (0,0))

    #All scene specific stuff in the main game loop needs to be handled here
    if currentScene == "startscreen":
        startSceneMainGameLoop()

    if currentScene == "mainScene":
        mainSceneMainGameLoop()

    if currentScene == "gameOver":
        gameOverSceneMainGameLoop()

    if currentScene == "planet":
        planetMainGameLoop()

    if currentScene == "gameGewonnen":
        gameGewonnenMainLoop()
    
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
        global selectedTab, tempResolution, tempFramerate, tempDifficulty, tempVolume

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
        textUI.drawText((str(tempFramerate)+"FPS"), textUI.settingsFont,(153, 204, 255),(650/1920*settings.resolution[0]),(300/1080*settings.resolution[1]))
        textUI.drawText(str(tempDifficulty), textUI.settingsFont,(153, 204, 255),(650/1920*settings.resolution[0]),(400/1080*settings.resolution[1]))
        textUI.drawText(str(tempVolume), textUI.settingsFont,(153, 204, 255),(650/1920*settings.resolution[0]),(500/1080*settings.resolution[1]))

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
                    
                    if selectedTab == 0:
                        nextResolution = settings.resolutionList.index(tempResolution)+1
                        if nextResolution > len(settings.resolutionList)-1:
                            nextResolution = 0
                        tempResolution = settings.resolutionList[nextResolution]

                    if selectedTab == 1:
                        nextFramerate = settings.fpsList.index(tempFramerate)+1
                        if nextFramerate > len(settings.fpsList)-1:
                            nextFramerate = 0
                        tempFramerate = settings.fpsList[nextFramerate]

                    if selectedTab == 2:
                        nextDifficulty = settings.difficultyList.index(tempDifficulty)+1
                        if nextDifficulty > len(settings.difficultyList)-1:
                            nextDifficulty = 0
                        tempDifficulty = settings.difficultyList[nextDifficulty]

                    if selectedTab == 3:
                        nextVolume = settings.volumeList.index(tempVolume)+1
                        if nextVolume > len(settings.volumeList)-1:
                            nextVolume = 0
                        tempVolume = settings.volumeList[nextVolume]

                elif event.key == pygame.K_LEFT:
                    
                    if selectedTab == 0:
                        nextResolution = settings.resolutionList.index(tempResolution)-1
                        if nextResolution < 0:
                            nextResolution = len(settings.resolutionList)-1
                        tempResolution = settings.resolutionList[nextResolution]

                    if selectedTab == 1:
                        nextFramerate = settings.fpsList.index(tempFramerate)-1
                        if nextFramerate < 0:
                            nextFramerate = len(settings.fpsList)-1
                        tempFramerate = settings.fpsList[nextFramerate]

                    if selectedTab == 2:
                        nextDifficulty = settings.difficultyList.index(tempDifficulty)-1
                        if nextDifficulty < 0:
                            nextDifficulty = len(settings.difficultyList)-1
                        tempDifficulty = settings.difficultyList[nextDifficulty]

                    if selectedTab == 3:
                        nextVolume = settings.volumeList.index(tempVolume)-1
                        if nextVolume < 0:
                            nextVolume = len(settings.volumeList)-1
                        tempVolume = settings.volumeList[nextVolume]

                elif event.key == pygame.K_a:
                    settings.applysettings()

                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                
                if event.type == pygame.QUIT:
                    main.run = False

def startSceneMainGameLoop():
    #Draw de daadwerkelijke knoppen
    Startbutton.draw()
    Settingsbutton.draw()
    Exitbutton.draw()

    if(settings.difficultyList.index(settings.difficulty) == 3):
        textUI.drawText("Gefeliciteerd Mvr. Roestenburg!", textUI.testFont , (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-400)

    #Check voor of er op de knoppen wordt gelickt. Hoe dit precies werkt staat in de button class.
    if Startbutton.checkClicked(loadedSceneTime):
        loadScene("mainScene")

    if Settingsbutton.checkClicked(loadedSceneTime):
        loadScene("SettingsScreen")

    #Invoked de quit event zodat het eigenlijk lijkt alsof de speler op het kruisje heeft geclickt en de main function alles stopt
    if Exitbutton.checkClicked(loadedSceneTime):
        pygame.event.post(pygame.event.Event(pygame.QUIT))

#Deze wordt om de interval geupdate zodat we dingen kunnen laten spawnen om de zoveel seconden
laatsteTick = 0

def mainSceneMainGameLoop():
    global afterStopAsteroids, asteroids, bullets
    #Comments about these functions are at the functions declarations
    #afterstopAsteroids staat iets verder naar beneden uitgelegd
    if(not afterStopAsteroids):
        player.update_movement()
        player.drawerPlayerTexture()
    global laatsteTick

    current_time = pygame.time.get_ticks()
    if current_time - loadedSceneTime < 5000:
        textUI.drawText("Use WASD to move, spacebar to shoot and shift to get a boost", textUI.testFont, (225,225,225), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-150)
    if current_time - laatsteTick >= interval:
        for i in range(amountOfAsteroids):
            if (not isDead and not stopAsteroids):
                laatsteTick = current_time
                if(random.randint(3, 25) <= 5):
                    astroid = Asteroid(random.randint(0, settings.resolution[0]), 0, random.uniform(1,4), True)
                else:
                    astroid = Asteroid(random.randint(0, settings.resolution[0]), 0, random.uniform(1,4), False)
                asteroids.append(astroid)
    
    #Oke dit kan confusing zijn maar stopAsteroids = true zodra een puzzel wordt gecalled. afterStopAsteroids is pas true na een bepaalde timer zodat de player nog ff wat tijd heeft 
    #om asteroids te ontwijken
    if(stopAsteroids and not afterStopAsteroids):
        textUI.drawText("Puzzle incoming, be ready!", textUI.testFont, (225,225,225), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-100)
        if (current_time - stopAsteroidsTijd >= 2000):
            puzzels.loadRandomPuzzel()
            afterStopAsteroids = True
    

    checkCol()
    #Print time, score and level on screen
    showTimeScoreLevel(current_time)

    #Lijst van asteroids die de volgende frame weg moeten
    listOfDeletedAsteroids = []
    listOfDeletedBullets = []

    for i in range(len(asteroids)):
        astroid = asteroids[i]
        #Detect of de asteroids buiten het scherm zij
        if(astroid.y > settings.resolution[1] + 20):
            listOfDeletedAsteroids.append(i)
        astroid.draw()

    for i in range(len(bullets)):
        bullet = bullets[i]
        for j in range(len(asteroids)):
            astroid = asteroids[j]
            if bullet.rect1.colliderect(astroid.x - astroid.radius, astroid.y - astroid.radius, astroid.radius*2, astroid.radius*2) and bullet.firstAlive:
                listOfDeletedAsteroids.append(j)
                bullet.firstAlive = False
            if bullet.rect2.colliderect(astroid.x - astroid.radius, astroid.y - astroid.radius, astroid.radius*2, astroid.radius*2) and bullet.secondAlive:
                if(len(listOfDeletedAsteroids) != 0):
                    if(listOfDeletedAsteroids[len(listOfDeletedAsteroids)-1] != j):
                        listOfDeletedAsteroids.append(j)
                        bullet.secondAlive = False
                else:
                    listOfDeletedAsteroids.append(j)
                    bullet.secondAlive = False

        #Detect of de asteroids buiten het scherm zij
        if(bullet.y < 0):
            listOfDeletedBullets.append(i)
        bullet.draw()

    #Delete de asteroids van de vorige frame
    currentOffset = 0
    for i in range(len(listOfDeletedAsteroids)):
        asteroids.pop(listOfDeletedAsteroids[i]-currentOffset)
        currentOffset = currentOffset + 1
        

    currentOffset = 0
    for i in range(len(listOfDeletedBullets)):           
        bullets.pop(listOfDeletedBullets[i]-currentOffset)
        currentOffset = currentOffset + 1

def checkCol():
    global isDead, inPuzzle
    playerRect = player.player
    deletedAsteroids = []
    for i in range(len(asteroids)):
        astroid = asteroids[i]
        if playerRect.colliderect(astroid.x - astroid.radius, astroid.y - astroid.radius, astroid.radius*2, astroid.radius*2):
            if not astroid.isPuzzel and not inPuzzle:
                isDead = True
                loadScene("gameOver")
            elif astroid.isPuzzel:
                deletedAsteroids.append(i)
                global stopAsteroids, stopAsteroidsTijd
                stopAsteroids = True
                stopAsteroidsTijd = pygame.time.get_ticks()
                inPuzzle = True
        
    for i in range(len(deletedAsteroids)):
        asteroids.pop(deletedAsteroids[i])

def showTimeScoreLevel(current_time):
    global currentScore, currentLevel, speedMultiplier, scoreMultiplier, startTime, delayTime, interval, previousLevel, amountOfAsteroids, secondsTimer, previousScore

    #De timer moet niet worden laten zien als we bezig zijn met een puzzel
    if not stopAsteroids:

        #calculates current score
        if puzzels.endPuzzleTime == 0:
            currentScore = round((current_time - retryTime - delayTime) / 60 * scoreMultiplier, 0)
        else:
            currentScore = previousScore + round((current_time - puzzels.endPuzzleTime - delayTime) / 60 * scoreMultiplier, 0)

        #Increases level once score threshold has been met
        if currentScore <= 500:
            currentLevel = 1
            speedMultiplier = 1
        elif currentScore <= 1000 and currentScore >= 500:
            currentLevel = 2
            speedMultiplier = 1.5
            #decreases interval of asteroid spawn
            if currentLevel == previousLevel + 1:
                previousLevel = currentLevel
                interval = interval - 50
        elif currentScore <= 1500 and currentScore >= 1000:
            currentLevel = 3
            speedMultiplier = 2
            #decreases interval of asteroid spawn
            if currentLevel == previousLevel + 1:
                previousLevel = currentLevel
                interval = interval - 50
        elif currentScore <= 2000 and currentScore >= 1500:
            currentLevel = 4
            speedMultiplier = 2.5
            #decreases interval and amount of asteroid spawn
            if currentLevel == previousLevel + 1:
                previousLevel = currentLevel
                interval = interval - 100
                amountOfAsteroids = amountOfAsteroids + 1
        elif currentScore <= 2500 and currentScore >= 2000:
            currentLevel = 5
            speedMultiplier = 3
            #decreases interval and amount of asteroid spawn
            if currentLevel == previousLevel + 1:
                previousLevel = currentLevel
                interval = interval - 100
                amountOfAsteroids = amountOfAsteroids + 1
        elif currentScore >= 2500 + 500 * amountOfPlanets:
            currentLevel = 6 + amountOfPlanets
            loadScene("planet")
        
        #Drawing section
        secondsTimer = round((current_time - startTime - delayTime) / 1000, 1)
        #Draws Level
        textUI.drawText("Level " + str(currentLevel), textUI.testFont , (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-500)
        #Draws Time
        textUI.drawText(str(secondsTimer) + "s", textUI.testFont , (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-400)
        #Draws Score
        textUI.drawText("Score: "+ str(currentScore), textUI.testFont , (255,255,255), 120/1920*settings.resolution[0], settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-400)
        #Draws bullet energy
        if energyLevel > 2 * bulletCost:
            textUI.drawText("Energy: "+ str(energyLevel), textUI.testFont , (255,255,255), 120/1920*settings.resolution[0], settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-300)
        else:
            textUI.drawText("Energy: "+ str(energyLevel), textUI.testFont , (255,0,0), 120/1920*settings.resolution[0], settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-300)




def spawnBullets(x,y):
    global bullets
    bullet = Bullet(x,y) 
    bullets.append(bullet)

def gameOverSceneMainGameLoop():
    global retryTime
    #Draws retry and main menu button
    retryButton.draw()
    menuButton.draw()   
    textUI.drawText("Mankind went extinct!", textUI.testFont , (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-400)
    textUI.drawText("Your score: "+ str(currentScore), textUI.testFont , (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-300)
    textUI.drawText("Time survived: "+ str(secondsTimer) + "s", textUI.testFont , (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-200)

    #Restarts game and sends to main menu once buttons are clicked
    #Needs to be fixed (loadScene doesnt work properly)
    if retryButton.checkClicked(loadedSceneTime) == True:
        loadScene("mainScene")
        retryTime = pygame.time.get_ticks()

    if menuButton.checkClicked(loadedSceneTime) == True:
        loadScene("startscreen")

def planetMainGameLoop():
    planet.draw()
    textUI.drawText("New planet found!", textUI.testFont , (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-500)
    textUI.drawText("Chance of survival: " + str(survivalChance), textUI.testFont , (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-400)
    landButton.draw()
    continueButton.draw()

    if landButton.checkClicked(loadedSceneTime):
        if random.randint(0, 100) > survivalChance:
            #Humans zijn dood
            loadScene("gameOver")
        else:
            loadScene("gameGewonnen")

    if continueButton.checkClicked(loadedSceneTime):
        #Bypass dat alles wordt gereset door de functie direct te callen ipv loadScene functie
        global currentScene, delayTime
        delayTime = delayTime + pygame.time.get_ticks() - loadedSceneTime
        loadMainScene(False)
        currentScene = "mainScene"

def gameGewonnenMainLoop():
    textUI.drawText("The humans survived!", textUI.testFont , (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-400)
    textUI.drawText("Your score: "+ str(currentScore), textUI.testFont , (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-300)
    textUI.drawText("Time survived: "+ str(secondsTimer) + "s", textUI.testFont , (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-200)
    menuButton.draw()
    if menuButton.checkClicked(loadedSceneTime):
        loadScene("startscreen")
