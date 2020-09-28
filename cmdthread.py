# -*- coding: utf-8 -*-

import threading
import traceback
import debug
import str2md5
import monkeypeach
import fibonacci

class CmdThread(threading.Thread):
    def __init__(self, threadID, name, win, config):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.win = win
        self.config = config
        debug.log("CmdThread init " + self.name)
    
    def run(self):
        debug.log("Starting " + self.name)
        self.process_cmd(self.name, self.win)
        debug.log("Exiting " + self.name)

    def process_cmd(self, threadName, win):
        while True:
            debug.log("process_cmd(start)")
            self.config.con.acquire()
            if not self.config.workQueue.empty():
                cmd = int(self.config.workQueue.get())
                self.config.set_result("")
                self.config.set_log("")
                win.set_btn_status(False)
                try:
                    result = self.config.run_method()
                    if result is None:
                        self.config.set_result("None")
                        self.config.set_log("ERROR:" + self.config.get_cmd() + " result None")
                    else:
                        self.config.set_result(result)
                        self.config.set_log("INFO:" + self.config.get_cmd() + " success")
                except Exception as e:
                    debug.log(e)
                    if debug.get_enable():
                        self.config.set_log("EXPT:" + self.config.get_cmd() + " error \n%S" % traceback.format_exc())
                    else:
                        self.config.set_log("EXPT:" + self.config.get_cmd() + " error [%S]" % e)
                    debug.log("Exception : " + self.config.get_log())
                self.config.con.notify()
                debug.log("process_cmd(end) %s cmd %s result %s" % (threadName, cmd, self.config.get_result()))
                win.set_btn_status(True)
                win.update_info()
            else:
                self.config.con.wait()
                self.config.con.release()
                debug.log("process_cmd(end)")
