# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-01-12 11:27:07
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-01-12 14:04:09

from collections import namedtuple


Result = namedtuple("Result", "count average")

li = [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5]

# 子生成器


def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total/count

    return Result(count, average)

# 委派生成器


def grouper(result, key):
    while True:

        result[key] = yield from averager()
        print(result, key, result[key])

# 调用方


def main():
    results = {}
    group = grouper(results, "kg")
    next(group)
    for value in li:
        group.send(value)
    group.send(None)
    print(results)


if __name__ == "__main__":
    main()
