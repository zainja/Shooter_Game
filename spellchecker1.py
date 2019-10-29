sentence =input("Enter sentence to spellcheck: ") #takes user input
listofWords=[] # creates a list to contain the words
file = open("EnglishWords.txt") # opens the file of the english words
EnglishWords = file.read().split("\n") #creates a list to contain the words in the file
#get rid of the white spaces in the at the edges of the sentence
sentence = sentence.lstrip()
sentence = sentence.rstrip()

#split the sentence into a list with words in the sentence
listofWords=sentence.split();

#checks the words in the listofWords with the dictionary and returns if the word is in the dictionary list or not
for word in listofWords :
    if word in EnglishWords :
        print("%s spelt correctly" %word)
    else :
        print("%s not found in dictionary" %word)


print(listofWords)
