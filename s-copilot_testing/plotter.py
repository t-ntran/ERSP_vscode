with open(r"C:\Users\sdtnt\ERSP_vscode-5"
    r"\s-copilot_testing\rev_Fib.txt") as f:
    invs = f.readlines()
f.close()

with open(r"C:\Users\sdtnt\ERSP_vscode-5"
    r"\s-copilot_testing\Fib.txt") as f:
    fib = f.readlines()
f.close()

first_digit_invs = []
for x in invs:
    num = str(x).strip()
    #Get first nonzero digit of num
    for i in range(len(num)):
        if(num[i]) != '0' and num[i] != '.':
            first_digit_invs.append(int(num[i]))
            break

first_digit_fib = []
for x in fib:
    num = str(x).strip()
    #Get first nonzero digit of num
    for i in range(len(num)):
        if(num[i]) != '0' and num[i] != '.':
            first_digit_fib.append(int(num[i]))
            break
print(first_digit_invs)

import matplotlib.pyplot as plt
plt.hist(first_digit_fib, bins=10, alpha=0.5,label='fib')
plt.hist(first_digit_invs, bins=10, alpha=0.5,label='fib')
plt.hist(first_digit_fib, bins=10,range=(0,10))
#plt.hist(first_digit_invs, bins=10,range=(0,10))
plt.show()

 