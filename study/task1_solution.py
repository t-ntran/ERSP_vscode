# Dot-decimal notation represents a list of integers as a string. The
# integers are written in base 10, separated by periods. This function
# parses dot-decimal notation back into a list of integers. For example:
#
# '22.4.5' -> [22, 4, 5]



def parse_dot_decimal(s):
    if s == '':
        return []
    parts = s.split('.')
    nums = []
    for part in parts:
        nums.append(int(part))
    return nums



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
## parse_ipv4('1.2.3.4') == [1, 2, 3, 4]
## parse_ipv4('22.4.5') == None
## parse_ipv4('0.0.0.-1') == None
## parse_ipv4('0.0.0.256') == None
## parse_ipv4('0') == None
## parse_ipv4('') == None
## parse_ipv4('1.2.3.4.5') == None
def parse_ipv4(s):
    nums = parse_dot_decimal(s)
    if len(nums) != 4:
        return None
    for num in nums:
        if num < 0 or num > 255:
            return None
    return nums