import pygame, settings
from settings import screen

#Button class waar een image wordt geladen
class ImageButton():
        #Dit is de functie die wordt gecalled automatisch als je een nieuwe instance maakt. Hier moeten een paar standaard waarden worden gegeven.
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.Clicked = False

        #Draw de daadwerkelijke button
        def draw(self):
            #draw button on screen
            screen.blit(self.image, (self.rect.x, self.rect.y))
        
        def checkClicked(self):
            #Als de muisknop niet wordt ingedrukt kunnen we direct uit deze functie returnen met false want dan kan een knop nooit worden ingedrukt

            if not pygame.mouse.get_pressed()[0]:
                self.Clicked = False
                return False
            
            #get mouse position
            mousepos = pygame.mouse.get_pos()
            
            #Als de muis niet op de knop staat kunnen we er ook uit returnen met false
            if(not self.rect.collidepoint(mousepos)):
                return False
            
            #Als hij al wordt ingeclickt is de functie die dat gebeurd al gecalled en hoeft dat niet nog een keer te gebeuren dus returnen we false
            if(self.Clicked):
                return False

            #Alles is er nu al uitgefilterd dus dan moet de speler wel op onze knop klikken voor de eerste keer en en returnen we true
            return True

#Button class waar een rect wordt gemaakt met al een gekozen kleur. Dit is vooral handing voor de puzzels maar kan ook worden gebruikt ergens anders        
class PuzzelButton():
    #Dit is de functie die wordt gecalled automatisch als je een nieuwe instance maakt. Hier moeten een paar standaard waarden worden gegeven.
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color
        self.Clicked = False

    #Draw de daadwerkelijke button met de eerder gekozen kleur
    def draw(self):
        #draw button on screen
        pygame.draw.rect(settings.screen, self.color, self.rect)

    #Dit komt overeen met de functie die in de image button class staat dus daar staan ook alle comments     
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
