import settings, pygame, scenehandler,random


class Astroid:
    #Dit is de functie die wordt gecalled automatisch als je een nieuwe instance maakt. Hier moeten een paar standaard waarden worden gegeven.
    def __init__(self, x, y, velocity, isPuzzel):
        self.x = x
        self.y = y
        self.velocity = velocity * scenehandler.speedMultiplier
        self.isPuzzel = isPuzzel
        self.radius = random.randint(38, 42)
        if isPuzzel:
            self.image = pygame.image.load("Textures/MainGame/asteroidpuzzel.png")
            self.image = pygame.transform.scale(self.image, (self.radius*2, self.radius*2))
        else:
            self.image = pygame.image.load("Textures/MainGame/asteroid" + str(random.randint(1,3)) + ".png")
            self.image = pygame.transform.scale(self.image, (self.radius*2, self.radius*2))
        
    #Draw de daadwerkelijke astroid
    def draw(self):
        settings.screen.blit(self.image, (self.x - self.image.get_width() / 2, self.y - self.image.get_height() / 2 + self.velocity))

        self.y = self.y + self.velocity


class Planet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.image = pygame.image.load('Textures/Planets/Planet0.png').convert_alpha()
        self.tempImage = 0

    def draw(self):
        if self.size < ((600/1920)*settings.resolution[0]):
            self.size = self.size + 10
            self.tempImage = pygame.transform.scale(self.image, (self.size, self.size))
        settings.screen.blit(self.tempImage, (self.x - self.tempImage.get_width() / 2, self.y - self.tempImage.get_height() / 2))
        