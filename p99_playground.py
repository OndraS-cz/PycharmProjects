from time import sleep

alphabet = "abcdefghijklmnopqrstuvwxyz "

sentence = "hello world"
solvedStr = []

for character in sentence:
    solved = False
    solvedStr.append(" ")
    for letter in alphabet:
        if not solved:
            solvedStr[len(solvedStr) - 1] = letter
        if letter == character:
            solved = True
        else:
            print("".join(solvedStr))
    sleep(0.5)
print("".join(solvedStr))