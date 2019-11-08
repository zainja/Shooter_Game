import datetime, time
import os
from difflib import SequenceMatcher

#size of the item length 
#decided in the stringMargin method
sizeX = 0
# predefined width for the box that will contain items
DEFAULT_SIZE_X=50  
sizeY = 8
# takes an input of list of contents that need to be printed in a box
# creates an artificial spaces around the item to fit it in the box
# if the list is less than 8 elemnts it will add empty string items
#if any item in the list is longer than 50 the box is resized to fit it
# to keep the box at a standard height
def stringMargin(listOfItemsForBox):
   
    #resize the height of the box
    listOfItemsForBox.append("")
    while len(listOfItemsForBox) < sizeY: 
       listOfItemsForBox.append("")

    # refere to the outer sizeX
    global sizeX
    
    sizeX = len(max(listOfItemsForBox, key=len)) + 10
    if sizeX < DEFAULT_SIZE_X : 
        sizeX = DEFAULT_SIZE_X
    # the final output of the function
    modifiedList = []  
    for item in listOfItemsForBox :
        # calculates needed length
        needed_length = sizeX - len(item)  
         # a standard right intended
        rightIndent = 6 
        if item == listOfItemsForBox[0]:
            rightIndent = 3
        leftIndent = needed_length - rightIndent
        leftMargin = len(item) + leftIndent 

         # creates left margin
        item = item.ljust(leftMargin) 
        rightMargin = len(item) + rightIndent  
         # adds right indent spaces into the item
        item = item.rjust(rightMargin, " ") 
        modifiedList.append(item)
    return modifiedList

# function to generate a box
#takes input for the actual content of the box
#outputs a box
def boxGenerator(listOfContent):
	# clears the terminal before the box so the box stays on top
    os.system('clear')

    #takes the input list to stringMargin() to modify it
    listOfContent = stringMargin(listOfContent)

    # prints a corner then stays in the same line
    print(u'\u250F', end="", flush=True)
    for i in range(0, sizeX):
    	# prints the top-bar
        print(u'\u2501', end="", flush=True) 
	
	# prints a corner 
    print(u'\u2513')  

    #  the body of the box
    for i in range(0, len(listOfContent)):
        # prints a vertical pipe
        print(u'\u2503', end="", flush=True)

        #prints the actual content with spaces around it
        print(listOfContent[i], end="", flush=True)

        # prints a vertical pipe
        print(u'\u2503')

    # prints a T style corner
    print(u'\u2523', end="", flush=True)

    # prints the bottom bar
    for i in range(0, sizeX):
    	# prints a horizontal bar
        print(u'\u2501', end="", flush=True)

    # prints a corner
    print(u'\u251B')

    #prints a corner
    print(u'\u2517', end="", flush=True)

    # prints a vertical line
    for i in range(0, 15):
        print(u'\u2501', end="", flush=True)

#cleans the sentence from special characters
def sentenceModification(sentence):
    sentence = sentence.lstrip().rstrip().lower()
    for chars in sentence:
        if not chars.isalpha() and chars !=" ":
            sentence = sentence.replace(chars, "")
    return sentence

#dictionary that contains word counts
fileWordsInformation = {
    'total Number of words': 0,
    'correctly spelt words': 0,
    'incorrectly spelt words': 0,
    'ignored words': 0,
    'marked words': 0,
    'words added to dictionary': 0
}

# checks words in sentences
def checkWordsForSentences(sentence):
    #cleans the sentence from any special characters
    sentence = sentenceModification(sentence)
    #splits the sentence into list of words
    listofWords = sentence.split()
    fileWordsInformation["total Number of words"] = len(listofWords)
    fileWordsInformation["correctly spelt words"] = 0
    fileWordsInformation["incorrectly spelt words"] = 0

    #irretates through the list of words to find any matching in the dictionary
    #prints the word is spelt correctly if it was found in the dictionary
    for word in listofWords:
        if word in EnglishWords:
            boxGenerator(["W O R D     F O U N D", "", "", word,
            "Spelt correctly"])
            #introduce a lag so the screen above does not disapper
            # if next screens come
            dummyInput = input("enter any key to go next")
            fileWordsInformation["correctly spelt words"] += 1
        else:
            boxGenerator(["W O R D   N O T  F O U N D", "", "", word,
             "Not found in dictionary"])
            dummyInput = input("enter any key to go next")
            fileWordsInformation["incorrectly spelt words"] += 1
    finalBoxList = ["F I N A L   R E S U L T", ""]

    #prints the fileWordsInformation which contains number of words,
    # spelt correctly not spelt correctly
    for x, y in fileWordsInformation.items():
        tempStr = "Number of " + x + " : " + str(y)
        finalBoxList.append(tempStr)
        #to not print the file related counts
        if len(finalBoxList) == 5:
            break
    #generate final information
    boxGenerator(finalBoxList)

#a funtion to spell check for words
#takes the input for the file and file name 
#creates a file with the name 2+file name 
#saves the spellchecked words to the new file 
#offeres the user the chance to use other words
#instead of the incorrect ones 
def checkWordsForFiles(sentence, file):
    sentence = sentenceModification(sentence)
    listofWords = sentence.split()
    fileWordsInformation["total Number of words"] = len(listofWords)
    correctedWords = ""
    resultFile = open("2" + file, "w")
    for word in listofWords:
        if word in EnglishWords:
            correctedWords += word + " "
            fileWordsInformation["correctly spelt words"] += 1
        # case the word is spelt incorrectly
        else:
            fileWordsInformation["incorrectly spelt words"] += 1
            listOfRaitos = []
            wordsFromRatios = []
            #saves the list of all ratios against the word from dictonary
            for matchedWord in EnglishWords:
                ratio = SequenceMatcher(None, matchedWord, word).ratio()
                listOfRaitos.append(ratio)
            desiredInput = False
            # insure correct input from the user
            while not desiredInput:
            	#takes the maximum ratio available to the word 
                requiredWordIndex = listOfRaitos.index(max(listOfRaitos))
                desiredWord = EnglishWords[requiredWordIndex]
                boxGenerator(["W O R D   N O T   F O U N D", "", word, "", "did you mean", "", desiredWord])
                changeWordInput = input(" Enter [y] or [n]: ")
                print("\n")
                if changeWordInput == "y":
                    correctedWords += desiredWord + " "
                    desiredInput = True

                #in case the user wants to save the word to a dictionary
                #or mark as incorrect or ignore it
                elif changeWordInput == "n":
                    desiredInput = True
                    correctInput = False
                    # asks the user to add the word into dictionart
                    # ignore the word or mark it
                    # while loop is to ensure correct input from the user 
                    while not correctInput:
                        boxGenerator(["W O R D   N O T   F O U N D", "", word, "", "1. Ignore the word.",
                                      "2. Mark the word as incorrect.", "3. Add word to dictionary."])
                        incorrectWordsHandling = input(" Enter choice: ")
                        print("\n")
                        if incorrectWordsHandling == "1":
                            correctedWords += "!" + word + "! "
                            fileWordsInformation["ignored words"] += 1
                            correctInput = True
                        elif incorrectWordsHandling == "2":
                            correctedWords += "?" + word + "? "
                            fileWordsInformation["marked words"] += 1
                            correctInput = True
                        elif incorrectWordsHandling == "3":
                            correctedWords += "*" + word + "* "
                            fileWordsInformation["words added to dictionary"] += 1
                            englishDict.write("\n" + word)
                            correctInput = True
    #prints the data into the corrected file
    resultFile.write(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S\n"))
    resultFile.write("\n")
    finalBoxList = ["F I N A L   R E S U L T", ""]
    for x, y in fileWordsInformation.items():
        tempStr = "Number of " + x + " : " + str(y)
        temp2Str = tempStr + "\n"
        finalBoxList.append(tempStr)
        resultFile.write(temp2Str)
    resultFile.write("\n")
    #writes all the words after correction to the file 
    resultFile.write(correctedWords)
    resultFile.close()

    #generates feedback with word counts, correct, incorrect,ignored...etc
    boxGenerator(finalBoxList)
    dummyInput = input(" enter any key to go next ")

# the main screen
terminated = False
englishDictReadOnly = open("EnglishWords.txt")
# creates a list to contain the words in the file
EnglishWords = englishDictReadOnly.read().split("\n") 
englishDictReadOnly.close()
# reopens the file in append mode so it can be edited
englishDict = open("EnglishWords.txt", "a")  
while not terminated:
	
	#generates the main screen  
    boxGenerator(["S P E L L   C H E C K E R", "", "1. Check a file", "2. Check a sentence", "", "", "0.Quit"])
    usrInput = input(" Enter choice: ")

    # file mode
    if usrInput == "1":
        fileWrittenCorrect = False
        userFileNameInput = ""
        #validates input for file name 
        while not fileWrittenCorrect:
        	# file mode main screen
            boxGenerator(["L O A D    F I L E", "", "Enter a file name", "then press [enter]"])
            if userFileNameInput == "":
                userFileNameInput = input(" Filename: ")
            startTime = time.clock()

            #checks if the file name exists 
            if os.path.exists(userFileNameInput):
                boxGenerator(["L O A D    F I L E", "", "", "Correct File name", "", "Done"])
                checkWordsForFiles(open(userFileNameInput).read(), userFileNameInput)
                fileWrittenCorrect = True
                open(userFileNameInput).close()
                endTime = time.clock() - startTime
                #shows the time in microseconds
                boxGenerator(["C H E C K E D   F I L E", "", "TimeElapsed", str(endTime * 10 ** 6), "microseconds"])
            else:
                boxGenerator(["L O A D    F I L E", "", "Enter a file name or press q to quit", "then press [enter]"])
                userFileNameInput = input(" Filename: ")
                if (userFileNameInput == "q"):
                    break
	# sentence mode
    elif usrInput == "2":

    	# prints sentence screen
        boxGenerator(["S E N T E N C E   M O D E", "", "Enter a sentence", "then press [enter]"])
        checkWordsForSentences(input(" Enter sentence to spellcheck: "))
        usrInput = input(" Press q [enter] to quit or any other key [enter] to go again: ")
        # termenates the program
        if usrInput == "q":
            terminated = True
    
    # quits the program
    elif usrInput == "0" or usrInput == "q":
        terminated = True
        englishDict.close()
