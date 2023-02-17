# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-01-12 15:31:11
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-02-16 16:03:46


def isPalindrome(x: int) -> bool:
    if x < 0:
        return False
    y = int("".join([f"{x}"[i] for i in range(f"{x}".__len__() - 1, -1, -1)]))
    return x == y


print(isPalindrome(-10))
