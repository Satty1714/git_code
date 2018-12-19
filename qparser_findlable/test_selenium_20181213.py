#coding:utf-8
#python:3
import sys
import time
import os
from time import sleep
from selenium import webdriver
import json
import getpass
from selenium.webdriver.common.keys import Keys

dirname, _ = os.path.split(os.path.abspath(__file__))

def GetTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

#是否输出打印信息
print_SIGN = True
def printt(everything, SIGN=True):
    if print_SIGN and SIGN:
        py_file = sys._getframe(0).f_back.f_code.co_filename.split("\\")[-1]
        py_file = py_file.ljust(15, " ")
        func_name = sys._getframe(0).f_back.f_code.co_name
        if func_name != "<module>":
            func_name = func_name + "()"
        else:
            func_name = "--------"
        func_name = func_name.ljust(10, " ")
        lines = str(sys._getframe(0).f_back.f_lineno).ljust(5, " ")
        print("{}{} {} {} {}".format(py_file, GetTime(), func_name, lines, everything))


def login(BASEURL):
    os.chdir("C:\python27")
    browser = webdriver.Chrome()
    browser.get(BASEURL)
    case_name = ""
    case_pwd = ""
    browser.find_element_by_xpath("//*[@id=\"frmLogin\"]/input[4]").send_keys(case_name)
    browser.find_element_by_xpath("//*[@id=\"frmLogin\"]/input[5]").send_keys(case_pwd)
    browser.find_element_by_xpath("//*[@id=\"frmLogin\"]/input[8]").click()
    browser.implicitly_wait(30)
    return browser

# 获得文本内容 测试通过
import traceback
def GetText_Xpath(browser, xpath, sign=True, count=0, text=""):
    while (sign):
        try:
            count += 1
            resolved_during_customer_browser = browser.find_element_by_xpath(xpath)
            text = resolved_during_customer_browser.text
            sign = False
        except:
            if count == 10:
                print("traceback.print_exc()")
                sign = False
                traceback.print_exc()
            else:
                print("sleep(1)")
                sleep(1)
    return text

def login_new(BASEURL):
    chromedriver_path = r"C:\Python27\chromedriver.exe"
    # browser = webdriver.Chrome()
    option = webdriver.ChromeOptions()
    # option.add_argument("--headless")
    option.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    option.add_argument('--start-maximized')
    # option.add_argument(
        # "--user-data-dir=" + r"C:\Users\{}\AppData\Local\Google\Chrome\User Data".format(getpass.getuser()))
    browser = webdriver.Chrome(chromedriver_path, chrome_options=option)
    browser.get(BASEURL)
    # case_name = ""
    # case_pwd = ""
    # browser.find_element_by_xpath('//*[@id="frmLogin"]/input[4]').send_keys(case_name)
    # browser.find_element_by_xpath('//*[@id="frmLogin"]/input[5]').send_keys(case_pwd)
    # browser.get_screenshot_as_file("{}\\login_new.png".format(dirname))
    # # browser.find_element_by_xpath('//*[@id="frmLogin"]/input[8]').click()
    browser.find_element_by_xpath('//*[@id="frmLogin"]/input[5]').send_keys(Keys.ENTER)
    # sleep(1000)
    browser.get_screenshot_as_file("{}\\Reports.png".format(dirname))
    browser.implicitly_wait(5)
    return browser

def Close(browser):
    browser.close()
    browser.quit()

def Main():
    printt("Main")
    BASEURL='https://qualcomm-cdmatech-support.my.salesforce.com/00O3A000009FfVy'#5003A00000t0SXa
    # # browser = login(BASEURL)
    def SaveCookies(browser):
        cookie = browser.get_cookies()
        # # 将获得cookie的信息打印
        # print(cookie)
        with open("{}\\cookies.txt".format(dirname), "w") as fp:
            json.dump(cookie, fp)

    def LoadCookies(browser, cookies_file):
        with open(cookies_file, "r") as fp:
            cookies = json.load(fp)
            for cookie in cookies:
                print(cookie)
                browser.add_cookie(cookie)
        return browser

    def login_cookies():
        chromedriver_path = r"C:\Python27\chromedriver.exe"
        # browser = webdriver.Chrome()
        option = webdriver.ChromeOptions()
        # option.add_argument("--headless")
        option.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
        option.add_argument('--start-maximized')
        option.add_argument(
            "--user-data-dir=" + r"C:\Users\{}\AppData\Local\Google\Chrome\User Data".format(getpass.getuser()))
        browser = webdriver.Chrome(chromedriver_path, chrome_options=option)
        browser.get(BASEURL)
        cookies_file = "{}\\png\\cookiesold.txt".format(dirname)
        sleep(10)
        browser = LoadCookies(browser,cookies_file)
        # with open("{}\\png\\cookies.txt".format(dirname), "r") as fp:
        #     cookies = json.load(fp)
        #     for cookie in cookies:
        #         print(cookie)
        #         browser.add_cookie(cookie)
        browser.get(BASEURL)

    # browser = login_new(BASEURL)
    browser = login(BASEURL)
    # html = browser.page_source.encode("gbk", "ignore")  # 将页面源码转成html文件
    # print(html)
    # with open("{}\\png\\html.html".format(dirname), "wb") as f:
    #     f.write(html)
    # case_status = GetText_Xpath(browser, '//*[@id="ep"]/div[2]/div[2]/table/tbody/tr[10]/td[2]')
    # print(case_status)
    SaveCookies(browser)
    # browser = login_cookies()

    # sleep(10000)


if __name__ == "__main__":
    printt("test new program {}".format("base_py_3"))
    Main()
    printt("test new program {}".format("base_py_3"))