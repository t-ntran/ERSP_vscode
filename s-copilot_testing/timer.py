
def Fib(num):
    if num == 0:
        return num
    elif num == 1:
        return num
    else:
        return Fib(num-1) + Fib(num-2)

s = "hello world!"
#create timer
import time
start = time.time() #time.perf_counter()
Fib_seq = []
for n in range(6):
    Fib_seq.append(Fib(n))
end = time.time() #time.perf_counter()
Time = end -start
print("Time:", end - start)

class Timer:
    def timer():
        start = time.time()
        counter = 0
        for char in s:
            counter += 1
        end = time.time()
        Time = end -start
        print("Time:", end - start)
        return Time

t = Timer()
ti = t.timer

import sys
print(sys.path)
