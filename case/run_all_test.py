#!D:\ProgramFiles\Python\Python38\python.exe
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os

case_path = os.getcwd()
report_path = os.getcwd()

def all_case():
    discover = unittest.defaultTestLoader.discover(case_path, pattern="test*.py", top_level_dir=None)
    return discover
    
if __name__ =='__main__':
    runner = unittest.TextTestRunner()
    runner.run(all_case())
