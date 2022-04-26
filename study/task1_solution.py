# Dot-decimal notation represents a list of integers as a string. The
# integers are written in base 10 (decimal), separated by periods.
#
# Given a dot-decimal string containing 0 or more integers, return the
# corresponding list of integers.
#
# Example: '22.4.5' => [22, 4, 5]

## parse_dot_decimal('22.4.5') == [22, 4, 5]
## parse_dot_decimal('-27') == [-27]
## parse_dot_decimal('') == []
def parse_dot_decimal(s):
    if len(s) == 0:
        return []
    split = s.split('.')
    nums = []
    for word in split:
        nums.append(int(word))
    return nums


# A valid IPv4 address is a dot-decimal string with exactly four
# integers, where each integer is between 0 and 255 inclusive.
#
# The input is a dot-decimal string containing 0 or more integers. If
# the input is a valid IPv4 address, return the corresponding list of
# integers. Otherwise, return None.
#
# Example 1: '22.4.5' => None
# Example 2: '1.2.3.4' => [1, 2, 3, 4]

## parse_ipv4('22.4.5') == None
### parse_ipv4('192.168.0.1') == [192, 168, 0, 1]
## parse_ipv4('2.3.-27.2') == None
## parse_ipv4('') == None
def parse_ipv4(s):
    nums = parse_dot_decimal(s)
    if len(nums) != 4:
        return None
    for num in nums:
        if num < 0 or num > 255:
            return None
    return nums