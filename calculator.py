# -*- coding: utf-8 -*-

import re
import basetask
import debug
from settings import Settings

class Calculator(basetask.BaseTask):
    
    __patterns = ['[^\d\+\-\*/\(\)]+',
                  '^[\+\*/]',
                  '^[\+\-\*/]{2}',
                  '[\+\-\*/]{3}',
                  '[\+\-\*/][\+\*/]',
                  '[\d][(]',
                  '[)][\d]']
    __convert = {' ':'', '++':'+', '+-':'-', '-+':'-', '--':'+'}
    
    def __init__(self):
        self._name = "计算器"

    def do_cmd(self, src):
        s = re.sub('\s', "", src)
        self.check_input(s)
        debug.log("do_cmd() s=[%s]" % s)
        result = self.priority(s)
        debug.log("do_cmd() result=[%s]" % result)
        return result

    def check_input(self, s):
        for pattern in Calculator.__patterns:
            if re.search(pattern, s):
                debug.log("check_input() Error input, Stop!")
                raise Exception('Input error : {} {}'.format(pattern, re.search(pattern, s)))
    
    def priority(self, s):
        while re.search('\([^()]+\)', s):
            temp = re.search('\([^()]+\)', s).group()
            [first, second] = s.split(temp, 1)
            temp = temp[1:-1]
            debug.log("priority() first[%s] temp[%s] second[%s]" % (first, temp, second))
            result = self.calculate(temp)
            debug.log("priority() result=[%s]" % result)
            s = self.format("%s%s%s" % (first, result, second))
            debug.log("priority() new s=[%s]" % s)
        return self.calculate(s)
    
    def format(self, s):
        for k, v in Calculator.__convert.items():
            s = s.replace(k, v)
        if s[:1] == "+":
            s = s[1:]
        return s
    
    def number(self, num):
        if re.search('\.', num):
            return float(num)
        else:
            return int(num)
    
    def compute(self, pattern, s):
        opt = re.search(pattern, s[1:]).group()
        idx = s[1:].find(opt)+1
        first = s[:idx]
        if re.search('[\+,\-,\*,/]', first[1:]):
            t_opt = re.findall('[\+,\-,\*,/]', first)[-1]
            t_idx = first.rfind(t_opt)
            first = first[t_idx+1:]
        second = s[idx+1:]
        if re.search('[\+,\-,\*,/]', second[1:]):
            t_opt = re.search('[\+,\-,\*,/]', second[1:]).group()
            t_idx = second[1:].find(t_opt)+1
            second = second[:t_idx]
        debug.log("compute() opt=[%s] idx=[%s] first=[%s] second=[%s]" % (opt, idx, first, second))
        fir = self.number(first)
        sec = self.number(second)
        if opt == '*':
            result = str(fir * sec)
        elif opt == '/':
            if Settings.get_instance().get_precision() == 0:
                result = str(fir // sec)
            elif Settings.get_instance().get_precision() == 1:
                result = str(fir / sec)
            else:
                if fir % sec == 0:
                    result = "商是：%d" % (fir // sec)
                else:
                    result = "商是：%d ，余数是：%d"% (fir // sec, fir % sec)
        elif opt == '+':
            result = str(fir + sec)
        else:
            result = str(fir - sec)
        s = re.sub('%s\%c%s' % (first, opt, second), result, s)
        s = self.format(s)
        debug.log("compute() result=[%s]" % s)
        return s
    
    def calculate(self, s):
        s = self.format(s)
        while re.search('[\*,/]', s[1:]):
            debug.log("calculate() s=[%s]" % s)
            s = self.compute('[\*,/]', s)
        while re.search('[\+,\-]', s[1:]):
            debug.log("calculate() s=[%s]" % s)
            s = self.compute('[\+,\-]', s)
        return s


