import pygame, settings

testFont = 0
settingsFont = 0
survivedFont = 0
mathFont = 0

#De testfont moet worden geassigned, als je dit niet in deze functie doet, doet pygame moeilijk
def init():
    global testFont, settingsFont, survivedFont, mathFont
    testFont = pygame.font.SysFont("Arial", int(30/1920*settings.resolution[0]), bold=True)
    settingsFont = pygame.font.SysFont("Arial", int(50/1920*settings.resolution[0]), bold=True)
    survivedFont = pygame.font.SysFont("Arial", int(40/1920*settings.resolution[0]), bold=True)
    mathFont = pygame.font.SysFont("Arial", int(50/1920*settings.resolution[0]), bold=True)

#Eigenlijk maken we een image van de tekst en blitten we die daarna zoals altijd
def drawText(text, font, text_col, x,y):
    img = font.render(text, True, text_col)
    #Dit zorgt ervoor dat de x en y coordinaten die je geeft altijd het center is
    x = x - img.get_width() / 2
    y = y - img.get_height() / 2
    settings.screen.blit(img, (x,y))
    return int(img.get_width() / 2)

def drawTextNotCentered(text, font, text_col, x,y):
    img = font.render(text, True, text_col)
    #Dit zorgt ervoor dat de y coordinaten die je geeft altijd het center is
    y = y - img.get_height() / 2
    settings.screen.blit(img, (x,y))
    
