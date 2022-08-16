def Rev_Fib(num):
    if num == 0:
        return num
    elif num == 1:
        return 1/num
    else:
        return 1/(Rev_Fib(num-1) + Rev_Fib(num-2))

def Fib(num):
    if num == 0:
        return num
    elif num == 1:
        return num
    else:
        return (Fib(num-1) + Fib(num-2))

def main():
    with open ("rev_Fib.txt", 'w') as f:
        for num in range(20):
            f.write(str(Rev_Fib(num))+"\n")
    f.close()

    with open ("Fib.txt", 'w' )  as f:
        for num in range(20):
            f.write(str(Fib(num))+"\n")
    f.close()

main()
