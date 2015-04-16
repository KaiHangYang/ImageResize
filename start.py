#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ---------Edit By KaiHangYang----------
# -------------2015,04,12---------------
import os
import time
from Tkinter import *
from PIL import (
    Image,
    ImageTk,
)
import tkFileDialog
import tkMessageBox
# 下来是我自己的辅助库
import fileCheck
'''
    库引用说明：
        Tkinter 提供了GUI界面支持
        tkFileDialog提供了文件弹出窗口支持
        tkMessageBox提供了对话框支持
        PIL中的组件是提供图片打开支持的，用于在canvas上显示图片预览
'''

class Application():
    # 初始化
    def __init__(self):
        self.root = Tk()
        self.root.title("图片放大缩小的差值实现")
        # self.root.geometry("400x300")
        self.root.resizable(width=True, height=True)

        self._inited = False
        # 声明上层部件框
        self.menu = Menu(self.root)
        self.viewpanel = Frame(self.root)
        self.managepanel = Frame(self.root)
        # 视窗部件的初始化
        self.__menu()
        self.__scrollbar()
        self.__view()
        self.__manage()
        self.bind_all()

        self._inited = True

    def __menu(self):
        # 主菜单
        if self._inited:
            return

        self.root.config(menu=self.menu)
        # 文件菜单
        filemenu = Menu(self.menu, name="file")
        self.menu.add_cascade(label="文件", menu=filemenu)
        filemenu.add_command(label="打开", command=self._getFileName)

        filemenu.add_separator()
        filemenu.add_command(label="退出", command=self.root.quit)

    def __scrollbar(self):
        if self._inited:
            return

        # 后期要加上滚动事件
        self.hbar = Scrollbar(self.viewpanel, orient=HORIZONTAL)
        self.vbar = Scrollbar(self.viewpanel)

        # 位置，距离
        self.hbar.set(0, 0.5)
        self.vbar.set(0, 0.5)

        self.hbar.pack(side=BOTTOM, fill=X)
        self.vbar.pack(side=RIGHT, fill=Y)


    def __view(self):
        if self._inited:
            return

        self.viewpanel.pack(side=TOP, fill=X)
        self.canvas = Canvas(self.viewpanel)
        self.canvas.pack(expand=True, fill=BOTH)

        self.canvas.config(width=600, height=400)

    def __manage(self):
        if self._inited:
            return

        # 注意每次向console插入完数据之后需要使用 console.yview(END)来滚动到底
        self.managepanel.pack(side=BOTTOM, fill=X, pady=10)

        self.consolepanel = Frame(self.managepanel)
        self.controlpanel = Frame(self.managepanel)

        self.consolepanel.pack(side=LEFT, fill=Y, padx=10)
        self.controlpanel.pack(side=RIGHT, fill=Y, padx=10)

        self.controlpanel.columnconfigure(0, minsize=70)
        self.controlpanel.columnconfigure(1, minsize=70)
        self.controlpanel.columnconfigure(2, minsize=70)
        self.controlpanel.columnconfigure(3, minsize=70)
        # 首先是console
        self.console = Text(self.consolepanel, width=45, height=8, bd=1,
                            highlightbackground="grey", highlightthickness=1,
                            highlightcolor="grey")
        self.console.pack(expand=True, fill=BOTH, padx=5, pady=5)

        # 设置不同信息类型的样式
        self.console.tag_config("error", background="red", foreground="white")
        self.console.tag_config("warning", background="yellow", foreground="black")
        # 设置不能输入
        self.console.bind("<KeyPress>", lambda x: "break")
        self.console.focus_force()

        # 然后是control
        # 设置控制框标签
        self.fileName = StringVar()
        self.fileName.set("请选择图片文件")

        fileLabel = Label(self.controlpanel, textvariable=self.fileName, pady=2)

        algLabel = Label(self.controlpanel, text="选择算法：")
        sizeLabel = Label(self.controlpanel, text="放大倍数:")
        wLabel = Label(self.controlpanel, text="宽度", pady=2)
        hLabel = Label(self.controlpanel, text="高度", pady=2)
        # 设置控制控件
        self.fileBtn = Button(self.controlpanel, text="添加图片", pady=2)

        self.algNum = IntVar()
        algRadio = []
        algRadio.append(Radiobutton(self.controlpanel, variable=self.algNum,
                                    text="双线性", value=0, pady=2))
        algRadio.append(Radiobutton(self.controlpanel, variable=self.algNum,
                                    text="三次卷积", value=1, pady=2))

        # 大小的有效性验证
        def sizeValidate(content):
            return content.isdigit()

        self.wVar = StringVar()
        self.hVar = StringVar()
        wSize = Entry(self.controlpanel, textvariable=self.wVar, validate="key",
                      validatecommand=(self.root.register(sizeValidate), "%S"),
                      width=7)

        hSize = Entry(self.controlpanel, textvariable=self.hVar, validate="key",
                      validatecommand=(self.root.register(sizeValidate), "%S"),
                      width=7)

        self.preBtn = Button(self.controlpanel, text="预览", pady=3)
        self.genBtn = Button(self.controlpanel, text="保存",
                             command=lambda x: x, pady=3)
        # 规划布局
        fileLabel.grid(row=0, column=0, columnspan=2, sticky=W)
        self.fileBtn.grid(row=0, column=2, columnspan=2, sticky=W)

        algLabel.grid(row=1, column=0, sticky=W)
        algRadio[0].grid(row=2, column=0, columnspan=2)
        algRadio[1].grid(row=2, column=2, columnspan=2)

        sizeLabel.grid(row=3, column=0, sticky=W)
        wLabel.grid(row=4, column=0, sticky=E)
        wSize.grid(row=4, column=1, sticky=W)
        hLabel.grid(row=4, column=2, sticky=E)
        hSize.grid(row=4, column=3, sticky=W)

        self.preBtn.grid(row=5, column=0, columnspan=2)
        self.genBtn.grid(row=5, column=2, columnspan=2)

    def _getFileName(self):
        name = tkFileDialog.askopenfilename()
        if fileCheck.isImage(name)[0]:
            self.fileName.set(name)
        else:
            tkMessageBox.showerror(title="Error",
                                   message="类型错误："
                                   "打开的不是图片呦，是不是打开的方式不对？")

    def _preview(self):
        # 在显示图片的时候需要保存对于那个图片的引用，
        # 否则python会在这个函数结束的时候，image的所有引用都没了，
        # 图片就显示不出来了

        name = self.fileName.get()

        # 需要检测一下文件的类型
        if not fileCheck.isImage(name)[0]:
            tkMessageBox.showerror(title="Error",
                                   message="类型错误："
                                   "打开的不是图片呦，是不是打开的方式不对？")

        self.canvas.delete(ALL)
        self.image = ImageTk.PhotoImage(Image.open(name))
        width = self.image.width()
        height = self.image.height()

        self.canvas.create_image(width/2, height/2, image=self.image)
    def consoleNor(self, message):
        existContent = self.console.get("0.0", END)
        if existContent.count("\n") >= 50:
            self.console.delete("0.0", "2.0")

        self.console.insert(END, message+"\n")
        self.console.yview(END)

    def consoleWar(self, message):
        self.consoleNor(message)
        # 获取最后的输入的字符串的位置并且对于那段文字加上警告样式
        info = self.console.get("0.0", END).strip()
        info = info.split("\n")
        infoLen = len(info)
        print self.console.get(str(infoLen)+".0", END)
        self.console.tag_add("warning", str(infoLen)+".0", str(infoLen+1)+".0")

    def consoleErr(self, message):
        self.consoleNor(message)
        # 获取最后的输入的字符串的位置并且对于那段文字加上警告样式
        info = self.console.get("0.0", END).strip()
        info = info.split("\n")
        infoLen = len(info)
        print self.console.get(str(infoLen)+".0", END)
        self.console.tag_add("error", str(infoLen)+".0", str(infoLen+1)+".0")

    def bind_all(self):
        self.fileBtn.config(command=self._getFileName)
        self.preBtn.config(command=self._preview)

if __name__ == "__main__":
    app = Application()
    app.root.mainloop()
