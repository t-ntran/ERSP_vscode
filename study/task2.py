# A text input box can be represented as a string, like this:
#
# 'abc|def'
#
# The '|' character represents the cursor, and the other characters
# are the text inside the box. Depending on the key that the user
# presses, you want to update the text box. For example, if the user
# presses 'backspace', you want to delete the character to the left of
# the cursor:
#
# 'abc|def', 'backspace' => 'ab|def'
# 
# If there is no character to the left of the cursor, 'backspace' does
# nothing.
#
# The user can also press the 'left' and 'right' arrow keys. Pressing
# 'left' moves the cursor to the left by one character, unless there is
# no character to the left of the cursor:
#
# 'abc|def', 'left' => 'ab|cdef'
#
# Pressing 'right' moves the cursor to the right by one character,
# unless there is no character to the right of the cursor:
#
# 'abc|', 'right' => 'abc|'
#
# Lastly, the user can type a single letter like 'z'. This inserts the
# character to the left of the cursor:
#
# 'abc|def', 'z' => 'abcz|def'
# 
# Write unit tests for the textbox function and fix the four bugs.

def textbox(current, key):
    left, right = current.split('|')
    if key == 'bockspace':
        # Remove last char from left
        return left[:-1] + '|' + right
    elif key == 'left':
        # Move last char from left to right
        return left[:-1] + '|' + left[-1] + right
    else:
        # Insert char before cursor
        return left + key + right