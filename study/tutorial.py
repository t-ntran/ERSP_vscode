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
    parts = name.split()
    letters = ""
    for part in parts:
        letters += part[0]
    return letters






# When you have multiple unit tests, you can select one test by adding
# an extra # at the start of the line (turning ## into ###). This will
# hide the other tests so you can examine or debug the selected test.
#
# 1. Find the line for the first test, and add a # at the start of the
#    line to select it.
# 2. Remove a # from the first test, and add a # to the second test. If
#    you forget to remove the extra # from the first test, both tests
#    will be selected, so they will both appear.
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
# that line's Projection Box. Since no return statement is reached, the
# test results are shown on the first line of the function instead.
#
# 1. Check the Projection Box on the first line to identify which unit
#    test has an exception.
# 2. Find the line where that unit test is written, and select that test
#    by adding a #.
# 3. Fix the code so that the unit test passes. If you're not sure what
#    the function should return in that case, the expected value is
#    written in the unit test.
# 4. Deselect that unit test to make sure the other test still passes.




## average([3, 4, 5]) == 4
## average([]) == None
def average(nums):
    total = 0
    for num in nums:
        total += num
    avg = total // len(nums)
    return avg








# By default, Projection Boxes are only shown on executed statements.
# To show Projection Boxes on if/elif/else lines, add a # at the end of
# the line.
#
# 1. Add a # at the end of the if statement, after the colon. This will
#    show every loop iteration, even though no statements are executed
#    inside the loop.
# 2. How many loop iterations are there?

## only_positive([-1, -5, 0]) == []
def only_positive(nums):
    positive = []
    for num in nums:
        if num > 0:
            positive.append(num)
    return positive





# Congratulations! Now you know how to use PBUnit.