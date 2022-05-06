# Welcome to the interactive tutorial for PBUnit! Please read the
# descriptions and follow the instructions for each example.
#
# Let's start with writing unit tests and using Projection Boxes:
#
# 1. Edit the unit test below to use your name and initials.
# 2. Click your mouse on each line of code in the function to see how
#    the Projection Boxes focus on the current line.
# 3. Check the Projection Box on the return statement to see if the
#    test passes.


## initials('Ada Lovelace') == 'AL'
def initials(name):
    parts = name.split(' ')
    letters = ''
    for part in parts:
        letters += part[0]
    return letters






# When you have multiple unit tests, you can select one test by adding
# an extra # at the start of the line (turning ## into ###). This will
# hide the other tests so you can examine or debug the selected test.
#
# 1. Find the line for the first test, and add a # at the start of the
#    line to select it.
# 2. Remove a # from the first test, and add a # to the second test. (If
#    you forget to remove the extra # from the first test, both tests
#    will be selected, so they will both appear.)
# 3. Select only the third test.
# 4. Deselect all tests.
# 5. Find the two Projection Boxes with the test results in them. The
#    result of each test is shown on the corresponding return statement.

## factorial(0) == 1
## factorial(2) == 2
## factorial(4) == 24
def factorial(n):
    if n <= 0:
        return 1
    result = 1
    for factor in range(2, n + 1):
        result *= factor
    return result








# If an exception occurs on a certain line, the exception will appear in
# that line's Projection Box.
#
# We can't show the test results on the return statement, because no
# return statement is reached. Instead, the test results are shown on
# the function header. (This is the line that starts with "def".)
#
# 1. Check the Projection Box on the function header to identify which
#    test has an exception.
# 2. Find the line where that unit test is written, and select that test
#    by adding a #.
# 3. Use the Projection Boxes to determine why the exception occurs.
# 4. Fix the code so that the unit test passes. If you're not sure what
#    the function should return, refer to the expected value which is
#    written in the unit test.
# 5. Deselect that unit test to make sure the other test still passes.

## average([3, 4, 5]) == 4
## average([]) == None
def average(nums):
    total = 0
    for num in nums:
        total += num
    avg = total // len(nums)
    return avg








# Projection Boxes also appear when you call a function from another
# function. In this example, the shout_last function calls the shout
# function, so we get Projection Boxes in the shout function too.
#
# 1. Click every line and see if you can figure out where each executed
#    line comes from. If you're not sure, try selecting each test case.


## shout('oops') == 'OOPS!'
def shout(s):
    uppercase = s.upper()
    return uppercase + '!'


## shout_last('oh hi') == 'oh HI!'
def shout_last(words):
    split = words.split(' ')
    split[-1] = shout(split[-1])
    return ' '.join(split)







# By default, Projection Boxes are not shown on if/elif/else lines. To
# show Projection Boxes on these lines as well, add a # at the end of
# the line, after the colon.
#
# 1. Add a # at the end of the if statement, after the colon. This will
#    show every execution of the if statement.
# 2. Why is the body of the if statement never executed? The Projection
#    Box you just added might be helpful.
# 3. How many loop iterations are there?

## only_positive([-1, -5, -3]) == []
def only_positive(nums):
    positive = []
    for num in nums:
        if num > 0:#
            positive.append(num)
    return positive





# Congratulations! Now you are ready to use PBUnit.