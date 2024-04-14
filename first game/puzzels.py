import random, pygame, settings, textUI, scenehandler
from textUI import drawText
from button import PuzzelButton

numberOfPuzzels = 1
currentPuzzel = "none"

#Dit is allemaal voor de eerste puzzel:

#Lijst met kleuren die worden geshufeld
colors = [
    (255,0,0), #Rood
    (0,255,0), #Groen
    (0,0,255), #Blauw
    (255, 255, 0) #Geel
]
squareWidth, squareHeight = 200, 200
squaresRect = pygame.Rect(settings.resolution[0] / 2 - squareWidth / 2, settings.resolution[1] / 2 - squareHeight / 2, squareWidth, squareHeight)

#Hoeveel tijd er tussen de vierkanten op het scherm zit bij de eerste puzzel
intervalBetweenSquares = 250
startEersteGame = 0

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

#Zorgt ervoor dat de kleuren een andere volgorde krijgt
def loadEerstePuzzel():
    random.shuffle(colors)
        
def mainGameLoop():
    if(currentPuzzel == "none"):
        return
    
    elif(currentPuzzel == "eerste"):
        currentTime = pygame.time.get_ticks()
        
        #De 3000 staat voor de 3 seconde die verloren gaan in de countdown. Die 3 seconden moeten we negeren
        timeInBetween = currentTime - startEersteGame - 3000

        #De startcountdown functie return false als hij nog bezig is met de countdown. Als hij al klaar is return hij true en kunnen we verder.
        if startCountdown(timeInBetween + 3000):
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
            else:
                checkSolEerste()

#Hoeveel de speler er al goed heeft
currentNum = 0

#Dit bewaardt x en y posities zodat we later de text op de knoppen kunnen laten zien. Dit is niet zo netjes hoe ik het nu heb gedaan maar kan ff niks beters bedenken
posOfButtonsX = [0,0,0,0]
posOfButtonsY = [0,0,0,0]

#De al geclickte knoppen lijst zodat als een speler nog een keer op een knop klikt perongeluk het spel het gwn kan negeren
buttonsClicked = [False, False, False, False]

#Init alle buttons en maak een lijst zodat we er straks doorheen kunnen loopen
RedButton = PuzzelButton(pygame.Rect(-100 + settings.resolution[0] / 2, settings.resolution[1]/ 2, 50, 50), (255,0,0))
GreenButton = PuzzelButton(pygame.Rect(-50 + settings.resolution[0] / 2, settings.resolution[1]/ 2, 50, 50), (0,255,0))
BlueButton = PuzzelButton(pygame.Rect(50 + settings.resolution[0] / 2, settings.resolution[1]/ 2, 50, 50), (0,0,255))
YellowButton = PuzzelButton(pygame.Rect(100 + settings.resolution[0] / 2, settings.resolution[1]/ 2, 50, 50), (255,255,0))
buttons = [RedButton, GreenButton, BlueButton, YellowButton]

def checkSolEerste():
    drawText("Click de vakjes in de juiste volgorde", textUI.testFont, (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-200)
    global currentNum, currentPuzzel    
    
    #Player heeft ze goed opgelost
    if(currentNum == 4):
        currentPuzzel = "none"
        scenehandler.stopAstroids = False
        scenehandler.afterStopAstroids = False
        scenehandler.delayTime = pygame.time.get_ticks() - scenehandler.stopAstroidsTijd
        scenehandler.stopAstroidsTijd = 0
        return

    #Check continue of knoppen worden geclicked
    for i in range(0,4):
        buttons[i].draw()
        if(buttons[i].checkClicked()):

            #Check of de kleur van de geclickte knop overeen komt met de kleur die op dit moment moet worden gekozen
            if(colors[currentNum] == buttons[i].color):
                #Ze hebben de goede gekozen
                if(not buttonsClicked[i]):
                    posOfButtonsX[currentNum] = buttons[i].rect.x 
                    posOfButtonsY[currentNum] = buttons[i].rect.y
                    buttonsClicked[i] = True 
                    currentNum += 1
            else:
                #Ze hebben de verkeerde gekozen
                if not buttonsClicked[i]: 
                    currentPuzzel = "none"
                    scenehandler.loadScene("gameOver")

    #Laat de nummers zien van de al gekozen vakjes
    if(not currentNum == 0):
        for i in range(0, currentNum):
            drawText(str(i+1), textUI.testFont, (255,255,255), posOfButtonsX[i] + 25, posOfButtonsY[i] + 25)

def startCountdown(timeInBetween):
    if(timeInBetween < 1000):
        drawText("Onthoud de volgorde!", textUI.testFont, (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-100)
        drawText("3", textUI.testFont, (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-200)
        return False
    if(timeInBetween < 2000):
        drawText("Onthoud de volgorde!", textUI.testFont, (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-100)
        drawText("2", textUI.testFont, (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-200)
        return False
    if(timeInBetween < 3000):
        drawText("Onthoud de volgorde!", textUI.testFont, (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-100)
        drawText("1", textUI.testFont, (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 *-200)
        return False

    return True
