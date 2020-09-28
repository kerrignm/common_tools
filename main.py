#!D:\ProgramFiles\Python\Python38\python.exe
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
import cmdwin
import cmdthread
import config
import debug

root = Tk()
config = config.Config()

def on_closing():
    debug.log("on_closing()")
    root.destroy()
    exit(0)
    
def main():
    win = cmdwin.CmdWin(root, config)
    win.set_init_window()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    thread = cmdthread.CmdThread(1, "CmdThread", win, config)
    thread.setDaemon(True)
    thread.start()
    root.mainloop()

main()

