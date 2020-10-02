# -*- coding: utf-8 -*-

from tkinter import *
import time
import debug
from settings import Settings

class CmdWin():
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.select = IntVar()
        self.mode = IntVar()
        self.precision = IntVar()
        self.line_num = 0


    def set_init_window(self):
        self.root.title("CommonTools_v1.0")
        
        scn_w, scn_h = self.root.maxsize()
        curWidth = 800
        curHight = 600
        size_xy = '%dx%d+%d+%d' % (curWidth, curHight, (scn_w-curWidth)/2, (scn_h-curHight)/2)
        self.root.geometry(size_xy)
        self.root.resizable(0, 0)
        
        menubar = Menu(self.root)
        task_menu = Menu(menubar, tearoff=False)
        self.select.set(0)
        menubar.add_cascade(label="任务选项", menu=task_menu)
        for cmd in self.config.CMDS:
            task_menu.add_radiobutton(label=cmd.task.get_cmd(), command=self.cmd_callback, variable=self.select, value=cmd.id)
            if cmd.sept:
                task_menu.add_separator()
        
        set_menu = Menu(menubar, tearoff=False)
        set_menu.mode_menu = Menu(set_menu, tearoff=False)
        self.mode.set(Settings.get_instance().get_mode())
        set_menu.mode_menu.add_radiobutton(label="发布版", command=self.mode_callback, variable=self.mode, value=0)
        set_menu.mode_menu.add_separator()
        set_menu.mode_menu.add_radiobutton(label="调试版", command=self.mode_callback, variable=self.mode, value=1)
        set_menu.add_cascade(label="模式", menu=set_menu.mode_menu)
        
        set_menu.calculate_menu = Menu(set_menu, tearoff=False)
        self.precision.set(Settings.get_instance().get_precision())
        set_menu.calculate_menu.add_radiobutton(label="整数", command=self.calculate_callback, variable=self.precision, value=0)
        set_menu.calculate_menu.add_separator()
        set_menu.calculate_menu.add_radiobutton(label="小数", command=self.calculate_callback, variable=self.precision, value=1)
        set_menu.calculate_menu.add_separator()
        set_menu.calculate_menu.add_radiobutton(label="余数", command=self.calculate_callback, variable=self.precision, value=2)
        set_menu.add_separator()
        set_menu.add_cascade(label="精度", menu=set_menu.calculate_menu)
        
        menubar.add_cascade(label="设置", menu=set_menu)
        self.root.config(menu=menubar)
        
        self.input_label = Label(self.root, text="输入数据")
        self.input_label.grid(row=0, column=0)
        self.output_label = Label(self.root, text="输出结果")
        self.output_label.grid(row=0, column=12)
        self.log_label = Label(self.root, text="日志")
        self.log_label.grid(row=12, column=0)
        
        self.input_text = Text(self.root, width=50, height=35)
        self.input_text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.output_text = Text(self.root, width=50, height=35)
        self.output_text.grid(row=1, column=12, rowspan=10, columnspan=10)
        self.log_text = Text(self.root, width=110, height=9)
        self.log_text.grid(row=13, column=0, columnspan=22)
        
        self.cmd_text = StringVar()
        self.cmd_button = Button(self.root, textvariable=self.cmd_text, bg="lightskyblue", width=10, state='normal')
        self.cmd_text.set(self.config.get_cmd())
        self.cmd_button.grid(row=0, column=11)
        self.run_text = StringVar()
        self.run_button = Button(self.root, textvariable=self.run_text, bg="lightblue", width=10,command=self.do_cmd)
        self.run_button.grid(row=2, column=11)
        self.run_text.set(self.config.get_run_label())
    
    def set_btn_status(self, status):
        if status:
            self.run_button['state']='normal'
        else:
            self.run_button['state']='disabled'
    
    def cmd_callback(self):
        debug.log("cmd_callback() value = %s" % self.select.get())
        self.config.set_id(self.select.get())
        self.cmd_text.set(self.config.get_cmd())
        self.run_text.set(self.config.get_run_label())
        
    def mode_callback(self):
        debug.log("mode_callback() value = %s" % self.mode.get())
        Settings.get_instance().set_mode(self.mode.get())
        
    def calculate_callback(self):
        debug.log("calculate_callback() value = %s" % self.precision.get())
        Settings.get_instance().set_precision(self.precision.get())

    def do_cmd(self):
        src = self.input_text.get(1.0, END).strip().replace("\n", "")
        debug.log("do_cmd() src = " + src)
        if src:
            self.config.set_data(src)
            self.post_cmd(self.config.get_id())
        else:
            self.output_text.delete(1.0, END)
            self.write_log_to_text("ERROR:" + self.config.get_cmd() + " failed")
        
    def post_cmd(self, cmd):
        debug.log("post_cmd(start)")
        self.config.con.acquire()
        debug.log("post_cmd(doing)")
        self.config.workQueue.put(cmd)
        self.config.con.notify()
        self.config.con.release()
        debug.log("post_cmd(end)")
        
    def update_info(self):
        debug.log("updata_info() result : {%s}" % self.config.get_result())
        if len(str(self.config.get_result())):
            self.output_text.delete(1.0, END)
            self.output_text.insert(1.0, self.config.get_result())
            self.write_log_to_text(self.config.get_log())
        else:
            self.output_text.delete(1.0, END)
            self.write_log_to_text(self.config.get_log())
        
    def write_log_to_text(self, log):
        current_time = self.get_current_time()
        log_in = str(current_time) + " " + str(log) + "\n"
        if self.line_num < 200:
            self.log_text.insert(END, log_in)
            self.line_num += 1
        else:
            self.output_text.delete(1.0, 2.0)
            self.log_text.insert(END, log_in)
        self.log_text.see(END)
        
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

