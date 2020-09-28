# -*- coding: utf-8 -*-

import basetask

class Fibonacci(basetask.BaseTask):
    def __init__(self):
        self._name = "斐波那契数"

    def do_cmd(self, src):
        NUM = int(src)
        result = 0
        if NUM<= 1:
            result = 1
        elif NUM == 2:
            result = 2
        else:
            i, result, j = 1, 2, 3
            while (j <= NUM):
                i, result = result, i + result
                j += 1
        return result


