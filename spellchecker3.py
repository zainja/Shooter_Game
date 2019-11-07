import datetime
import time
import os
terminated=False
englishDict = open("EnglishWords.txt") # opens the file of the english words
EnglishWords = file.read().split("\n") #creates a list to contain the words in the file
print("S P E L L  C H E C K E R")

#this function handles
#having special characters like . , ? ! :
#and if there is repeated characters these will be dealt with ex: hello,,,,,, world!!!  : result [0] hello [1] world
def sentenceModification (sentence) :
    sentence=sentence.lstrip().rstrip().lower()
    for chars in sentence :
        if (ord(chars) < 97 or ord(chars) >122)  and ord(chars) != 32 :
            sentence = sentence.replace(chars,"")
    return sentence
#function that checks the words in the listofWords with the dictionary and returns if the word is in the dictionary list or not
def checkWords(listofWords) :
    correctWordsCount=0
    incorrectWordsCount=0
    for word in listofWords :
        if word in EnglishWords :
            print("%s spelt correctly" %word)
            correctWordsCount+=1
        else :
            print("%s not found in dictionary" %word)
            incorrectWordsCount+=1
    print("Number of words: %d" %len(listofWords))
    print("Number of correctly spelt words: %d" %correctWordsCount)
    print("Number of incorrectly spelt words: %d" %incorrectWordsCount)

def checkWordsForFiles(listofWords,file) :
    checkedFile = open("2" + file, "w")
    correctedWord=""
    correctWordsCount=0
    incorrectWordsCount=0
    for word in listofWords :
        if word in EnglishWords :
            correctedWord += word +" "
            correctWordsCount +=1
        else :
            correctedWord+= "?"+word+"? "
            incorrectWordsCount +=1

    checkedFile.write(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S\n"))

    print("Number of words: %d" , %len(listofWords))
    checkedFile.write("Number of words: %d \n" %len(listofWords))
    print("Number of correctly spelt words: %d" %correctWordsCount)
    checkedFile.write("Number of correctly spelt words: %d \n" %correctWordsCount)
    print("Number of incorrectly spelt words: %d" %incorrectWordsCount)
    checkedFile.write("Number of incorrectly spelt words: %d \n\n" %incorrectWordsCount)

    checkedFile.write(correctedWord)
    checkedFile.close()

while not terminated :
    listofWords=[] # creates a list to contain the words
    print("1. Check a file \n2. Check a sentence\n\n0.Quit\n")
    usrInput= input("Enter choice: ")

    if usrInput == "1" :
        fileWrittenCorrect = False
        userFileNameInput = input("Enter the name of the file to spellcheck: ")
        startTime = time.clock()
        while not fileWrittenCorrect :
            if os.path.exists(userFileNameInput) :
                print("Correct File name")
                listofWords=sentenceModification(open(userFileNameInput).read()).split()
                checkWordsForFiles(listofWords,userFileNameInput)
                fileWrittenCorrect = True
                print("Done")
                open(userFileNameInput).close()
                endTime = time.clock() - startTime
                print("TimeElapsed " , endTime * 10**6 ,"microseconds")
                usrInput=input("Press q [enter] to quit or any other key [enter] to go again: ")
                if usrInput == "q" :
                    terminated = True
            else :
                print("\nplease try again enter a file name \n")
                userExitFileMode=input("Exit press q to rewrite the file name press any thing else ")
                if userExitFileMode == "q" :
                    break;
                else :
                    userFileNameInput = input("Enter the name of the file to spellcheck: ")

    elif usrInput == "2" :
        sentence = input("Enter sentence to spellcheck: ")#takes user input
        checkWords(sentenceModification(sentence).split())
        usrInput=input("Press q [enter] to quit or any other key [enter] to go again: ")
        if usrInput == "q" :
            terminated = True
    elif(usrInput == "0" or usrInput == "q") :
        terminated = True
        englishDict.close()


    else :
        print("\nplease try again\n")
