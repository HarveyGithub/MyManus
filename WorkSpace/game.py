# 导入必要的库
import random

def main():
    # 生成随机数作为目标数字
    target_number = random.randint(1, 100)

    print("欢迎来到猜数字游戏！")
    attempts = 0
    while True:
        try:
            guess = int(input("请输入你的猜测（1-100）："))
            attempts += 1

            if guess < target_number:
                print("太低了，请再试一次！")
            elif guess > target_number:
                print("太高了，请再试一次！")
            else:
                print(f"恭喜你，猜对了！你总共尝试了 {attempts} 次。")
                break
        except ValueError:
            print("请输入一个有效的整数。")

    # 游戏结束时的提示
    input("按回车键退出游戏...")

if __name__ == "__main__":
    main()