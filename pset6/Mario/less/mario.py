from cs50 import get_int


def main():
    size = get_size()
    for i in range(size):
        print(" " * (size - 1 - i), end = '')
        print("#" * (i + 1))


def get_size():
    while True:
        size = get_int("Height: ")
        if size > 0 and size < 9:
            break
    return size

main()

