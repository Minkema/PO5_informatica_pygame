import random, pygame, settings, textUI, scenehandler
from textUI import drawText, drawTextNotCentered
from button import PuzzelButton, MathImageButton

numberOfPuzzels = 3
currentPuzzel = "none"
endPuzzleTime = 0

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
intervalBetweenSquares = 350
startPuzzleTime = 0

def loadRandomPuzzel():
    randomPuzzel = random.randint(1,numberOfPuzzels)
    global currentPuzzel, startPuzzleTime
    match randomPuzzel:
        case 1:
            loadEerstePuzzel()
            currentPuzzel = "eerste"
            startPuzzleTime = pygame.time.get_ticks()
        case 2:
            keybindPuzzleLoad()
            currentPuzzel = "keybindPuzzle"
        
        case 3:
            mathsLoadPuzzle()
            currentPuzzel = "mathsPuzzle"

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
        timeInBetween = currentTime - startPuzzleTime - 3000

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
    
    elif(currentPuzzel == "keybindPuzzle"):
        keybindPuzzle()
    
    elif(currentPuzzel == "mathsPuzzle"):
        mathsPuzzle()

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
    global currentNum, currentPuzzel, endPuzzleTime  
    
    #Player heeft ze goed opgelost
    if(currentNum == 4):
        currentPuzzel = "none"
        #increases score gain if puzzle has been completed succesfully
        scenehandler.scoreMultiplier = scenehandler.scoreMultiplier + 1
        scenehandler.energyLevel = scenehandler.energyLevel + 25
        ResetEerstePuzzel()
        #sets score prior to level
        scenehandler.previousScore = scenehandler.currentScore
        #gets time when puzzle end
        endPuzzleTime = pygame.time.get_ticks()
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
                    endPuzzleTime = 0
                    ResetEerstePuzzel()
                    scenehandler.loadScene("gameOver")

    #Laat de nummers zien van de al gekozen vakjes
    if(not currentNum == 0):
        for i in range(0, currentNum):
            drawText(str(i+1), textUI.testFont, (255,255,255), posOfButtonsX[i] + 25, posOfButtonsY[i] + 25)

def ResetEerstePuzzel():
    global currentNum, posOfButtonsX, posOfButtonsY, buttonsClicked
    currentNum = 0

    posOfButtonsX = [0,0,0,0]
    posOfButtonsY = [0,0,0,0]

    buttonsClicked = [False, False, False, False]
    scenehandler.stopAstroids = False
    scenehandler.afterStopAstroids = False
    scenehandler.delayTime = pygame.time.get_ticks() - scenehandler.stopAstroidsTijd
    scenehandler.stopAstroidsTijd = 0

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


#keybindpuzzle variables
abcDict = {"  A":pygame.K_a, "  B":pygame.K_b, "  C":pygame.K_c, "  D":pygame.K_d, "  E":pygame.K_e, "  F":pygame.K_f, "  G":pygame.K_g, "  H":pygame.K_h, "  I":pygame.K_i, "  J":pygame.K_j, "  K":pygame.K_k, "  L":pygame.K_l, "  M":pygame.K_m,
           "  N":pygame.K_n, "  O":pygame.K_o, "  P":pygame.K_p, "  Q":pygame.K_q, "  R":pygame.K_r, "  S":pygame.K_s, "  T":pygame.K_t, "  U":pygame.K_u, "  V":pygame.K_v, "  W":pygame.K_w, "  X":pygame.K_x, "  Y":pygame.K_y, "  Z":pygame.K_z}
abcList = ["  A","  B","  C","  D","  E","  F","  G","  H","  I","  J","  K","  L","  M","  N","  O","  P","  Q","  R","  S","  T", "  U","  V","  W","  X","  Y","  Z"]
inputLetterList = []
inputKeyList = []
keystring = ""
textBackground = 0
currentIndex = 0  

#preparation for keybindpuzzle
def keybindPuzzleLoad():
    global keystring, textBackground
    random.shuffle(abcList)

    #loads backgroundimage for text
    try:
        textBackground_Image = pygame.image.load("Textures/Puzzles/backgroundText.png")
        textBackground = pygame.transform.scale(textBackground_Image, (400, 60))
    except:
        print("Image couldn't load")

    #letters van ABC list verplaatsen naar writeable string
    for i in range(0,10):
        keystring = keystring + abcList[i]
        inputLetterList.append(abcList[i])

    for letter in inputLetterList:
        inputKeyList.append(abcDict.get(letter))
    
#mainloop for keybind puzzle
def keybindPuzzle():

    global currentPuzzel, currentNum, currentIndex, keystring, endPuzzleTime
    events = pygame.event.get()
    keystring2 = keystring[0:currentIndex + 1]

    #Stops puzzle once correctly completed
    if (currentNum == 10):
        #increases score gain if puzzle has been completed succesfully
        scenehandler.scoreMultiplier = scenehandler.scoreMultiplier + 1
        scenehandler.energyLevel = scenehandler.energyLevel + 25
        currentPuzzel = "none"
        #sets score prior to level
        scenehandler.previousScore = scenehandler.currentScore
        #gets time when puzzle ended
        endPuzzleTime = pygame.time.get_ticks()
        resetKeybindPuzzel()
        return
    
    #Checks for correct key input
    for event in events: 
        if event.type == pygame.KEYDOWN:
            #Progresses puzzle if correct input was made
            if event.key == inputKeyList[currentNum]:
                currentNum = currentNum + 1
                currentIndex = currentIndex + 3
            #Fails puzzle if incorrect input was made
            elif event.key != inputKeyList[currentNum]:
                currentPuzzel = "none"
                resetKeybindPuzzel()
                endPuzzleTime = 0
                scenehandler.loadScene("gameOver")

    #Background image for random letter order
    settings.screen.blit(textBackground, (settings.resolution[0] / 2 - textBackground.get_width() / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 * 50 - textBackground.get_height() / 2) )

    #Tells player what to do (text)
    drawText("Type the keys in the correct order!", textUI.testFont, (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 * 20 )

    #Draws random letter order on screen
    drawText(keystring, textUI.testFont, (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 * 50 )
    #Says where random text x-cords start
    extraWidth = int(drawText(keystring, textUI.testFont, (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 * 50 )) 
    #shows which letters have been typed
    drawTextNotCentered(keystring2, textUI.testFont, (255,0,0), settings.resolution[0] / 2 - extraWidth, settings.resolution[1] / 2 + settings.resolution[1] / 1080 * 50 )

#resets keybind puzzle  
def resetKeybindPuzzel():
    global currentNum, keystring, inputKeyList, inputLetterList, currentIndex
    currentNum = 0
    
    keystring = ""
    currentIndex = 0
    inputKeyList = []
    inputLetterList = []

    scenehandler.stopAstroids = False
    scenehandler.afterStopAstroids = False
    scenehandler.delayTime = pygame.time.get_ticks() - scenehandler.stopAstroidsTijd
    scenehandler.stopAstroidsTijd = 0


#variables for math puzzle
correctNum = 0
operatorRandom = 0
operatorList = [" + ", " - ", " / ", " x "]
firstRandomNum = 0
secondRandomNum = 0
answerTwo = 0
answerThree = 0
answerFour = 0
answerList = []
mathString = ""
answerButtons = []
topRight = 0
topLeft = 0
bottomRight = 0
bottomLeft = 0

def mathsLoadPuzzle():
    global operatorRandom, correctNum, firstRandomNum, secondRandomNum, answerList, mathString, answerTwo, answerThree, answerFour, answerButtons
    #chooses random operator
    operatorRandom = random.randint(0, 3)
    #chooses random numbers
    firstRandomNum = random.randint(1, 100)
    secondRandomNum = random.randint(1, 100)
    #finds correct answer
    if operatorRandom == 0:
        correctNum = firstRandomNum + secondRandomNum
    elif operatorRandom == 1:
        correctNum = firstRandomNum - secondRandomNum
    elif operatorRandom == 2:
        correctNum = round(firstRandomNum / secondRandomNum, 1)
    elif operatorRandom == 3:
        correctNum = firstRandomNum * secondRandomNum
    mathString = str(firstRandomNum) + operatorList[operatorRandom] + str(secondRandomNum) + " ="

    #Creates list with 4 possible answers (1 correct)
    answerTwo = correctNum + random.randint(0, 40)
    answerThree = correctNum - random.randint(0, 40)
    answerFour = round(correctNum * random.randint(2, 3), 1)

    answerList = [correctNum, answerTwo, answerThree, answerFour]
    #randomizes the order of answerList
    random.shuffle(answerList)

    #Loads image for buttons
    try:
        answerButtons_img = pygame.image.load('Textures/Puzzles/backgroundText.png').convert_alpha()
    except pygame.error as e:
        print("button images couldn't load")
    
    #creating button instance
    topRight = MathImageButton((100 + settings.resolution[0] / 2),(-200 + settings.resolution[1]/ 2), answerButtons_img)
    topLeft = MathImageButton((-350 + settings.resolution[0] / 2),(-200 + settings.resolution[1]/ 2), answerButtons_img)
    bottomRight = MathImageButton((100 + settings.resolution[0] / 2),(200 + settings.resolution[1]/ 2), answerButtons_img)
    bottomLeft = MathImageButton((-350 + settings.resolution[0] / 2),(200 + settings.resolution[1]/ 2), answerButtons_img)

    answerButtons = [topRight, topLeft, bottomRight, bottomLeft]

def mathsPuzzle():
    global mathString, answerButtons, correctNum, currentPuzzel, endPuzzleTime
    #Draws the math problem
    drawText(mathString, textUI.mathFont, (255,255,255), settings.resolution[0] / 2, settings.resolution[1] / 2 + settings.resolution[1] / 1080 * 20 )
    #draws buttons
    for i in range(0, 4):
        answerButtons[i].draw(answerList[i])
        if (answerButtons[i].checkClicked(0)):
            if answerList[i] == correctNum:
                currentPuzzel = "none"
                #increases score gain if puzzle has been completed succesfully
                scenehandler.scoreMultiplier = scenehandler.scoreMultiplier + 1
                scenehandler.energyLevel = scenehandler.energyLevel + 25
                #Gets time when puzzle ended
                endPuzzleTime = pygame.time.get_ticks()
                #Resets asteroids
                scenehandler.stopAstroids = False
                scenehandler.afterStopAstroids = False
                scenehandler.delayTime = pygame.time.get_ticks() - scenehandler.stopAstroidsTijd
                scenehandler.stopAstroidsTijd = 0
                #sets score prior to level
                scenehandler.previousScore = scenehandler.currentScore
            #fails puzzle if wrong answer was chosen
            else:
                currentPuzzel = "none"
                endPuzzleTime = 0
                scenehandler.loadScene("gameOver")

