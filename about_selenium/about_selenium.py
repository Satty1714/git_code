# -*- coding:utf-8 -*-
# python3.6

from selenium import webdriver
from selenium.webdriver.support.select import Select

#补齐8位数
x = '123'
s = x.zfill(8)
a = 928
b = ("%08d" % a)
print(b)

brower = webdriver.Chrome()
#切换到指定表单
brower.switch_to.frame()
#切换到上一级表单
brower.switch_to.parent_frame()
#切换到最外层
brower.switch_to.default_content()
#获得当前窗口的句柄
now_handle = brower.current_window_handle
#获得所有句柄
all_handles = brower.window_handles
#切换窗口句柄
brower.switch_to.window()
#获得当前的url
currents_url = brower.current_url
