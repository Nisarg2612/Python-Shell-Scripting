#Take a string input from user 
s = input("Please enter string which you would like to shuffle?\n")
#Take integers from the user 
indices = input("please enter array indices\n")
#Break string into list of characters
input_str = list(s)
#Break integer array into list of characters
input_indices = list(indices)

strings = []

for s_val, idx in zip(input_str, input_indices):
    strings.append((input_str, idx))

strings = sorted(strings, key=lambda x : x[1])
#assign the position to list of characters
answers = [sval[0] for sval in strings]

print("".join(answers))
