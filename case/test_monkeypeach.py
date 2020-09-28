#!D:\ProgramFiles\Python\Python38\python.exe
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))

import unittest

from monkeypeach import MonkeyPeach

class TestMonkeyPeach(unittest.TestCase):
    
    def test_1_monkeypeach(self):
        obj = MonkeyPeach()
        self.assertEqual(obj.do_cmd("2"), 7)
        self.assertEqual(obj.do_cmd("3"), 25)
        self.assertEqual(obj.do_cmd("4"), 253)
        self.assertEqual(obj.do_cmd("5"), 3121)
    
if __name__ =='__main__':
    unittest.main()
