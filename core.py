import json
import config
import os
import time
import re
import TencentAPI


class start():
    def __init__(self,event):
        self.indexs = [0, 0, 0, 0, 0]
        self.event=event
        # 需翻译的总句子量
        self.allTaskNum=0
        # 已经翻译的句子量
        self.completedTaskNum=0
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
                    if self.getStringByEvent(z,c,callBake) == 'ERR':return 'ERR'


    def getStringByEvent(self,z,c,callBake):
        if c['code'] in (401, 402, 118, 119,101):
            self.type = 1
            self.indexs[2] = z
            for w, d in enumerate(c['parameters']):
                if d and isinstance(d, str):
                    self.indexs[3] = w
                    self.nowString = d
                    if callBake() == 'ERR':return 'ERR'
        if c['code'] == 102:
            self.type = 2
            self.indexs[2] = z
            for w, d in enumerate(c['parameters']):
                self.indexs[3] = w
                if not isinstance(d, int):
                    for v, e in enumerate(d):
                        if e and isinstance(e, str):
                            self.indexs[4] = v
                            self.nowString = e
                            if callBake() == 'ERR':return 'ERR'

    def getEventJsonByCommon(self,callBake):
        self.state = 2
        for x,a in enumerate(self.nowMapJson):
            self.indexs[0] = x
            if not a:
                continue
            for y, b in enumerate(a['list']):
                if self.getStringByEvent(y,b,callBake) == 'ERR':return 'ERR'

    def getItemJson(self,callBake):
        self.state = 3
        for x,a in enumerate(self.nowMapJson):
            self.indexs[0] = x
            if not a:
                continue
            if not a['description']=='':
                self.type = 1
                self.nowString = a['description']
                if callBake() == 'ERR':return 'ERR'
            if not a['name']=='':
                self.type = 2
                self.nowString = a['name']
                if callBake() ==  'ERR':return 'ERR'

    def printString(self):
        print()

    def getEventJsonByCData(self, filter, function):
        for a in self.nowMapJson:
            if not a:
                continue
            for b in a['list']:
                if filter(b, function) == 'ERR':return 'ERR'

    def eventFilter(self, event, function):
        if event['code'] in (401, 402, 118, 119):
            function(event)

    def dealString(self):
        print(self.nowString)
        self.spiltString()
        print(self.nowSplitedList)
        if self.filter()=='ERR': return 'ERR'
        self.nowString = ''.join(self.nowSplitedList)
        print(self.nowString)
        self.reSave()
        self.completedTaskNum+=1
        self.event.refreshNum()
        print()
        # self.tmpfun(self.whitList)

    def reSave(self):
        if self.state == 1:
            if self.type == 1:
                self.nowMapJson['events'][self.indexs[0]]['pages'][self.indexs[1]]['list'][self.indexs[2]]['parameters'][self.indexs[3]] = self.nowString
            elif self.type == 2:
                print("DEBUG")
                print(self.nowMapJson['events'][self.indexs[0]]['pages'][self.indexs[1]]['list'][self.indexs[2]]['parameters'])
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
                    if self.translate()=='ERR':return 'ERR'
                    self.nowSplitedList[index] = self.finishTranslate

    def translate(self):
        time.sleep(0.1)
        fin = TencentAPI.tran(self.witeTranslate)
        if fin == 'ERROR':
            print("机翻错误！")
            if self.errorNum >= 3:
                self.errorNum = 0
                #self.inputByUser()
                self.finishTranslate=self.witeTranslate
            else:
                self.errorNum+=1
                time.sleep(0.5)
                self.translate()
        elif fin == "API_ERR":
            self.event.showInfo("翻译API不存在，请检查ID和KEY是否输入正确")
            return 'ERR'
        self.savedJapanese.append(self.witeTranslate)
        self.savedChinese.append(fin)
        self.finishTranslate = fin

    def inputByUser(self):
        print("待翻译句子："+self.witeTranslate)
        minput = input("手动输入翻译")
        self.finishTranslate = minput

    def getTaskNum(self):
        for i in range(len(self.mapFileName)):
            print("-----------"+self.mapFileName[i]+"---------------")
            self.getMapJsonData(i)
            self.getEventJsonByData(self.addOneNum)
        self.getCommonMapJsonData()
        self.getEventJsonByCommon(self.addOneNum)
        self.getItemJsonData()
        self.getItemJson(self.addOneNum)
        print("一共有%d个句子"%(self.allTaskNum))
        
    def addOneNum(self):
        self.allTaskNum+=1



