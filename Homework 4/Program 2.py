def count_frequency(mylist):

    # break the string into list of words
    mylist = mylist.split()
    #creating an empty dictionary
    str2 = {}

    #loop till string values present in mylist
    for i in mylist:
        #count the frequency of the each word
         str2[i] = str2.get(i, 0) + 1
    return str2
                 
mylist = input("Enter list of words to count it's frequency: \n")
print(count_frequency(mylist))