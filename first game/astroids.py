import settings, pygame, scenehandler


class Astroid:
    #Dit is de functie die wordt gecalled automatisch als je een nieuwe instance maakt. Hier moeten een paar standaard waarden worden gegeven.
    def __init__(self, x, y, velocity, isPuzzel):
        self.x = x
        self.y = y
        self.velocity = velocity * scenehandler.speedMultiplier
        self.isPuzzel = isPuzzel
        
    #Draw de daadwerkelijke astroid
    def draw(self):
        if self.isPuzzel : pygame.draw.circle(settings.screen, (255,0,0), (self.x, self.y + self.velocity * 60/settings.fps), 20)
        elif not self.isPuzzel : pygame.draw.circle(settings.screen, (0,0,0), (self.x, self.y + self.velocity * 60/settings.fps), 20)
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
        