from tkinter import *
root = Tk()
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
w=600
h=300
x=(screenWidth-w)/2
y=(screenHeight-h)/3
root.title("RPG maker MV 翻译向导")
root.geometry("%dx%d+%d+%d"%(w,h,x,y))
title=Label(root,text="1/5 选择游戏文件",anchor="w",font="yahei 13 bold",bg="white",fg="gray",padx=10,pady=10)
title.pack(fill=X)
content=Frame(root)
lab1=Label(content,text="游戏根目录")
lab1.pack()
ent1=Entry(content)
ent1.pack()
content.pack(fill=X

)
root.mainloop()