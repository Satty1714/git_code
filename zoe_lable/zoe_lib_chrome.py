import os
from time import sleep
from selenium import webdriver

os.chdir("C:\python27")
browser = webdriver.Chrome()
browser.get("https://qualcomm-cdmatech-support.my.salesforce.com/a2A?fcf=00B3A000009VOTB")
case_name = ""
case_pwd = ""
browser.find_element_by_xpath("//*[@id=\"frmLogin\"]/input[4]").send_keys(case_name)
browser.find_element_by_xpath("//*[@id=\"frmLogin\"]/input[5]").send_keys(case_pwd)
browser.find_element_by_xpath("//*[@id=\"frmLogin\"]/input[8]").click()
browser.implicitly_wait(30)
sleep(100000)