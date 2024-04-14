import settings, pygame


class Astroid:
    #Dit is de functie die wordt gecalled automatisch als je een nieuwe instance maakt. Hier moeten een paar standaard waarden worden gegeven.
    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.velocity = velocity
        
    #Draw de daadwerkelijke astroid
    def draw(self):
        self.object = pygame.draw.circle(settings.screen, (0,0,0), (self.x, self.y + self.velocity), 20)
        self.y = self.y + self.velocity

