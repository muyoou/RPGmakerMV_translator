import aboutme
import config
import thread
import core
from tkinter.messagebox import *
import webbrowser as web

#自身的对象
event=None

#---GUI对象---
#GUI根元素对象
root=None
#翻译时的状态框对象
tip=None
#翻译时的进度数字对象
proNum=None
#进度条对象
pb=None


#---操作对象---
#下载线程对象
tranThread=None
#核心类对象
coreClass=None
#关于页面的状态量
aboutState=0

#打开关于页面
def openAbout():
    aboutme.about(root,event)

#关闭程序
def closeProgram():
    root.destroy()

#翻译准备工作
def beforeTranslate(path,ops,id,key):
    config.rootPath=path
    config.path=path+r'\www\data'
    if ops==1:
        config.ApiID=id
        config.ApiKEY=key
    initCore()
    
#开启翻译线程
def startThread():
    global tranThread
    tranThread=thread.translate(event)
    tranThread.start()

#初始化并读取数据文件
def initCore():
    global coreClass
    coreClass = core.start(event)
    try:
        coreClass.getAllMapFileName()
    except:
        print("文件读取错误")
        showInfo("文件读取错误")
        changeTip("文件读取错误")
    print("初始化完成")

#检查并统计任务量
def getTaskNum():
    try:
        coreClass.getTaskNum()
    except:
        print("数据读取错误")
        showInfo("数据读取错误")
        changeTip("数据读取错误")
    if coreClass.allTaskNum==0:
        print("没有检测到数据文件")
        showInfo("没有检测到需要翻译的文件，请检查游戏根目录是否设置正确")
        changeTip("没有检测到需要翻译的文件，请检查游戏根目录是否设置正确")
    refreshNum()

#更改翻译时的状态提示框
def changeTip(content):
    tip.config(text=content)

#刷新翻译时的数字量
def refreshNum():
    proNum.config(text="进度："+str(coreClass.completedTaskNum)+'/'+str(coreClass.allTaskNum))
    pb['value']=int(coreClass.completedTaskNum/coreClass.allTaskNum*100)

#翻译
def startTranslate():
    for i in range(len(coreClass.mapFileName)):
        print("-----------"+coreClass.mapFileName[i]+"---------------")
        coreClass.getMapJsonData(i)
        if coreClass.getEventJsonByData(coreClass.dealString) == 'ERR':return 'ERR'
        coreClass.save(i)
        print("------------已完成-----------")
    coreClass.getCommonMapJsonData()
    print("一共有%d个句子"%(coreClass.allTaskNum))
    if coreClass.getEventJsonByCommon(coreClass.dealString) == 'ERR':return 'ERR'
    coreClass.saveCommon()
    coreClass.getItemJsonData()
    if coreClass.getItemJson(coreClass.dealString) == 'ERR':return 'ERR'
    coreClass.saveItem()

#显示警告框
def showInfo(content):
    showinfo("提示",content)

#打开申请界面
def openWeb():
    print("打开浏览器")
    web.open("https://www.muyoo.top/index.php/archives/74/")