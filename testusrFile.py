from difflib import SequenceMatcher
# if(usrchoice == 1) :
# userFileName = input("Enter the name of the file to spellcheck: ")
# usrFile= open(userFileName)
# sentence=usrFile.read().split()
# badChars=[",",".","?"," "]
# for index in range(0,len(sentence)) :
#     for unwantedItem in badChars :
#         if unwantedItem in sentence[index]:
#             sentence[index] = sentence[index].replace(unwantedItem,"")
# print(sentence)
# sentence= "HKELO JFF MT JFFSD"
# sentence.lower()
# print(sentence)
englishDictReadOnly = open("EnglishWords.txt")
EnglishWords = englishDictReadOnly.read().split("\n")
list = ["banana","apple","mango", "manra"]
newList =[]
sentence = "banan apple manga"
sentence = sentence.split()
print(sentence)
for word in sentence :
    sutableWord = False
    for dict in EnglishWords:
        if sutableWord == EnglishWords :
            newList.append(sutableWord)
        else :
            
