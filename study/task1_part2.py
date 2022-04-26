# A valid IPv4 address is a dot-decimal string with exactly four
# integers, where each integer is between 0 and 255 inclusive.
#
# The input is a dot-decimal string containing 0 or more integers. If
# the input is a valid IPv4 address, return the corresponding list of
# integers. Otherwise, return None.
#
# '22.4.5' => None
# '1.2.3.4' => [1, 2, 3, 4]

# Write unit tests for the examples above before you write your code.
def parse_ipv4(s):
    return