import random, pygame, settings

numberOfPuzzels = 1
colors = [
    (255,0,0), #Rood
    (0,255,0), #Groen
    (0,255,0), #Blauw
    (255, 255, 0) #Geel
]
squaresRect = pygame.Rect(0,0,200, 200)
intervalBetweenSquares = 250
startEersteGame = 0
currentPuzzel = "none"

def loadRandomPuzzel():
    randomPuzzel = random.uniform(1,numberOfPuzzels)

    match randomPuzzel:
        case 1:
            global currentPuzzel
            global startEersteGame

            loadEerstePuzzel()
            startEersteGame = pygame.time.get_ticks()
            currentPuzzel = "eerste"
        case _:
            print("Error random puzzel out of bounds")

def loadEerstePuzzel():
    random.shuffle(colors)
        
def mainGameLoop():
    if(currentPuzzel == "none"):
        return
    
    elif(currentPuzzel == "eerste"):
        currentTime = pygame.time.get_ticks()
        timeInBetween = currentTime - startEersteGame
        if(timeInBetween <= intervalBetweenSquares):
            #eerste
            pygame.draw.rect(settings.screen, colors[0], squaresRect)
        elif(timeInBetween >= intervalBetweenSquares and timeInBetween <= (2 * intervalBetweenSquares)):
            #tweede
            pygame.draw.rect(settings.screen, colors[1], squaresRect)
        elif(timeInBetween >= 2 * intervalBetweenSquares and timeInBetween <= (3 * intervalBetweenSquares)):
            #Derde
            pygame.draw.rect(settings.screen, colors[2], squaresRect)
        elif(timeInBetween >= 3 * intervalBetweenSquares and timeInBetween <= (4 * intervalBetweenSquares)):
            #Vierde
            pygame.draw.rect(settings.screen, colors[3], squaresRect)
