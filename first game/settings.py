import pygame

resolution = [1920,1080] #resolution is done with a list so you can change it easier using code. This can be helpfull for resolution settings.
playerY = resolution[1] / 2 #defines the starting y position
playerX = resolution[0] / 2 #defines the starting x position
playerWidht = (100/1920) * resolution[0]
playerHeight = (150/1920) * resolution[0]
screen = pygame.display.set_mode((resolution))
fps = 120 #defines the amount of frames per second