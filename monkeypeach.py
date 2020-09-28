# -*- coding: utf-8 -*-

import basetask

class MonkeyPeach(basetask.BaseTask):
    def __init__(self):
        self._name = "猴子分桃子"

    def do_cmd(self, src):
        NUM = int(src)
        i = 0
        j = 1
        k = 0
        while i < NUM :
            x = (NUM-1) * j
            for k in range(0, NUM):
                if (x % (NUM-1) != 0):
                    i = 0
                    break
                else:
                    i += 1
                x = (x / (NUM-1)) * NUM + 1
            j += 1
        return int(x)


