#!D:\ProgramFiles\Python\Python38\python.exe
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))

import unittest

from calculator import Calculator

class TestCalculator(unittest.TestCase):
    
    def test_1_input(self):
        obj = Calculator()
        self.assertRaises(Exception, obj.do_cmd, "12+(a-5)")
        self.assertRaises(Exception, obj.do_cmd, "*12+(6-5)")
        self.assertRaises(Exception, obj.do_cmd, "-*12+(6-5)")
        self.assertRaises(Exception, obj.do_cmd, "12+(5---5)")
        self.assertRaises(Exception, obj.do_cmd, "12+(5*+5)")
        self.assertRaises(Exception, obj.do_cmd, "12(3-5)")
        self.assertRaises(Exception, obj.do_cmd, "12*(3-5)6")
    
    def test_2_calculator(self):
        obj = Calculator()
        self.assertEqual(obj.do_cmd("1+2-3+4"), "4")
        self.assertEqual(obj.do_cmd("((4+1-2)*5+(5-4*1))/3"), "5.333333333333333")
        self.assertEqual(obj.do_cmd("2*(17-(-43)/(16-32))"), "28.625")
        self.assertEqual(obj.do_cmd("-3*-(8-3)+6/-3+5"), "18.0")
        self.assertEqual(obj.do_cmd("-3*-(8-3)+6/-3+5-(8-3)+4"), "17.0")
    
if __name__ =='__main__':
    unittest.main()
