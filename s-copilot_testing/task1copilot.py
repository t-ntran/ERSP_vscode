# Dot-decimal notation represents a list of integers as a string. The
# integers are written in base 10, separated by periods. This function
# parses dot-decimal notation back into a list of integers. For example:
#
# '22.4.5' -> [22, 4, 5]


from functools import reduce
def parse_dot_decimal(s):
    parts = s.split('.')
    nums = []
    for part in parts:
        nums.append(int(part))
    return nums

def str2int(s):
    def fn(x, y):
        return x * 10 + y
    def char2num(s):
        return {'0': 0, '1': 1, '2': 2, '3': 3, 
        '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
    return reduce(fn, map(char2num, s))
def dot_decimal_notation_to_list(s):
    return map(str2int, s.split('.'))

def dot_decimal_notation_to_list2(s):
    return list(map(str2int, s.split('.')))

##dot_decimal_notation_to_list2('22.4.5') == [22, 4, 5]

# An IPv4 address can be written as a dot-decimal string. For example:
#
# '127.0.0.1'
#
# The input is a dot-decimal string containing 0 or more integers. If
# the input contains exactly 4 integers, and each integer is between
# 0 and 255 inclusive, then the input is a valid IPv4 address, and you
# should return the list of integers. Otherwise, return None:
#
# '1.2.3.4' -> [1, 2, 3, 4]
# '22.4.5' -> None

# Write unit tests for the examples above before you write your code.
def parse_ipv4(s):
    return

## dot_decimal_notation_to_ipv4_2('1.2.3.4') == [1, 2, 3, 4]
## dot_decimal_notation_to_ipv4_2('22.4.5') == None
## dot_decimal_notation_to_ipv4_2('0.0.0.-1') == None
## dot_decimal_notation_to_ipv4_2('0.0.0.256') == None
## dot_decimal_notation_to_ipv4_2('0') == None
## dot_decimal_notation_to_ipv4_2('') == None
## dot_decimal_notation_to_ipv4_2('1.2.3.4.5') == None
def dot_decimal_notation_to_ipv4_2(s):
    if len(s.split('.')) == 4:
        try:
            num = lambda x: 0 <= x <= 255
            return num
        except:
            return None
    else:
        return None