# This  script changes all names of the characters in the play 
# that are in the beginning of each new line by suggesting the user 
# to manually replace all names to the needed ones

# Copy-past scenario into to_change.txt
# Output is changed.txt

#ATTENTION: 
# 1) This script won't work if the symbol after a character name on a new line isn't a colon (':'). 
# 2) Only works for character names in the beginning of the sentence
#3) In order for it to work with other symbols right after character names, change all occurences of ':' up to your choice in the script

f = open("to_change.txt", "r")
out = open('changed.txt', 'w')

# distinct names

names = {}
name = ''
replaced = []

for line in f:
    name = ''

    for letter in line:
        if letter != ':':
            name += str(letter)
        if letter == ':':
            if name not in names: 
                names[name] = ''
            name = ''
            break
            
# INTERFACE

print(names)

for name in names:


    print('What should the program replace "' + name +  '" with? Type: ' )
    x = str(input())
    names[name] = x

sentence = ''
f.seek(0)

for line in f:
    name = ''

    for letter in line:

        if letter != ':':
            name += str(letter)
        if letter == ':':
            line = line.replace(name, names[name])
            needed = str(name)

            name = ''
            break
    
    name = ''
    
    out.write(line)



out.close()
f.close()

