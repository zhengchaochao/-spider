# @Time    : 2019/1/15 下午3:16
# @Author  : 郑超
# @Desc    : 在这个游戏里，玩家在一片到处是龙的陆地上，龙生活的山洞穴装满了它们收集来的大量宝藏
#            有些龙很友善，愿意与你分享宝藏。而另外一些龙很饥饿。会吃掉闯入它们洞穴的任何人。玩家站在两个洞口前
#            一个山洞住着友善的龙，另一个住着饥饿的龙。玩家必须选择一个
import random
import time


class Dragon:
    def display_intro(self):
        """游戏说明"""
        print("You are in a land full of dragons.\nIn front of you,you see two caves.\nIn one cave,the dragon is"
              "friendly and will share his treasure with you.\nThe other dragon is greedy and hungry,and will eat"
              "you on sight.\nWhich cave wil you go into?(1 or 2)")
        print("-" * 50)

    def choose_cave(self):
        """输入选择"""
        cave = ''
        while cave != "1" and cave != "2":
            print("Which cave while you go into?")
            cave = input("Please choose the cave\nTo:")
        return cave

    def check_cave(self, choose_cave):
        """游戏主体"""
        print("You approach the cave......")
        time.sleep(1)
        print("It is dark and spooky")
        time.sleep(1)
        print("A large dragon jumps out in front of you! He opens his jaws and ......")
        time.sleep(1)
        friendly_cave = random.randint(1, 2)
        if choose_cave == str(friendly_cave):
            print("Gives you his treasure!")
        else:
            print("Gobbles you down in one bite!")
        print("*" * 100)
        print()
        print("*" * 100)
        # 循环主体
        print("DO you want to play again?(yes or no)")
        play_again = input()
        if play_again == "YES" or play_again == "y":
            d = Dragon()
            d.display_intro()
            cave = d.choose_cave()
            d.check_cave(choose_cave=cave)
        else:
            print("Game over")


if __name__ == "__main__":
    d = Dragon()
    d.display_intro()
    cave = d.choose_cave()
    d.check_cave(choose_cave=cave)
