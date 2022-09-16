# Dot-decimal notation represents a list of integers as a string. The
# integers are written in base 10, separated by periods. This function
# parses dot-decimal notation back into a list of integers. For example:
#
# '22.4.5' -> [22, 4, 5]

##parse_dot_decimal('22.4.5') == [22, 4, 5]

def parse_dot_decimal(s):
    if s == '':
        return []
    parts = s.split('.')
    nums = []
    for part in parts:
        nums.append(int(part))
    return nums
