# -*- coding: utf-8 -*-

import os
import json
import debug

class Settings():

    __settings_file = "setting.ini"
    
    __s_instance = None
    
    def __init__(self):
        self.data = { 'mode' : 0,
                      'precision' : 0}
        self.read_settings()
        debug.set_enable(self.get_mode())
    
    @classmethod
    def get_instance(cls):
        if cls.__s_instance == None:
            cls.__s_instance = cls()
        return cls.__s_instance
    
    def read_settings(self):
        if not os.path.isfile(Settings.__settings_file):
            debug.log("read_settings() File not exist")
            self.write_settings()
        else:
            with open(Settings.__settings_file, 'r') as f:
                self.data = json.load(f)
            debug.log("read_settings() data = %s" % self.data)
        return self.data
    
    def write_settings(self):
        debug.log("write_settings()")
        with open(Settings.__settings_file, 'w') as f:
            json.dump(self.data, f)
    
    def get_mode(self):
        return self.data['mode']
    
    def set_mode(self, mode):
        debug.set_enable(mode)
        self.data['mode'] = mode
        self.write_settings()
    
    def get_precision(self):
        return self.data['precision']
    
    def set_precision(self, precision):
        self.data['precision'] = precision
        self.write_settings()
    
    
