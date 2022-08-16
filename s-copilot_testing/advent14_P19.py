s = "hello world"
print("hi")
def main():
    input_path1 = "C:/Users/sdtnt/ERSP_vscode-5"
    input_path2 = "/s-copilot_testing/input-day14.txt"
    input_path = input_path1 + input_path2

    #Create an empty dictionary
    template = ""
    insertionRules = {}

    #Read input file
    with open(input_path, "r") as f:
        input_data = f.read()

        input = input_data.split("\n")

        #Argument one
        template = input[0]

        #Iterate from 2 to the end of list
        for i in range(2, len(input)):
            rawRule = input[i].split("->")
            #Copilot answer better than ori idea

            #Add to dictionary
            insertionRules[rawRule[0].strip()] = rawRule[1].strip()

    print("Template: " + template)
    print("Rules: " + str(insertionRules))

    #string to array
    polymer = list(template)

    newPolymer = []
    #Iterate over the polymer
    for i in range(0, len(polymer)-1):
        insertionRule = insertionRules[polymer[i] + polymer[i+1]]
        if insertionRule is not None:
            newPolymer.append(polymer[i])
            newPolymer.append(insertionRule)
            #newPolymer.append(polymer[i+1])

    newPolymer.append(polymer[len(polymer) - 1])

    print(newPolymer)

    #Count the occurances of each letter in newPolymer
    letterCounts = {}
    for i in range(0, len(newPolymer)):
        if newPolymer[i] in letterCounts:
            letterCounts[newPolymer[i]] += 1
        else:
            letterCounts[newPolymer[i]] = 1

    #Get the highest value of the dictionary
    highestValue = 0
    lowestValue = len(newPolymer)

    for key in letterCounts:
        if letterCounts[key] > highestValue:
            highestValue = letterCounts[key]
        
        if letterCounts[key] < lowestValue:
            lowestValue = letterCounts[key]

    result = highestValue - lowestValue
    print("Results: " + str(result))


main()
s = "goodbye"

"""
For counting occurances and highest and lowest values
particpants just accepted Copilot's suggestion
as it seemed right
later went to double check by printing and
evaluating each line
"""