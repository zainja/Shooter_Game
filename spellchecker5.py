import datetime, time
import os
from difflib import SequenceMatcher

sizeX = 50  # predefined width for the box that will contain items


# function stringMargin
# takes an input of list of contents that need to be printed in a box
# creates an artificial spaces around the item
# if the list is less than 8 it will add empty string items
# to keep the box at a standard height

def stringMargin(listOfItemsForBox):
    # adds empty elements to the list
    while len(listOfItemsForBox) < 8:
        listOfItemsForBox.append("")
    size = sizeX - 1  # the general size the item should have
    modifiedList = []  # the final output of the function
    for item in listOfItemsForBox:
        needed_length = size - len(item)  # calculates needed length
        rightIndent = 10   # a standard right intended
        if item == listOfItemsForBox[0]:
            rightIndent = 5   # if the item was the first item the margin is 5

        leftIndent = needed_length - rightIndent
        leftMargin = len(item) + leftIndent  # adds the left indent to total length of item
        item = item.ljust(leftMargin)  # uses the leftmargin to add spaces to the left side of the item
        rightMargin = len(item) + rightIndent  # adds the right indent to total len of item
        item = item.rjust(rightMargin, " ")  # adds right indent spaces into the item
        modifiedList.append(item)
    return modifiedList


def boxGenerator(listOfContent):
    os.system('clear')
    listOfContent = stringMargin(listOfContent)
    print(u'\u250F', end="", flush=True)  # corner
    for i in range(0, sizeX - 1):
        print(u'\u2501', end="", flush=True)  # top-bar
    print(u'\u2513')  # corner

    for i in range(0, len(listOfContent)):
        # down
        print(u'\u2503', end="", flush=True)  # vertical pipe

        print(listOfContent[i], end="", flush=True)

        print(u'\u2503')  # vertical pipe

    print(u'\u2523', end="", flush=True)  # T style pipe

    for i in range(0, sizeX - 1):  # bottom
        print(u'\u2501', end="", flush=True)  # horizontal pipe

    print(u'\u251B')  # corner

    print(u'\u2517', end="", flush=True)
    for i in range(0, 20):
        print(u'\u2501', end="", flush=True)


terminated = False
englishDictReadOnly = open("EnglishWords.txt")
EnglishWords = englishDictReadOnly.read().split("\n")  # creates a list to contain the words in the file
englishDictReadOnly.close()
englishDict = open("EnglishWords.txt", "a")  # opens the file of the english words


def sentenceModification(sentence):
    sentence = sentence.lstrip().rstrip().lower()
    for chars in sentence:
        if (ord(chars) < ord("a") or ord(chars) > ord("z")) and ord(chars) != ord(" "):
            sentence = sentence.replace(chars, " ")
    return sentence


fileWordsInformation = {
    'total Number of words': 0,
    'correctly spelt words': 0,
    'incorrectly spelt words': 0,
    'ignored words': 0,
    'marked words': 0,
    'words added to dictionary': 0
}


def checkWordsForSentences(sentence):
    sentence = sentenceModification(sentence)
    listofWords = sentence.split()
    fileWordsInformation["total Number of words"] = len(listofWords)
    fileWordsInformation["correctly spelt words"] = 0
    fileWordsInformation["incorrectly spelt words"] = 0
    for word in listofWords:
        if word in EnglishWords:
            boxGenerator(["W O R D     F O U N D", "", "", word, "Spelt correctly"])
            dummyInput = input("enter any key to go next")
            fileWordsInformation["correctly spelt words"] += 1
        else:
            boxGenerator(["W O R D   N O T  F O U N D", "", "", word, "Not found in dictionary"])
            dummyInput = input("enter any key to go next")
            fileWordsInformation["incorrectly spelt words"] += 1
    finalBoxList = ["F I N A L   R E S U L T", ""]
    for x, y in fileWordsInformation.items():
        tempStr = "Number of " + x + " : " + str(y)
        finalBoxList.append(tempStr)
        if len(finalBoxList) == 4:
            break
    boxGenerator(finalBoxList)


def checkWordsForFiles(sentence, file):
    sentence = sentenceModification(sentence)
    listofWords = sentence.split()
    fileWordsInformation["total Number of words"] = len(listofWords)
    correctedWord = ""
    resultFile = open("2" + file, "w")
    for word in listofWords:
        if word in EnglishWords:
            correctedWord += word + " "
            fileWordsInformation["correctly spelt words"] += 1
        else:
            listOfRaitos = []
            wordsFromRatios = []
            for matchedWord in EnglishWords:
                ratio = SequenceMatcher(None, matchedWord, word).ratio()
                listOfRaitos.append(ratio)
                wordsFromRatios.append(matchedWord)
            desiredInput = False
            while not desiredInput:
                requiredWordIndex = listOfRaitos.index(max(listOfRaitos))
                desiredWord = wordsFromRatios[requiredWordIndex]
                boxGenerator(["W O R D   N O T   F O U N D", "", word, "", "did you mean", "", desiredWord])
                changeWordInput = input("y or n else will go to the next screen :")
                print("\n")
                if changeWordInput == "y":
                    correctedWord += desiredWord + " "
                    desiredInput = True
                elif changeWordInput == "n":
                    listOfRaitos.pop(requiredWordIndex)
                    wordsFromRatios.pop(requiredWordIndex)
                else:
                    desiredInput = True
                    correctInput = False
                    while not correctInput:
                        boxGenerator(["W O R D   N O T   F O U N D", "", word, "", "1. Ignore the word.",
                                      "2. Mark the word as incorrect.", "3. Add word to dictionary."])
                        fileWordsInformation["incorrectly spelt words"] += 1
                        incorrectWordsHandling = input("Enter choice: ")
                        print("\n")
                        if incorrectWordsHandling == "1":
                            correctedWord += "!" + word + "! "
                            fileWordsInformation["ignored words"] += 1
                            correctInput = True
                        elif incorrectWordsHandling == "2":
                            correctedWord += "?" + word + "? "
                            fileWordsInformation["marked words"] += 1
                            correctInput = True
                        elif incorrectWordsHandling == "3":
                            correctedWord += "*" + word + "* "
                            fileWordsInformation["words added to dictionary"] += 1
                            englishDict.write("\n" + word)
                            correctInput = True

    resultFile.write(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S\n"))
    finalBoxList = ["F I N A L   R E S U L T", ""]
    for x, y in fileWordsInformation.items():
        tempStr = "Number of " + x + " : " + str(y)
        temp2Str = tempStr + "\n"
        finalBoxList.append(tempStr)
        resultFile.write(temp2Str)
    boxGenerator(finalBoxList)
    dummyInput = input("enter any key to go next")
    resultFile.write(correctedWord)
    resultFile.close()


while not terminated:
    listOfWords = []  # creates a list to contain the words
    boxGenerator(["S P E L L   C H E C K E R", "", "1. Check a file", "2. Check a sentence", "", "", "0.Quit"])
    usrInput = input("Enter choice: ")
    if usrInput == "1":
        fileWrittenCorrect = False
        userFileNameInput = ""
        while not fileWrittenCorrect:
            boxGenerator(["L O A D    F I L E", "", "Enter a file name", "then press [enter]"])
            if userFileNameInput == "":
                userFileNameInput = input(" Filename: ")
            startTime = time.clock()
            if os.path.exists(userFileNameInput):
                boxGenerator(["L O A D    F I L E", "", "", "Correct File name", "", "Done"])
                checkWordsForFiles(open(userFileNameInput).read(), userFileNameInput)
                fileWrittenCorrect = True
                open(userFileNameInput).close()
                endTime = time.clock() - startTime
                boxGenerator(["C H E C K E D   F I L E", "", "TimeElapsed", str(endTime * 10 ** 6), "microseconds"])
            else:
                boxGenerator(["L O A D    F I L E", "", "Enter a file name or press q to quit", "then press [enter]"])
                userFileNameInput = input(" Filename: ")
                if (userFileNameInput == "q"):
                    break
    elif usrInput == "2":
        boxGenerator(["S E N T E N C E   M O D E", "", "Enter a sentence", "then press [enter]"])
        checkWordsForSentences(input("Enter sentence to spellcheck: "))
        usrInput = input("Press q [enter] to quit or any other key [enter] to go again: ")
        if usrInput == "q":
            terminated = True
    elif usrInput == "0" or usrInput == "q":
        terminated = True
        englishDict.close()
