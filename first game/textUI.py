import pygame, settings

testFont = 0

def init():
    global testFont
    testFont = pygame.font.SysFont("Arial", 30)

def drawText(text, font, text_col, x,y):
    img = font.render(text, True, text_col)
    x = x - img.get_width() / 2
    y = y - img.get_height() / 2
    settings.screen.blit(img, (x,y))