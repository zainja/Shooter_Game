sizeX=50

def stringMargin(listofItems):
    size = sizeX-1
    modifiedList = []
    for item in listofItems:
        needed_length =size - len(item)
        rightIntedent = int(needed_length/4)
        leftIntedent = needed_length - rightIntedent
        leftMargin = len(item) + leftIntedent
        item = item.ljust(leftMargin)
        rightMargin= len(item) + rightIntedent
        item = item.rjust(rightMargin," ")
        modifiedList.append(item)
    return modifiedList


def boxGenerator(listofContent) :

    print(u'\u250F', end="", flush=True) #corner 
    for i in range (0,sizeX-1) :
        print(u'\u2501' , end="", flush=True) #top-bar
    print(u'\u2513')

    for i in range (0,len(listofContent)): 
    #down
        print(u'\u2503', end="", flush=True)
        
        print(listofContent[i] ,end="", flush=True)
        
        print(u'\u2503')

    print(u'\u2517', end="", flush=True) #corner 

    for i in range (0,sizeX-1) :#bottom
        print(u'\u2501' , end="", flush=True)
     
    print(u'\u251B') 


newList =["H E A D E R  H E A D E R","","apple","","potato"]
boxGenerator(stringMargin(newList))
