from tkinter import *
root = Tk()
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
w=600
h=300
x=(screenWidth-w)/2
y=(screenHeight-h)/3

apiSwitch=IntVar()
apiSwitch.set(1)

root.title("RPG maker MV 翻译向导")
root.geometry("%dx%d+%d+%d"%(w,h,x,y))
title=Label(root,text="1/5 选择游戏文件",anchor="w",font="yahei 13 bold",bg="white",fg="gray",padx=10,pady=10)
title.pack(fill=X)
content=Frame(root)
lab1=Label(content,text="游戏根目录:")
lab1.pack(padx=20,pady=10)
lab2=Label(content,text="腾讯翻译API:")
lab2.pack()
content.pack(side=LEFT,anchor=N)
table=Frame(root)
table1=Frame(table)
ent1=Entry(table1)
ent1.pack(padx=20,pady=10,side=LEFT)
Button(table1,text="浏览").pack(side=LEFT)
table1.pack()
table2=Frame(table)
rbp=Radiobutton(table2,text="个人API",variable=apiSwitch,value=1)
rbp.pack(side=LEFT)
rbp2=Radiobutton(table2,text="公用API(不推荐)",variable=apiSwitch,value=2)
rbp2.pack(side=LEFT)
table2.pack()
ent2=Entry(table)
ent2.pack(padx=20,pady=10)
ent3=Entry(table)
ent3.pack(padx=20,pady=10)
table.pack(side=LEFT,anchor=NW)
root.mainloop()