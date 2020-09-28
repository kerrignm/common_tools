# -*- coding: utf-8 -*-

class BaseTask():
    def __init__(self):
        self._name = ""

    def get_cmd(self):
        return self._name

    def do_cmd(self, src):
        pass
        

