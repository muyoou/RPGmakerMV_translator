from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import *
import event
root = Tk()
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
w=460
h=260
x=(screenWidth-w)/2
y=(screenHeight-h)/3

apiSwitch=IntVar()
apiSwitch.set(1)

def switchApi():
    if apiSwitch.get()==2:
        ent2.config(state=DISABLED)
        ent3.config(state=DISABLED)
    else:
        ent2.config(state=NORMAL)
        ent3.config(state=NORMAL)

def browse():
    ent1.delete(0,END)
    ent1.insert(0,askdirectory(initialdir ='E:/Python'))

def switchGUI():
    event.beforeTranslate(ent1.get(),apiSwitch.get(),ent2.get(),ent3.get())
    content.pack_forget()
    translate.pack(anchor=W)
    title.config(text="2/2 开始翻译")
    lastStep.pack(side=RIGHT,padx=10,pady=5)
    nextStep.pack_forget()
    event.startThread()

def flcSwitchGUI():
    content.pack(anchor=W)
    title.config(text="1/2 设置必要信息")
    translate.pack_forget()
    nextStep.pack(side=RIGHT,padx=10,pady=5)
    lastStep.pack_forget()

root.title("RPG maker MV 翻译向导")
root.geometry("%dx%d+%d+%d"%(w,h,x,y))
title=Label(root,text="1/2 设置必要信息",anchor="w",font="yahei 13 bold",bg="white",fg="gray",padx=10,pady=10)
title.pack(fill=X)
content=Frame(root)
textbox=Frame(content)
lab1=Label(textbox,text="游戏根目录:")
lab1.pack(padx=10,pady=10)
lab2=Label(textbox,text="腾讯翻译API:")
lab2.pack()
textbox.pack(side=LEFT,anchor=N)
table=Frame(content)
table1=Frame(table)
ent1=Entry(table1,width=40)
ent1.pack(padx=10,pady=10,side=LEFT)
Button(table1,text="浏览",width=6,command=browse).pack(side=LEFT)
table1.pack()

table2=Frame(table)

table2_1=Frame(table2)
rbp=Radiobutton(table2_1,text="个人API",variable=apiSwitch,value=1,command=switchApi)
rbp.pack(side=LEFT)
rbp2=Radiobutton(table2_1,text="公用API(不推荐)",variable=apiSwitch,value=2,command=switchApi)
rbp2.pack(side=LEFT)
table2_1.pack()

table3=Frame(table2)
Label(table3,text=" ID ：").pack(side=LEFT)
ent2=Entry(table3,width=30)
ent2.pack(pady=10,side=LEFT)
table3.pack()

table3=Frame(table2)
Label(table3,text="Key：").pack(side=LEFT)
ent3=Entry(table3,width=30)
ent3.pack(pady=10,side=LEFT)
table3.pack()
Button(table2,text="怎么申请翻译API？",command=event.openWeb,borderwidth=0,fg="DeepSkyBlue").pack(side=LEFT)

table2.pack(side=LEFT)
table.pack(side=LEFT,anchor=W)
content.pack(anchor=W)

translate=Frame(root)
tips=Label(translate,text="正在统计任务量",padx=30,pady=10)
tips.pack(anchor=W)
pb=Progressbar(translate,length=400)
pb['maximum']=100
pb['value']=0
pb.pack(padx=30)
progressNum=Label(translate,text="进度：0/0")
progressNum.pack(anchor=W,padx=30)

buttonBar=Frame(root)
Button(buttonBar,text="退出",width=5,padx=10,command=event.closeProgram).pack(side=RIGHT,padx=10,pady=5)
nextStep=Button(buttonBar,text="下一步",width=5,padx=10,command=switchGUI)
nextStep.pack(side=RIGHT,padx=10,pady=5)
lastStep=Button(buttonBar,text="上一步",width=5,padx=10,command=flcSwitchGUI)
Button(buttonBar,text="关于",width=5,padx=10,command=event.openAbout).pack(side=LEFT,padx=10,pady=5)
buttonBar.pack(side=BOTTOM,fill=X)
#初始化event
event.root=root
event.event=event
event.proNum=progressNum
event.tip=tips
event.pb=pb
root.mainloop()
