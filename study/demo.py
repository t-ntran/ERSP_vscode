
def initials(name):
    parts = name.split()
    letters = ""
    for part in parts:
        letters += part[0]
    return letters