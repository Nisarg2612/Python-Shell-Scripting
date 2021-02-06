#Take the user name from the user
name = input("Hi, What is your Name? ")
#Shows the greetings with the user name to user
print("Hello", name + "! Let's play a game! \nThink of random number from 1 to 100, and I'll try to guess it!")
guessesTaken = 0
low_guess = 1
high_guess = 100
guessed_num = False

while guessed_num == False:
    #Computer guess the number based on the value assign to low_guess and high_guess variables
    guess = (low_guess + high_guess) // 2

    answer = input("Is it " + str(guess) + "? (yes/no)")
    #Count the guesses taken to find a final number 
    guessesTaken += 1

    if answer == "no":
        answer = input("Is the number larger than " +  str(guess) + "? (yes/no)")
        if answer == "yes":
            low_guess = guess + 1
        if answer == "no":
            high_guess = guess - 1
    else:
        guessed_num = True

print("Yeey! I got it in", guessesTaken, "tries!")
play_again = input("Do you want to play more? ")
