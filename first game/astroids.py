import settings, pygame


class Astroid:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.velocity = velocity

    def draw(self):
        self.object = pygame.draw.circle(settings.screen, (0,0,0), (self.x, self.y + self.velocity), 20)
        self.y = self.y + self.velocity

