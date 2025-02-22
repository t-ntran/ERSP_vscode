# A text input box can be represented as a string, like this:
#
# 'abc|def'
#
# The '|' character is the cursor, and the other characters are the text
# inside the box. Depending on the key that the user presses, you want
# to update the text box.
#
# Pressing 'right' moves the cursor to the right by one character, unless
# there is no character to the right of the cursor:
#
# 'abc|def', 'right' -> 'abcd|ef'
#
# Similarly, pressing 'left' moves the cursor to the left by one
# character, unless there is no character to the left of the cursor:
#
# '|def', 'left' -> '|def'
#
# Lastly, the user can type a single letter like 'z'. This inserts the
# character to the left of the cursor:
#
# 'abc|def', 'z' -> 'abcz|def'
#
# Write unit tests for the textbox function and fix the three bugs.
# Feel free to copy the test cases above, and write your own as well.

## textbox('abc|def', 'right') == 'abcd|ef'
## textbox('abcdef|', 'right') == 'abcdef|'
## textbox('|def', 'left') == '|def'
## textbox('abc|def', 'left') == 'ab|cdef'
## textbox('abc|def', 'z') == 'abcz|def'
def textbox(current, key):
    left, right = current.split('|')
    if key == 'right':
        # Move one char from right to left
        if right == '':
            return current
        return left + right[0] + '|' + right[1:]
    elif key == 'left':
        if left == '':
            return current
        return left[:-1] + '|' + left[-1] + right
    else:
        # Insert char before cursor
        return left + key + '|' + right