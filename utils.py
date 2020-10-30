import random


def next_image():
    global Cont
    Cont = 1


def simulation():
    a = random.randrange(100)
    if a == 2:
        return True
    return False

