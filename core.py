import json
import config
import os
import time
import re
import TencentAPI


class start():
    def __init__(self):
        self.indexs = [0, 0, 0, 0, 0]
        # 所有需要翻译的map文件名
        self.mapFileName = []
        # 当前map文件的json数据
        self.nowMapJson = None
        # 当前处理的句子
        self.nowString = None
        # 当前被分割的词汇列表
        self.nowSplitedList = []
        # 当前待翻译的词汇
        self.witeTranslate = None
        # 已经翻译完成的词汇
        self.finishTranslate = None
        self.savedChinese = []
        self.savedJapanese = []
        self.type = 0
        self.state = 1
        self.errorNum = 0

    def getAllMapFileName(self):
        for filename in os.listdir(config.path):
            if re.match('^Map\d+.json', filename):
                filename = os.path.join(config.path, filename)
                self.mapFileName.append(filename)

    def getCommonMapJsonData(self):
        self.getAJsonData("CommonEvents.json")

    def getItemJsonData(self):
        self.getAJsonData("Items.json")
    
    def getAJsonData(self,name):
        with open(os.path.join(config.path, name), 'r', encoding='utf-8') as f:
            self.nowMapJson = json.load(f)

    def getMapJsonData(self, index=0):
        with open(self.mapFileName[index], 'r', encoding='utf-8') as f:
            self.nowMapJson = json.load(f)

    def getEventJsonByData(self, callBake):
        self.state = 1
        for x, a in enumerate(self.nowMapJson['events']):
            self.indexs[0] = x
            if not a:
                continue
            for y, b in enumerate(a['pages']):
                self.indexs[1] = y
                for z, c in enumerate(b['list']):
                    self.getStringByEvent(z,c,callBake)


    def getStringByEvent(self,z,c,callBake):
        if c['code'] in (401, 402, 118, 119):
            self.type = 1
            self.indexs[2] = z
            for w, d in enumerate(c['parameters']):
                if d and isinstance(d, str):
                    self.indexs[3] = w
                    self.nowString = d
                    callBake()
        if c['code'] in (102, 101):
            self.type = 2
            self.indexs[2] = z
            for w, d in enumerate(c['parameters']):
                self.indexs[3] = w
                if not isinstance(d, int):
                    for v, e in enumerate(d):
                        if e and isinstance(e, str):
                            self.indexs[4] = v
                            self.nowString = e
                            callBake()

    def getEventJsonByCommon(self,callBake):
        self.state = 2
        for x,a in enumerate(self.nowMapJson):
            self.indexs[0] = x
            if not a:
                continue
            for y, b in enumerate(a['list']):
                self.getStringByEvent(y,b,callBake)

    def getItemJson(self,callBake):
        self.state = 3
        for x,a in enumerate(self.nowMapJson):
            self.indexs[0] = x
            if not a:
                continue
            if not a['description']=='':
                self.type = 1
                self.nowString = a['description']
                callBake()
            if not a['name']=='':
                self.type = 2
                self.nowString = a['name']
                callBake()

    def printString(self):
        print()

    def getEventJsonByCData(self, filter, function):
        for a in self.nowMapJson:
            if not a:
                continue
            for b in a['list']:
                filter(b, function)

    def eventFilter(self, event, function):
        if event['code'] in (401, 402, 118, 119):
            function(event)

    def dealString(self):
        print(self.nowString)
        self.spiltString()
        print(self.nowSplitedList)
        self.filter()
        self.nowString = ''.join(self.nowSplitedList)
        print(self.nowString)
        self.reSave()
        print()
        # self.tmpfun(self.whitList)

    def reSave(self):
        if self.state == 1:
            if self.type == 1:
                self.nowMapJson['events'][self.indexs[0]]['pages'][self.indexs[1]]['list'][self.indexs[2]]['parameters'][self.indexs[3]] = self.nowString
            elif self.type == 2:
                self.nowMapJson['events'][self.indexs[0]]['pages'][self.indexs[1]]['list'][self.indexs[2]]['parameters'][self.indexs[3]][self.indexs[4]] = self.nowString
        elif self.state == 2:
            if self.type == 1:
                self.nowMapJson[self.indexs[0]]['list'][self.indexs[2]]['parameters'][self.indexs[3]] = self.nowString
            elif self.type == 2:
                self.nowMapJson[self.indexs[0]]['list'][self.indexs[2]]['parameters'][self.indexs[3]][self.indexs[4]] = self.nowString
        elif self.state == 3:
            if self.type == 1:
                self.nowMapJson[self.indexs[0]]['description'] = self.nowString
            elif self.type == 2:
                self.nowMapJson[self.indexs[0]]['name'] = self.nowString

    def save(self, index=0):
        with open(self.mapFileName[index], 'w', encoding='utf-8') as f:
            json.dump(self.nowMapJson, f, ensure_ascii=False)

    def saveOne(self,name):
        with open(os.path.join(config.path, name), 'w', encoding='utf-8') as f:
            json.dump(self.nowMapJson, f, ensure_ascii=False)

    def saveCommon(self):
        self.saveOne("CommonEvents.json")

    def saveItem(self):
        self.saveOne("Items.json")

    def printthat(self, input):
        print(input)

    def spiltString(self):
        self.nowSplitedList = re.split(
            r'(<|>|\[\d+\]|「|」|\\.|\(|\)|\n)', self.nowString)

    def getTextBySave(self, input):
        index = self.savedJapanese.index(input)

    def filter(self):
        for index, item in enumerate(self.nowSplitedList):
            if item != '' and not re.match(r'[<>「」(\[\d+\])(\\.)a-zA-Z\d\s]+', item):
                if item in self.savedJapanese:
                    self.nowSplitedList[index] = self.savedChinese[self.savedJapanese.index(item)]
                else:
                    self.witeTranslate = item
                    self.translate()
                    self.nowSplitedList[index] = self.finishTranslate

    def translate(self):
        fin = TencentAPI.tran(self.witeTranslate)
        if fin == 'ERROR':
            print("机翻错误！")
            if self.errorNum >= 3:
                self.errorNum = 0
                self.inputByUser()
            else:
                self.errorNum+=1
                time.sleep(0.5)
                self.translate()

        self.savedJapanese.append(self.witeTranslate)
        self.savedChinese.append(fin)
        self.finishTranslate = fin

    def inputByUser(self):
        print("待翻译句子："+self.witeTranslate)
        minput = input("手动输入翻译")
        self.finishTranslate = minput
    def tmpfun(self, tmps):
        for init in range(len(tmps)):
            if not re.match('[<>「」(\[\d+\])(\\\\.)]+', tmps[init]) and tmps[init] != '':
                haveindex = 0
                try:
                    haveindex = self.oldtext.index(tmps[init])
                    tmps[init] = self.newtext[haveindex]
                except ValueError:
                    self.oldtext.append(tmps[init])
                    jifan = tran(tmps[init])
                    if(jifan == 'ERROR'):
                        tmps[init] = input("翻译：")
                    else:
                        tmps[init] = jifan
                    self.newtext.append(tmps[init])
                    #time.sleep(0.1)
        output = ''.join(tmps)
        print("机翻："+output)
        return output


s = start()
s.getAllMapFileName()

for i in range(len(s.mapFileName)):
    print("-----------"+s.mapFileName[i]+"---------------")
    s.getMapJsonData(i)
    s.getEventJsonByData(s.dealString)
    s.save(i)
    print("------------已完成-----------")
s.getCommonMapJsonData()
s.getEventJsonByCommon(s.dealString)
s.saveCommon()
s.getItemJsonData()
s.getItemJson(s.dealString)
s.saveItem()