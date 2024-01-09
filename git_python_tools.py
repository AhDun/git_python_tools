#coding=UTF-8

#
# Copyright (c) 2022-2023 AhDun
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

default_branch = 'master'


import os
import datetime
import subprocess 
import re

logo = '''
      ___                                   ___                                 ___           ___           ___     
     /  /\        ___           ___        /  /\        ___         ___        /__/\         /  /\         /__/\    
    /  /:/_      /  /\         /  /\      /  /::\      /__/|       /  /\       \  \:\       /  /::\        \  \:\   
   /  /:/ /\    /  /:/        /  /:/     /  /:/\:\    |  |:|      /  /:/        \__\:\     /  /:/\:\        \  \:\  
  /  /:/_/::\  /__/::\       /  /:/     /  /:/~/:/    |  |:|     /  /:/     ___ /  /::\   /  /:/  \:\   _____\__\:\ 
 /__/:/__\/\:\ \__\/\:\__   /  /::\    /__/:/ /:/   __|__|:|    /  /::\    /__/\  /:/\:\ /__/:/ \__\:\ /__/::::::::\\
 \  \:\ /~~/:/    \  \:\/\ /__/:/\:\   \  \:\/:/   /__/::::\   /__/:/\:\   \  \:\/:/__\/ \  \:\ /  /:/ \  \:\~~\~~\/
  \  \:\  /:/      \__\::/ \__\/  \:\   \  \::/       ~\~~\:\  \__\/  \:\   \  \::/       \  \:\  /:/   \  \:\  ~~~ 
   \  \:\/:/       /__/:/       \  \:\   \  \:\         \  \:\      \  \:\   \  \:\        \  \:\/:/     \  \:\     
    \  \::/        \__\/         \__\/    \  \:\         \__\/       \__\/    \  \:\        \  \::/       \  \:\    
     \__\/                                 \__\/                               \__\/         \__\/         \__\/     
'''






from tkinter import simpledialog
from tkinter import *
import tkinter.messagebox as messagebox
from tkinter import ttk

shell_exit = ""

root = Tk()
root.title("git_python_tools.py")
root.config(bg='#ffffff')
root.geometry('800x500+300+200')
root.resizable(0, 1)

shell_win = Text(root,font=("", 10),width=800,height=500)


shell_win.tag_config('T1C',foreground="#000000", font=("", 20, "bold"),justify="center")
shell_win.tag_config('T2C',foreground="#000000", font=("", 15, "bold"),justify="center")
shell_win.tag_config('T3C',foreground="#000000", font=("", 12, "bold"),justify="center")

shell_win.tag_config('T1',foreground="#000000", font=("", 20, "bold"))
shell_win.tag_config('T2',foreground="#000000", font=("", 15, "bold"))
shell_win.tag_config('T3',foreground="#000000", font=("", 12, "bold"))


shell_win.tag_config('error',foreground="red")
shell_win.tag_config('info',foreground="blue")
shell_win.tag_config('logo',foreground="#009000", font=("", 8, ""),justify="center")
shell_win.tag_config('welcome',foreground="#009000", font=("", 20, ""),justify="center")
shell_win.tag_config('log',foreground="#000090", font=("", 15, ""),justify="center")


def shell_error(res):
    output, error = res.communicate()
    if len(error.decode()) == 0:
        return 0
    else:
        return 1
    
# def shell_win_get_lines():
#     index  = shell_win.index("end-1c")
#     return index.split('.')[0]

def shell_win_insert(res):
    output, error = res.communicate()
    if shell_error(res) == 0:
        shell_win.insert(END, datetime.datetime.now().strftime("[%H:%M:%S]") + output.decode() + '\n','info')
    else:
        shell_win.insert(END, datetime.datetime.now().strftime("[%H:%M:%S]") + error.decode() + '\n','error')
    root.update()
    shell_win.see(END)

def shell(cmd):
    res = subprocess.Popen(cmd.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    shell_win_insert(res)
    return res
def git_exist():
    if os.path.isdir(".git") == 0:
        messagebox.showwarning("错误", "还没有仓库，请新建或克隆仓库 ")
        return True
    else:
        return False

def git_create():

    file = open('.gitignore','w+')

    file.write('git_python_tool.py\n')

    file.close()

    res = shell("git init")
    if shell_error(res) == 0:
        output, error = res.communicate()
        if (output.decode().find("Reinitialized existing Git repository")) != -1:
            messagebox.showerror("错误", "这里已经有仓库了")
        else:
            messagebox.showinfo("成功", "仓库创建成功")
    else:
        messagebox.showerror("错误", "发生异常")

def git_remove():
    if git_exist():
        return
    if messagebox.askyesno("警告！", "确定要删除仓库吗？") == False:
        return
    res = shell("rm -rf .git")
    messagebox.showinfo("成功", "仓库删除成功")

def git_reset():
    if git_exist():
        return
    if messagebox.askyesno("警告！", "确定要重置仓库吗？") == False:
        return
    res = shell("rm -rf .git")
    res = shell("git init")
    messagebox.showinfo("成功", "仓库重置成功")

def git_log():
    if git_exist():
        return
    cmd = 'git log'
    res = subprocess.Popen(cmd.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = res.communicate()
    sum = 0
    if shell_error(res) == 1:
         messagebox.showerror("错误", "查询错误")
    else:
        history = ''
        outputs = output.decode()
        while True:
            commit = ''
            result = re.search(r'commit.*\n', outputs)
            if result:
                commit = result.group(0)
                commit = re.sub(r'commit', '节点: ', commit)
                commit = re.sub(r'\n', '', commit)

            author = ''
            result = re.search(r'Author.*\n', outputs)
            if result:
                author = result.group(0)
                author = re.sub(r'Author', '作者', author)
                author = re.sub(r'\n', '', author)


            date = ''
            result = re.search(r'Date.*\n', outputs)
            if result:
                date = result.group(0)
                date = re.sub(r'Date: ', '', date)
                date = re.sub(r'\n', '', date)
                date = datetime.datetime.strptime(date.strip(), "%a %b %d %H:%M:%S %Y %z")
                date = str(date)
                date = re.sub(r'\+[\d]{1,2}:[\d]{1,2}', '', date)
                date = '时间: ' + date


            note = ''
            result = re.search(r'\n\n.*\n', outputs)

            if result:
                note = result.group(0)

                note = re.sub(r'\n', '', note)
                note = re.sub(r' ', '', note)
                note = '注释: ' + note



       
                
            
            history  = history +   commit + '\n' + author + '\n' + date + '\n' + note + '\n\n'
            history  = history + '-------------------------------------------------------\n\n'
            sum = sum + 1
  
            outputs = outputs[int(result.span(0)[1]):]
            if len(outputs) < 10:
                break

    shell_win.insert(END, '\n\n\n所有提交('+str(sum)+'次提交)\n\n' + history,'T2C')
    shell_win.insert(END, history,'log')
 
    root.update()

def git_remote_url_check():

    cmd = 'git remote -v'
    res = subprocess.Popen(cmd.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = res.communicate()

    if shell_error(res) == 1:
        config_url()
    if len(output) < 2:
        config_url()
        

def git_add_commit_push():
    if git_exist():
        return
    res = shell("git add .")
    if shell_error(res) == 1:
        output,error = res.communicate()
        if error.find("warning") == -1:
            messagebox.showerror("错误", "添加失败")
            return
    commit = simpledialog.askstring(title='',prompt='输入提交注释')
    if commit  == None:
        return
    res = shell("git commit -m" + commit)
    if shell_error(res) == 1:
        messagebox.showerror("错误", "提交失败")
        return
    
    switch = simpledialog.askstring(title='',prompt='输入提交分支(不输入默认'+default_branch+')')
    git_remote_url_check()
    if switch  == None:
        return
    if len(switch) == 0:
        switch = default_branch
    res = shell("git push origin " + switch)
    output,error = res.communicate()
    text = error.decode()
    print(text)
    if text.find(default_branch + ' ->') != -1:
        messagebox.showinfo("成功", "推送成功")
        return
    if text.find('Everything up-to-date') != -1:
        messagebox.showwarning("警告", "远程仓库已是最新的")
        return
    messagebox.showerror("错误", "推送失败")
    return
    

def git_add_commit():
    if git_exist():
        return
    res = shell("git add .")
    if shell_error(res) == 1:
        output,error = res.communicate()
        if error.find("warning") == -1:
            messagebox.showerror("错误", "添加失败")
            return
    commit = simpledialog.askstring(title='',prompt='输入提交注释')
    if commit  == None:
        return
    res = shell("git commit -m" + commit)
    if shell_error(res) == 1:
        messagebox.showerror("错误", "提交失败")
        return
    
def git_push():
    if git_exist():
        return
    switch = simpledialog.askstring(title='',prompt='输入提交分支(不输入默认'+default_branch+')')
    git_remote_url_check()
    if switch  == None:
        return
    if len(switch) == 0:
        switch = default_branch
    res = shell("git push origin " + switch)
    output,error = res.communicate()
    text = error.decode()
    print(text)
    if text.find(default_branch + ' ->') != -1:
        messagebox.showinfo("成功", "推送成功")
        return
    if text.find('Everything up-to-date') != -1:
        messagebox.showwarning("警告", "远程仓库已是最新的")
        return
    messagebox.showerror("错误", "推送失败")
    return
    
def git_clone():
    url = simpledialog.askstring(title='',prompt='输入克隆地址')
    if url  == None:
        return
    res = shell("git clone " + url)
    output,error = res.communicate()
    text = error.decode()
    if text.find('Cloning into') != -1:
        messagebox.showinfo("成功", "克隆成功")
    else:
        messagebox.showerror("错误", "克隆异常")
 
    
def git_pull():
    res = shell("git pull")

    output,error = res.communicate()
    text = output.decode()
    if text.find('Already up to date.') != -1:
        messagebox.showwarning("警告", "本地仓库已经是最新的")
        return
    if text.find('Already up to date.') != -1:
        messagebox.showwarning("警告", "本地仓库已经是最新的")
        return
    
def git_back():

    if messagebox.askyesno("警告！", "确定要回滚到上提交点吗？") == False:
        return

    git_remote_url_check()
    res = shell("git reset --hard HEAD~")
    if shell_error(res) == 1:
        messagebox.showerror("错误", "回滚失败")
        return
    else:
        messagebox.showinfo("成功", "回滚成功")
        return
    
def git_back_commit():
    if messagebox.askyesno("警告！", "确定要回滚指定提交点吗？") == False:
        return
    commit = simpledialog.askstring(title='',prompt='输入提交的节点值')
    git_remote_url_check()
    if commit  == None:
        return
    res = shell("git reset --soft "+commit)
    if shell_error(res) == 1:
        messagebox.showerror("错误", "回滚失败")
        return
    else:
        messagebox.showinfo("成功", "回滚成功")
        return

def start():
    shell_win.insert(END, logo,'logo')
    shell_win.insert(END, '\n\n\n\n','logo')
    shell_win.insert(END, '欢迎使用git-python工具\n\n','welcome')
    cmd = 'git log'
    res = subprocess.Popen(cmd.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = res.communicate()

    if os.path.isdir(".git") == 0:
        shell_win.insert(END, '还没有仓库，请新建或克隆仓库 \n\n','T2C')
        shell_win.insert(END, '菜单栏->仓库->新建/克隆 \n\n\n','T2C')
        root.update()
        return 

    if shell_error(res) == 1:
        shell_win.insert(END, '这里没有提交记录 \n\n','T2C')
        shell_win.insert(END, '菜单栏->推送->本地提交\n\n\n','T2C')
        root.update()
        return
    else:
        outputs = output.decode()
        commit = ''
        result = re.search(r'commit.*\n', outputs)
        if result:
            commit = result.group(0)
            commit = re.sub(r'commit', '节点: ', commit)
            commit = re.sub(r'\n', '', commit)

        author = ''

        result = re.search(r'Author.*\n', outputs)
        if result:
            author = result.group(0)
            author = re.sub(r'Author', '作者', author)
            author = re.sub(r'\n', '', author)


        date = ''
        result = re.search(r'Date.*\n', outputs)
        if result:
            date = result.group(0)
            date = re.sub(r'Date: ', '', date)
            date = re.sub(r'\n', '', date)
            date = datetime.datetime.strptime(date.strip(), "%a %b %d %H:%M:%S %Y %z")
            date = str(date)
            date = re.sub(r'\+[\d]{1,2}:[\d]{1,2}', '', date)
            date = '时间: ' + date


        note = ''
        result = re.search(r'\n\n.*\n', outputs)
        if result:
            note = result.group(0)
            note = re.sub(r'\n', '', note)
            note = re.sub(r' ', '', note)
            note = '注释: ' + note



  
        shell_win.insert(END, '您的上一次提交: \n\n','T2C')
        late  =   commit + '\n' + author + '\n' + date + '\n' + note + '\n\n'

        shell_win.insert(END, late,'log')
        root.update()
        return

    
    

def about():
    win = Tk()
    win.title("关于")
    win.geometry("350x230")
    win.resizable(0, 0)

    w_label0 = Label(win, height=2)
    w_label0.pack()

    w_label0 = Label(win, text="git-python工具", font=("", 20))   
    w_label0.pack()

    w_sep0 = ttk.Separator(win, orient='horizontal')
    w_sep0.pack(fill='x', padx=10, pady=10)

    
    w_label = Label(win, text="开发者: AhDun(DunHongWei)", font=("", 12))
    w_label.pack()

    w_sep = ttk.Separator(win, orient='horizontal')
    w_sep.pack(fill='x', padx=10, pady=10)

    w_label1 = Label(win, text="版本:v1.0(2024-1-8)", font=("", 12))
    w_label1.pack()

    w_sep1 = ttk.Separator(win, orient='horizontal')
    w_sep1.pack(fill='x', padx=10, pady=10)

    w_label2 = Label(win, text="开源协议:LICENSE-2.0(详情见源码)", font=("", 12))
    w_label2.pack()
    



def config_url():
    if git_exist():
        return
    url = simpledialog.askstring(title='',prompt='输入远程仓库地址 (http/https/git)')
    if url == None:
        return
    shell_error(shell("git remote rm origin "))
    if shell_error(shell("git remote add origin " + url)) == 1:
        messagebox.showwarning("错误", "远程仓库地址配置失败")
        return
    messagebox.showinfo("成功", "远程仓库地址配置成功")
    
    
def config_user_and_mail():
    user = simpledialog.askstring(title='',prompt='输入用户名')
    if user == None:
        return
    if shell_error(shell("git config --global user.name ") + user) == 1:
        messagebox.showwarning("错误", "用户名配置失败")
        return
    mail = simpledialog.askstring(title='',prompt='输入邮箱')
    if mail == None:
        return
    if shell_error(shell("git config --global user.email ") + mail) == 1:
        messagebox.showwarning("错误", "用户名配置失败")
        return
    messagebox.showinfo("成功", "用户名配置成功")
     

def git_url():
    cmd = 'git remote -v'
    res = subprocess.Popen(cmd.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = res.communicate()
    text = output.decode()
    text = re.sub('origin', '地址: ', text)
    text = re.sub('\(fetch\)', '', text)
    text = re.sub('\(push\)', '', text)
    shell_win.insert(END,'-------------------------------------------------------\n\n','log')
    shell_win.insert(END,text,'log')
    shell_win.insert(END,'\n-------------------------------------------------------\n\n','log')
    shell_win.see(END)
    shell_win.update()

def git_user_mail_info():
    cmd = 'git config user.name'
    res = subprocess.Popen(cmd.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = res.communicate()
    username = output.decode()

    cmd = 'git config user.email'
    res = subprocess.Popen(cmd.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = res.communicate()
    mail = output.decode()
    shell_win.insert(END,'-------------------------------------------------------\n\n','log')
    shell_win.insert(END,'用户名: ' + username,'log')
    shell_win.insert(END,'邮箱: ' + mail,'log')
    shell_win.insert(END,'\n-------------------------------------------------------\n\n','log')
    shell_win.see(END)
    shell_win.update()

    


main_menu = Menu(root,font=("", 15))


push_menu = Menu(main_menu, tearoff=0)
push_menu.add_command (label="本地提交并仓库推送 (F5)",command=git_add_commit_push)
root.bind("<F5>",lambda event:git_add_commit_push())
push_menu.add_command (label="本地提交",command=git_add_commit)
push_menu.add_command (label="仓库推送",command=git_push)
main_menu.add_cascade (label="推送", menu=push_menu)


# pull_menu = Menu(main_menu, tearoff=0)
# pull_menu.add_command (label="线上")
# main_menu.add_cascade (label="拉取", menu=pull_menu)

back_menu = Menu(main_menu, tearoff=0)

back_menu.add_command (label="上次提交",command=git_back)
back_menu.add_command (label="指定提交",command=git_back_commit)
main_menu.add_cascade (label="回滚", menu=back_menu)


store_menu = Menu(main_menu, tearoff=0)
store_menu.add_command (label="新建" ,command=git_create)
store_menu.add_command (label="拉取",command=git_pull)
store_menu.add_command (label="克隆" ,command=git_clone)
store_menu.add_command (label="重置" ,command=git_reset)
store_menu.add_command (label="删除" ,command=git_remove)

main_menu.add_cascade (label="仓库", menu=store_menu)

query_menu = Menu(main_menu, tearoff=0)
query_menu.add_command (label="所有提交",command=git_log)
query_menu.add_command (label="用户名和邮箱",command=git_user_mail_info)
query_menu.add_command (label="仓库地址",command=git_url)
main_menu.add_cascade (label="查询", menu=query_menu)

confing_menu = Menu(main_menu, tearoff=0)
confing_menu.add_command (label="仓库地址",command=config_url)
confing_menu.add_command (label="用户名和邮箱",command=config_user_and_mail)
main_menu.add_cascade (label="配置", menu=confing_menu)




main_menu.add_command (label="关于", command=lambda: about())



shell_win.insert(INSERT, shell_exit)

shell_win.pack()

start()


root.config(menu=main_menu)
root.mainloop()









