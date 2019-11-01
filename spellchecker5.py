import datetime
import time
import os
from difflib import SequenceMatcher

terminated = False
englishDictReadOnly = open("EnglishWords.txt")
EnglishWords = englishDictReadOnly.read().split("\n")  # creates a list to contain the words in the file
englishDictReadOnly.close()
englishDict = open("EnglishWords.txt", "a")  # opens the file of the english words
print("S P E L L  C H E C K E R")


# checks if the sentence contains any non alpha characters and removes them
# returns a sentence without non-alpha characters
# could be done using isAlpha function
def sentenceModification(sentence):
    sentence = sentence.lstrip().rstrip().lower()
    for chars in sentence:
        if (ord(chars) < 97 or ord(chars) > 122) and ord(chars) != 32:
            sentence = sentence.replace(chars, "")

    return sentence


def checkWords(listofWords):
    correctWordsCount = 0
    incorrectWordsCount = 0
    for word in listofWords:
        if word in EnglishWords:
            print("%s spelt correctly" % word)
            correctWordsCount += 1
        else:
            print("%s not found in dictionary" % word)
            incorrectWordsCount += 1
    print("Number of words: %d" % len(listofWords))
    print("Number of correctly spelt words: %d" % correctWordsCount)
    print("Number of incorrectly spelt words: %d" % incorrectWordsCount)


def checkWordsForFiles(listofWords, file):
    correctedWord = ""
    checkedFile = open("2" + file, "w")
    correctWordsCount = 0
    incorrectWordsCount = 0
    ignoredWordsCount = 0
    markedWordsCount = 0
    addedToDictionaryCount = 0

    for word in listofWords:
        if word in EnglishWords:
            correctedWord += word + " "
            correctWordsCount += 1
        else:
            print("\n%s not found in dictionary \n" % word)
            print("1. Ignore the word \n2. Mark the word as incorrect." +
                  "\n3. Add word to dictionary.\n")
            incorrectWordsCount += 1
            incorrectWordsHandling = input("Enter choice: ")
            correctInput = False
            while not correctInput:
                if incorrectWordsHandling == "1":
                    correctedWord += "!" + word + "! "
                    ignoredWordsCount += 1
                    correctInput = True
                elif incorrectWordsHandling == "2":
                    correctedWord += "?" + word + "? "
                    markedWordsCount += 1
                    correctInput = True
                elif incorrectWordsHandling == "3":
                    correctedWord += "*" + word + "* "
                    addedToDictionaryCount += 1
                    englishDict.write("\n" + word)
                    correctInput = True

                else:
                    print("please try again")
                    print("1. Ignore the word \n2. Mark the word as incorrect." +
                          "\n3.Add word to dictionary.\n")
                    incorrectWordsHandling = input("Enter choice")

    checkedFile.write(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S\n"))

    print("Number of words: %d" % len(listofWords))
    checkedFile.write("Number of words: %d \n" % len(listofWords))
    print("Number of correctly spelt words: %d" % correctWordsCount)
    checkedFile.write("Number of correctly spelt words: %d \n" % correctWordsCount)
    print("Number of incorrectly spelt words: %d" % incorrectWordsCount)
    checkedFile.write("Number of incorrectly spelt words: %d \n" % incorrectWordsCount)
    print("    Number of ignored words: %d" % ignoredWordsCount)
    checkedFile.write("    Number of ignored: %d \n" % ignoredWordsCount)
    print("    Number of added to dictionary: %d" % addedToDictionaryCount)
    checkedFile.write("    Number of added to dictionary: %d \n" % addedToDictionaryCount)
    print("    Number of marked: %d" % markedWordsCount)
    checkedFile.write("    Number of marked: %d \n\n" % markedWordsCount)
    checkedFile.write(correctedWord)
    checkedFile.close()


while not terminated:
    listOfWords = []  # creates a list to contain the words
    print("\n1. Check a file \n2. Check a sentence\n\n0.Quit\n")
    usrInput = input("Enter choice: ")
    if usrInput == "1":
        fileWrittenCorrect = False
        userFileNameInput = input("\nEnter the name of the file to spellcheck: ")
        startTime = time.clock()
        while not fileWrittenCorrect:
            if os.path.exists(userFileNameInput):
                print("Correct File name\n")
                listofWords = sentenceModification(open(userFileNameInput).read()).split()
                checkWordsForFiles(listofWords, userFileNameInput)
                fileWrittenCorrect = True
                print("Done")
                open(userFileNameInput).close()
                endTime = time.clock() - startTime
                print("TimeElapsed ", endTime * 10 ** 6, "microseconds")
                usrInput = input("Press q [enter] to quit or any other key [enter] to go again: ")
                if usrInput == "q":
                    terminated = True
            else:
                print("\nplease try again enter a file name ")
                userExitFileMode = input("\nExit press q , rewrite the file name press any thing else ")
                if userExitFileMode == "q":
                    break
                else:
                    userFileNameInput = input("\nEnter the name of the file to spellcheck: ")
    elif usrInput == "2":
        sentence = input("\nEnter sentence to spellcheck: ")  # takes user input
        checkWords(sentenceModification(sentence).split())
        usrInput = input("\nPress q [enter] to quit or any other key [enter] to go again: ")
        if usrInput == "q":
            terminated = True
    elif usrInput == "0" or usrInput == "q":
        terminated = True
        englishDict.close()

    else:
        print("\nplease try again\n")
