import threading
import time
class translate(threading.Thread):
    def __init__(self,event):
        threading.Thread.__init__(self)
        self.event=event

    def run(self):
        print("翻译线程开始")
        self.event.getTaskNum()
        self.event.changeTip("准备开始")
        if self.event.startTranslate() =='ERR':
            self.event.changeTip("翻译失败")
        else:
            self.event.changeTip("翻译完成！直接退出即可")