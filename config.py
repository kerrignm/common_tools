# -*- coding: utf-8 -*-

from collections import namedtuple
import queue
import threading
import str2md5
import monkeypeach
import fibonacci
import calculator

CMD = namedtuple('CMD', 'id sept label task')

class Config():
    def __init__(self):
        self.id = 0
        self.data = ""
        self.result = ""
        self.log = ""
        
        self.con = threading.Condition()
        self.workQueue = queue.Queue(10)
        
        self.CMDS = [CMD(0, 1, "转换", str2md5.Str2Md5()),
                     CMD(1, 1, "运行", monkeypeach.MonkeyPeach()),
                     CMD(2, 1, "运行", fibonacci.Fibonacci()),
                     CMD(3, 0, "计算", calculator.Calculator())]
    
    def get_id(self):
        return self.id
    
    def set_id(self, id):
        self.id = id
    
    def get_data(self):
        return self.data
    
    def set_data(self, data):
        self.data = data
    
    def get_result(self):
        return self.result
    
    def set_result(self, result):
        self.result = result
    
    def get_log(self):
        return self.log
    
    def set_log(self, log):
        self.log = log
    
    def get_cmd(self):
        return self.CMDS[self.id].task.get_cmd()
    
    def get_run_label(self):
        return self.CMDS[self.id].label
    
    def run_method(self):
        return self.CMDS[self.id].task.do_cmd(self.data)
    
