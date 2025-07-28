// 猜数字游戏
#include <iostream>
#include <cstdlib>
#include <ctime>

int main() {
    srand(time(0));
    int secretNumber = rand() % 100 + 1;
    int guess;
    std::cout << "猜一个1到100之间的数字：" << std::endl;
    std::cin >> guess;

    while (guess != secretNumber) {
        if (guess < secretNumber) {
            std::cout << "太小了，请再试一次！" << std::endl;
        } else if (guess > secretNumber) {
            std::cout << "太大了，请再试一次！" << std::endl;
        }
        std::cin >> guess;
    }

    std::cout << "恭喜你，猜对了！" << std::endl;
    return 0;
}