#include <iostream>
#include <cstdlib>
#include <ctime>

int main() {
    srand(time(0));
    int target = rand() % 100 + 1;
    std::cout << "猜一个介于1到100之间的数字：";
    return 0;
}