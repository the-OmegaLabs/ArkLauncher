import random
sum = int(input("sum"))
randlist = ["o", "i", "a", "yi", "u", "d"]
for i in range(0, sum):
    print(randlist[random.randint(0, 5)], end=" ")
