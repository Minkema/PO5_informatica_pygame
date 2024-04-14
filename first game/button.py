import pygame
from settings import screen

class Button():
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.Clicked = False

        def draw(self):
            #draw button on screen
            screen.blit(self.image, (self.rect.x, self.rect.y))

        def checkClicked(self):
            if not pygame.mouse.get_pressed()[0]:
                self.Clicked = False
                return False
            
            #get mouse position
            mousepos = pygame.mouse.get_pos()
            
            if(not self.rect.collidepoint(mousepos)):
                return False
            
            if(self.Clicked):
                return False

            return True