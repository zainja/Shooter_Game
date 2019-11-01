terminated=False
file = open("EnglishWords.txt") # opens the file of the english words
EnglishWords = file.read().split("\n") #creates a list to contain the words in the file


#this function handles
#having special characters like . , ? ! :
#and if there is repeated characters these will be dealt with ex: hello,,,,,, world!!!  : result [0] hello [1] world
def sentenceModification (sentence) :
    sentence=sentence.lstrip().rstrip().lower()
    for chars in sentence :
        if (ord(chars) < 97 or ord(chars) >122) and (not 48<= ord(chars) <= 57) and ord(chars) != 32 :
            sentence = sentence.replace(chars," ")
        print(sentence)

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


while not terminated :
    sentence = input("Enter sentence to spellcheck: ")#takes user input
    listofWords=[] # creates a list to contain the words
    listofWords=sentenceModification(sentence).split()
    checkWords(listofWords)
    userinput=input("Press q [enter] to quit or any other key [enter] to go again: ")

    if(userinput == "q") :
        file.close()
        terminated = True
