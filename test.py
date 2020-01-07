from selenium import webdriver
from time import sleep
import tkinter as tk
import tkinter.messagebox
import json

usr_name=input('请输入用户名，回车键结束：')
usr_pwd=input('请输入密码，回车键结束：')
f=False
flag1=False
var_usr_name=None
var_usr_pwd=None
window=None
'''
def usr_log_in():
    global usr_name
    global usr_pwd
    global f
    global var_usr_name
    global var_usr_pwd
    usr_name=var_usr_name.get()
    usr_pwd=var_usr_pwd.get()
    f=True
    window.destroy()

def login():
    global var_usr_name
    global var_usr_pwd
    global window
    window=tk.Tk()
    window.title('rookie选择题自动答题系统')
    window.geometry('450x190')
    window.resizable(False,False,)

    tk.Label(window,text='请确保用户名密码正确和没有考试中的考卷').place(x=120,y=10)
    tk.Label(window,text='用户名:').place(x=100,y=50)
    tk.Label(window,text='密码:').place(x=100,y=90)
    tk.Label(window,text='Made By steven12138').place(x=310,y=170)

    var_usr_name=tk.StringVar()
    entry_usr_name=tk.Entry(window,textvariable=var_usr_name)
    entry_usr_name.place(x=160,y=50)
    var_usr_pwd=tk.StringVar()
    entry_usr_pwd=tk.Entry(window,textvariable=var_usr_pwd)
    entry_usr_pwd.place(x=160,y=90)
    bt_login=tk.Button(window,text='登录',command=usr_log_in)
    bt_login.place(x=200,y=130)
    tkinter.messagebox.showwarning('提示', '自动答题过程中可以切换到其他窗口')
    window.mainloop()

login()

if not f:
	exit(0)'''

driver = webdriver.Chrome()
print('正在打开中')

driver.get("http://rookie.pkuschool.edu.cn/login")
sleep(0.5)

def getid(uid,d):
	d=d-1
	return uid*4+d

def dpair(a,b):
	k=0
	if not a:
		return 0
	for i in b:
		if not i in a:
			return k
		k=k+1
	return None

lastcookie=[]

def getans(driver):
	global lastcookie
	global num
	cookie=driver.get_cookies()
	uidcookie=[]
	for i in cookie:
		if "choice" in i['name']:
			uidcookie.append((i['name'],i['value']))
	lastcookie.sort()
	uidcookie.sort()
	k=dpair(lastcookie,uidcookie)
	res=uidcookie[dpair(lastcookie,uidcookie)][1]
	if res:
		lastcookie.append(uidcookie[k])
	return (res=="1")


# 开始登录
# 1. 让司机找用户名的输入框
we_account = driver.find_element_by_css_selector('#loginUsername')
we_account.clear()
we_account.send_keys(usr_name)
 
# 2. 让司机找密码的输入框
we_password = driver.find_element_by_css_selector('#loginPassword')
we_password.clear()
we_password.send_keys(usr_pwd)
 
# 3. 让司机找 登录按钮 并 单击
driver.find_element_by_css_selector('#btn_login').click()
sleep(1)

driver.get("http://rookie.pkuschool.edu.cn/test-center")

driver.find_element_by_css_selector('.addTestPaper').click()
sleep(1)
driver.find_element_by_css_selector('.start-or-continue').click()
sleep(1)

btn=driver.find_elements_by_css_selector('[href="#"]')

num=len(btn)//4
print(num)

for i in range(num):
	for k in range(4):
		btn[getid(i,k+1)].click()
		sleep(3.2)
		s=getans(driver)
		if s:
			break

driver.find_element_by_css_selector('#paper-submit').click()
sleep(0.2)
alert=driver.switch_to_alert()
alert.accept()

tkinter.messagebox.showwarning('提示','程序自动答题完成请查看是否正确')