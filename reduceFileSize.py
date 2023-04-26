import random
import json

inputFile = "shortList.txt"
outputFile = "shortListNew.txt"
lines = []
i = 0

items = 0

fileOut = open(outputFile, 'a')

with open(inputFile, mode='r') as fileIn:
    #   Process 44131073 lines one by one
    for line in fileIn:

        line = line[line.find('{'):]

        #   Verify if no isbn is present, skip entry
        if 'isbn_10' not in line and 'isbn_13' not in line:
            continue
        else:
            lines.append(line)
            i += 1
            #   Once certain number of lines appended, shuffle section
            if i > 74999:
                random.shuffle(lines)
                #   Number of lines to add from each randomized group
                num_lines = 15000
                fileOut.writelines(lines[:num_lines])
                #   Clear lines list to free memory, reset counter variable
                items += num_lines
                lines.clear()
                i = 0
                print(f"Roughly {items} Copied")
                continue

    #   Final group of the file
    random.shuffle(lines)
    #   Number of lines to add from group
    num_lines = 15000
    fileOut.writelines(lines[:num_lines])
    items += num_lines
    print(f"Roughly {items} Copied")

fileOut.close()
print("Finished!")
