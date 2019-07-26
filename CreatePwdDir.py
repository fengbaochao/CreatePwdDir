"""
@生成密码字典
@Author:Feng
@Date:2019-07-26
"""

# -*- coding: UTF-8 -*-
import itertools as its
from tkinter import *
import tkinter.filedialog
import tkinter
import rarfile
import os
import threading

def extractRar(filePath, pwd):
    extractPath = os.path.join(os.path.split(filePath)[0], 'extract')
    rf = rarfile.RarFile(filePath)
    try:
        rf.extractall(extractPath,pwd=pwd)
        return True
    except:
        return False

data = {
    'end': True,
    'filePath':'',
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
        data['end']= False
        data['words']= txtInfo.get('1.0',END)
        data['minLen']= int(txtMinLen.get())
        data['maxLen']= int(txtManLen.get())+1
        #form.quit()
        form.destroy()

    """
    取消事件
    """
    def cancel():
        global data
        data['end'] = True
        form.quit()

    """
    选择发生变化时触发
    """
    def checkChanged():
        numbers = '1234567890'
        lowerLetters = 'abcdefghijklmnopqrstuvwxyz'
        upperLetters = lowerLetters.upper()
        symbols = '~!@#$%^&*()_-=+{}[]\\|;:\'",.<>/?`'
        info=''

        if checkedOther.get():
            info = ''
        else:
            if checkedNumber.get():
                info+=numbers
            if checkedLower.get():
                info += lowerLetters
            if checkedUpper.get():
                info += upperLetters
            if checkedSymbol.get():
                info += symbols
        txtInfo['state'] = 'normal'
        txtInfo.delete(1.0, END)
        txtInfo.insert(INSERT, info)
        txtInfo['state'] =('normal' if checkedOther.get() else 'disabled')

    """
    选择文件
    """
    def chooseFile():
        global data
        filePath = tkinter.filedialog.askopenfilename(filetypes=[("rar文件","rar")])
        data['filePath']=filePath

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
    rowIndex = 0
    Label(form,text='密码生成设置',fg='blue',font=('微软雅黑',24)).grid(row=rowIndex,columnspan=4,sticky=W)
    rowIndex = rowIndex + 1
    Button(form, text="选择RAR文件", command=chooseFile).grid(row=rowIndex, sticky=N + W + S + E, padx=5, pady=5)

    list=[]
    list.append({'id':1,'text': '全部数字', 'variable': checkedNumber})
    list.append({'id':2,'text': '全部小写字母', 'variable': checkedLower})
    list.append({'id':3,'text': '全部大写字母', 'variable': checkedUpper})
    list.append({'id':4,'text': '全部特殊符号', 'variable': checkedSymbol})
    list.append({'id':4,'text': '用户自定义', 'variable': checkedOther})

    for check in list:
        rowIndex = rowIndex + 1
        Checkbutton(form, text=check['text'], variable=check['variable'],command=checkChanged).grid(row=rowIndex, columnspan=2, sticky=W)

    txtInfo=Text(form,width=60,height=4,state='normal')
    rowIndex = rowIndex + 1
    txtInfo.grid(row=rowIndex,columnspan=4,sticky=N+W+S+E, padx=5, pady=5)

    rowIndex = rowIndex + 1
    Label(form, text='最小长度').grid(row=rowIndex, column=0, sticky=W)
    # 设置text默认值
    default_value = StringVar()
    default_value.set('1')
    txtMinLen= Entry(form,width=10,textvariable=default_value)
    rowIndex = rowIndex + 1
    txtMinLen.grid(row=rowIndex, column=1)
    Label(form, text='最小长度').grid(row=rowIndex, column=2, sticky=W)
    default_value = StringVar()
    default_value.set('4')
    txtManLen=Entry(form,width=10,textvariable=default_value)
    txtManLen.grid(row=rowIndex, column=3)

    rowIndex = rowIndex + 1
    Button(form, text="确 定", command=enter).grid(row=rowIndex,column=2,sticky=N+W+S+E, padx=5, pady=5)
    Button(form, text="取 消", command=cancel).grid(row=rowIndex,column=3,sticky=N+W+S+E, padx=5, pady=5)
    #.Button(top, text="点我", command=helloCallBack)

    # 输出
    form.mainloop()
    return data

"""
创建密码字典并破解
"""
def createPwd(data):
    print(data)
    words = data['words'].replace('\n', '')
    minLen = data['minLen']
    maxLen = data['maxLen']
    filePath = data['filePath']

    dic = open('dictionary.txt', 'w')
    index = 0
    # 循环密码长度
    for num in range(minLen, maxLen):
        # 生成密码
        keys = its.product(words, repeat=num)
        for key in keys:
            index = index + 1
            pwd = "".join(key)
            dic.write(pwd + "\n")
            if len(filePath)>0:
                if extractRar(filePath, pwd):
                    print('次数', index, '密码', pwd, '破解成功！！！')
                    return 1
                else:
                    print('次数', index, '密码', pwd, '密码错误！！！')
            else:
                print('次数', index, '密码', pwd, '写入完成！！！')
    dic.close()

"""
主函数
"""
def main():
    # 创建控件
    data= createControls()
    if data['end']:
        return 1
    # 创建
    t = threading.Thread(target=createPwd, args=[data,])
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()
    # 阻塞--卡死界面！
    t.join()

if __name__=='__main__':
    print('生成密码字典')

    main()