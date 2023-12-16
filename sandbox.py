def a(x):
    if x != 0:
        b(x - 1)
    print(x)


def b(x):
    if x != 0:
        a(x - 1)
    print(x)


a(10)
