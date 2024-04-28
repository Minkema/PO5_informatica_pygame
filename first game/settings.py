import pygame

#these are lists with all the options that a setting can have
difficultyList = ["Easy", "Medium", "Hard", "Antje"]
resolutionList = [[2560,1440],[1920,1080],[1366,768],[1280,1024],[1024,768]]
fpsList = [120, 60, 30]
volumeList = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

#Here you can find the different settings (Some of them can't be changed. That's why they don't have a list)
resolution = resolutionList[1] #resolution is done with a list so you can change it easier using code. This can be helpfull for resolution settings.
playerY = resolution[1] / 2 #defines the starting y position
playerX = resolution[0] / 2 #defines the starting x position
playerWidht = (75/1920) * resolution[0]
playerHeight = (113/1920) * resolution[0]
screen = pygame.display.set_mode((resolution))
fps = fpsList[0] #defines the amount of frames per second
difficulty = difficultyList[0]
volume = volumeList[0]

def applysettings():
    pygame.mixer_music.set_volume(volume/100)
