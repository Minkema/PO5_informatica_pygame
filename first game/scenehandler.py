import pygame, settings, player, random
from astroids import Astroid

currentScene = "default"
resolution = settings.resolution
screen = settings.screen
music_active = False

astroids = []

def loadScene(scenename):
    #All specific sceneloading stuff needs to be handeld here
    global currentScene
    currentScene = scenename

    if(scenename == "startscreen"):
        loadStartScene()
    if(scenename == "testScene"):
        loadTestScene()

def loadTestScene():
    player.loadPlayer()
    #Tries to load the specific background textures
    global background
    try:
        background_image = pygame.image.load('Textures/StartScreen/homescreen.png')
        background = pygame.transform.scale(background_image, resolution)
    #if loading fails it will print that in the console
    except pygame.error as e:
        print("startscreen couldn't load")

def loadStartScene():
    #defining variables
    global background
    global StartButton_img
    global SettingsButton_img
    global ExitButton_img
    global Startbutton
    global Settingsbutton
    global Exitbutton

    #Loads the music in pygame so that it can be used later in the scene loop
    pygame.mixer.music.load('Audio\Startscreen\startscreen.mp3')
    
    #Tries to load the specific background textures
    try:
        background_image = pygame.image.load('Textures/StartScreen/homescreen.png')
        background = pygame.transform.scale(background_image, resolution)
    #if loading fails it will print that in the console
    except pygame.error as e:
        print("startscreen couldn't load: ", e)

    #loading button textures
    try:
        StartButton_img = pygame.image.load('Textures/StartScreen/StartButton.png').convert_alpha()
        SettingsButton_img = pygame.image.load('Textures/StartScreen/SettingsButton.png').convert_alpha()
        ExitButton_img = pygame.image.load('Textures/StartScreen/ExitButton.png').convert_alpha()
    except pygame.error as e:
        print("button images couldn't load")
    

    #button class
    class Button():
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)

        def draw(self):
            #draw button on screen
            screen.blit(self.image, (self.rect.x, self.rect.y))

    #creating button instance
    Startbutton = Button(((100/1920)*resolution[0]),((800/1920)*resolution[0]), StartButton_img)
    Settingsbutton = Button(((100/1920)*resolution[0]),((600/1920)*resolution[0]), SettingsButton_img)
    Exitbutton = Button(((100/1920)*resolution[0]),((400/1920)*resolution[0]), ExitButton_img)

    Startbutton.draw()
    Settingsbutton.draw()
    Exitbutton.draw()

last_execution_time = pygame.time.get_ticks()
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
    
    if currentScene == "testScene":
        #Comments about these functions are at the functions declarations
        player.drawPlayer()
        player.update_movement()
        player.drawerPlayerTexture()
        global last_execution_time

        current_time = pygame.time.get_ticks()
        if current_time - last_execution_time >= interval:
            for i in range(5):
                last_execution_time = current_time
                astroid = Astroid(random.randint(0, resolution[0]), 0, random.uniform(1,4))
                astroids.append(astroid)

        for astroid in astroids:
            astroid.draw()
