# -*- coding: utf-8 -*-

import hashlib
import basetask

class Str2Md5(basetask.BaseTask):
    def __init__(self):
        self._name = "字符串转MD5"
        self._md5 = ""

    def do_cmd(self, src):
        self._md5 = hashlib.md5()
        self._md5.update(src.encode())
        return self._md5.hexdigest()


