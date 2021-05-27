from cs50 import get_float


while True:
    n = get_float("Change owed: ")
    if n >= 0:
        break

owed = round(n * 100)
coins = 0

while owed >= 25:
    coins += 1
    owed -= 25
while owed >= 10:
    coins += 1
    owed -= 10
while owed >= 5:
    coins += 1
    owed -= 5
while owed >= 1:
    coins += 1
    owed -= 1
print(coins)




