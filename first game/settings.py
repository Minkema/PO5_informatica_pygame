import pygame

difficultyList = ["Easy", "Medium", "Hard", "Antje"]
resolutionList = [[2560,1440],[1920,1080],[1366,768],[1280,1024],[1024,768]]
fpsList = [120, 60, 30]

resolution = resolutionList[1] #resolution is done with a list so you can change it easier using code. This can be helpfull for resolution settings.
playerY = resolution[1] / 2 #defines the starting y position
playerX = resolution[0] / 2 #defines the starting x position
playerWidht = (75/1920) * resolution[0]
playerHeight = (113/1920) * resolution[0]
screen = pygame.display.set_mode((resolution))
fps = fpsList[0] #defines the amount of frames per second
difficulty = difficultyList[0]
