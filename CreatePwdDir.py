"""
生成密码字典
"""

# -*- coding: UTF-8 -*-
import itertools as its
from tkinter import *
import tkinter
import rarfile
import os

def extractRar(filepath,pwd):
    extractpath = os.path.join(os.path.split(filepath)[0], 'extract')
    rf = rarfile.RarFile(filepath)
    try:
        rf.extractall(extractpath,pwd=pwd)
        return True
    except:
        return False

data = {
    'end': True,
    'words': '',
    'minLen': 0,
    'maxLen': 0
}

"""
增加控件
"""
def createControls():
    """
    确定事件
    """
    def enter():
        global data
        data={
            'end': False,
            'words': txtInfo.get('1.0',END),
            'minLen': int(txtMinLen.get()),
            'maxLen': int(txtManLen.get())+1
        }
        form.quit()

    """
    取消事件
    """
    def cancel():
        global data
        data = {
            'end': True,
            'words': '',
            'minLen': 0,
            'maxLen': 0
        }
        form.quit()

    def checkChanged():
        numbers = '1234567890'
        lowerletters = 'abcdefghijklmnopqrstuvwxyz'
        upperletters = lowerletters.upper()
        symbols = '~!@#$%^&*()_-=+{}[]\\|;:\'",.<>/?`'
        info=''

        if checkedOther.get():
            info = ''
        else:
            if checkedNumber.get():
                info+=numbers
            if checkedLower.get():
                info += lowerletters
            if checkedUpper.get():
                info += upperletters
            if checkedSymbol.get():
                info += symbols
        txtInfo['state'] = 'normal'
        txtInfo.delete(1.0, END)
        txtInfo.insert(INSERT, info)
        txtInfo['state'] =('normal' if checkedOther.get() else 'disabled')

    form = tkinter.Tk()
    form.title('生成密码字典')
    form.resizable(0, 0)
    #form.geometry('500x300')  # 设置窗口大小
    # 是否选中标志 结果用.get()获取 True/False
    checkedNumber = BooleanVar()
    checkedLower = BooleanVar()
    checkedUpper = BooleanVar()
    checkedSymbol = BooleanVar()
    checkedOther=BooleanVar()

    # 创建控件
    Label(form,text='密码生成设置',fg='blue',font=('微软雅黑',24)).grid(row=0,columnspan=4,sticky=W)

    list=[]
    list.append({'id':1,'text': '全部数字', 'variable': checkedNumber})
    list.append({'id':2,'text': '全部小写字母', 'variable': checkedLower})
    list.append({'id':3,'text': '全部大写字母', 'variable': checkedUpper})
    list.append({'id':4,'text': '全部特殊符号', 'variable': checkedSymbol})
    list.append({'id':4,'text': '用户自定义', 'variable': checkedOther})

    rowIndex=1
    for check in list:
        Checkbutton(form, text=check['text'], variable=check['variable'],command=checkChanged).grid(row=rowIndex, columnspan=2, sticky=W)
        rowIndex=rowIndex+1

    txtInfo=Text(form,width=60,height=4,state='normal')
    txtInfo.grid(row=6,columnspan=4,sticky=N+W+S+E, padx=5, pady=5)

    Label(form, text='最小长度').grid(row=7, column=0, sticky=W)
    # 设置text默认值
    default_value = StringVar()
    default_value.set('1')
    txtMinLen= Entry(form,width=10,textvariable=default_value)
    txtMinLen.grid(row=7, column=1)
    Label(form, text='最小长度').grid(row=7, column=2, sticky=W)
    default_value = StringVar()
    default_value.set('4')
    txtManLen=Entry(form,width=10,textvariable=default_value)
    txtManLen.grid(row=7, column=3)

    Button(form, text="确 定", command=enter).grid(row=8,column=2,sticky=N+W+S+E, padx=5, pady=5)
    Button(form, text="取 消", command=cancel).grid(row=8,column=3,sticky=N+W+S+E, padx=5, pady=5)
    #.Button(top, text="点我", command=helloCallBack)

    # 输出
    form.mainloop()
    return data

def main():
    # 创建控件
    data= createControls()
    if data['end']:
        return 1

    words=data['words'].replace('\n','')
    minlen=data['minLen']
    maxlen = data['maxLen']

    #dic = open('dictionary.txt', 'w')
    # 循环密码长度
    for num in range(minlen, maxlen):
        # 生成密码
        keys = its.product(words, repeat=num)
        for key in keys:
            pwd="".join(key)
            if extractRar(r'E:\test\txt.rar',pwd):
                print(pwd,'破解成功！！！')
                return 1
            else:
                print(pwd,'密码错误！！！')
            #dic.write("".join(key) + "\n")
    #dic.close()

if __name__=='__main__':
    print('生成密码字典')

    main()