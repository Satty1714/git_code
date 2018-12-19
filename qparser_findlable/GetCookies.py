# coding:utf-8
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import getpass

import traceback, os


# 清空编辑框内的值
def ClearInputText(browser, xpath, sign=True, count=0):
    while (sign):
        try:
            count += 0.5
            browser.find_element_by_xpath(xpath).clear()
            sign = False
        except:
            if count == 10:
                sign = False
                traceback.print_exc()
            else:
                sleep(0.5)


from selenium.webdriver.chrome.options import Options


def OpenChrome_():
    case_name, case_pwd = GetArgv()
    # print case_name;
    # print case_pwd;
    # sleep(10000);
    executable_path = r"C:\Python27\chromedriver.exe"
    os.environ['webdriver.chrome.driver'] = executable_path
    options = webdriver.ChromeOptions()  # 定义配置对象
    # options.add_argument("--user-data-dir="+r"C:\Users\c_yansun\AppData\Local\Google\Chrome\User Data")
    options.add_argument(
        "--user-data-dir=" + r"C:\Users\{}\AppData\Local\Google\Chrome\User Data".format(getpass.getuser()))
    browser = webdriver.Chrome(executable_path, chrome_options=options)
    case_name = ""
    case_pwd = ""
    browser.get('https://qualcomm-cdmatech-support.my.salesforce.com/00O3A000009HhDz')
    # sleep(2);
    # ClearInputText(browser,"//*[@id=\"frmLogin\"]/input[4]")
    # browser.find_element_by_xpath("//*[@id=\"frmLogin\"]/input[4]").send_keys(case_name)
    # ClearInputText(browser,"//*[@id=\"frmLogin\"]/input[5]")
    # browser.find_element_by_xpath("//*[@id=\"frmLogin\"]/input[5]").send_keysd_keys(case_pwd)
    try:
        browser.find_element_by_xpath("//*[@id=\"frmLogin\"]/input[8]").click()
    except:
        pass
    sleep(40)
    browser.implicitly_wait(120)
    browser.close()
    browser.quit()


import sys


def GetArgv():
    print("python_name: ", sys.argv[0])
    try:
        name = sys.argv[1]
        pwd = sys.argv[2]
    except:
        name = ""
        pwd = ""
    return name, pwd


OpenChrome_()


