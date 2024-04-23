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
        if self.isPuzzel : pygame.draw.circle(settings.screen, (255,0,0), (self.x, self.y + self.velocity), 20)
        elif not self.isPuzzel : pygame.draw.circle(settings.screen, (0,0,0), (self.x, self.y + self.velocity), 20)
        self.y = self.y + self.velocity

