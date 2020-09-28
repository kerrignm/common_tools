# -*- coding: utf-8 -*-

MODE = 0

def set_enable(enable):
    global MODE
    MODE = enable
    
def get_enable():
    return MODE
    
def log(s):
    if MODE : print(s)