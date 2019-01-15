# @Time    : 2019/1/15 下午2:32
# @Author  : 郑超
# @Desc    : 猜数字游戏
import random

guessesTaken = 0
print("Hello! what is you name?")
name = input()
number = random.randint(1, 20)
print("Well, %s,I am thinking of a number between 1 and 20." % name)
print("Take a guess")
while True:
    try:
        guess_number = int(input())
        guessesTaken += 1
        if guess_number < number:
            print("You guess is to low")
        elif guess_number > number:
            print("You guess is to high")
        else:
            print("Good job,%s! You guessed my number %d guesses!" % (name, guessesTaken))
            break
    except:
        guessesTaken += 1
        print("What you enter is not a number！！！")
