import pygame, settings

class Bullet:
    def __init__(self, x, y):
        self.x1 = x + settings.playerWidht * 0.2
        self.x2 = x + settings.playerWidht * 0.8
        self.y = y + 18/1080 * settings.resolution[1]
        self.rect1 = pygame.Rect(self.x1, self.y, 5, 15)
        self.rect2 = pygame.Rect(self.x2, self.y, 5, 15)
        self.velocity = 25
        self.firstAlive = True
        self.secondAlive = True

    def draw(self):
        self.y = self.y - self.velocity
        self.rect1.y = self.y
        self.rect2.y = self.y
        if self.firstAlive:
            pygame.draw.rect(settings.screen, (0,255,0), self.rect1)
        if self.secondAlive:
            pygame.draw.rect(settings.screen, (0,255,0), self.rect2)
    

        