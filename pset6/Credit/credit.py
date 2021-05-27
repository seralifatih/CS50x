import cs50
import re
import sys

cardnumber = cs50.get_int("Number: ")
strnumber = str(cardnumber)

if len(strnumber) != 13 or len(cardnumber) != 15 or len(cardnumber) != 16:
    print("INVALID")
    sys.exit()



if len(strnumber) == 16:
    total = 0
    for i in range(0, 15, 2):
        total = total + int(strnumber[-2+i])
    print(total) 




