s = "hello world"

def create_dict_from_split_string(string):
    key = string.split("->")[0].strip()
    value = string.split("->")[1].strip()
    return {key:value}
    #forgot how to strip using Python
    #Copilot helped
    #Then printed out to ensure
    #Copilot was correct
    #With PB can choose to print
    #Or use PB to check
    

def convert_string_to_list(string):
    return list(string)
    #written by CP
    #Checked by printing

def main():
    input_path1 = "C:/Users/sdtnt/ERSP_vscode-5"
    input_path2 = "/s-copilot_testing/input-day14.txt"
    input = input_path1 + input_path2
    with open(input) as file:
        data = file.read().splitlines()
    print(data)
    reaction_list = []
    compound = convert_string_to_list(data[0])
    print(compound)
    for line in data:
        if "->" in line:
            reaction_list.append(
                create_dict_from_split_string(line)
            )
    print(reaction_list)
    #all print statements can be replaced
    #by PB

main()
s = "goodbye world"

#Note: particapant already had a very clear method of how they wanted
#To write their code. They were just using Copilot to test its 
#capabilites and handle tedious tasks
#It seems like it saved them a few Google searches though