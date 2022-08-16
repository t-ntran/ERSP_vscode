#from the ‘data.csv’ file. Delete the first column and the last
#column. Save it to the ‘output.csv’ file.

def main():
    with open(r'C:\Users\sdtnt\ERSP_vscode-5'
    r'\s-copilot_testing\data.csv') as f:
        data = f.readlines()
    data = [line.strip().split(',') for line in data]
    with open('output.csv', 'w') as f:
        for line in data:
            f.write(','.join(line[1:-1]) + '\n')
main()