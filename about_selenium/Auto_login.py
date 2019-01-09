# -*- coding:utf-8 -*-
# python2.7

import os,sys
import time
import traceback
import getpass
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.select import Select

BaseUrl = "https://qualcomm-cdmatech-support.my.salesforce.com/00O3A000009FfVy"
chromedriver_path = r"C:\Python27\chromedriver.exe"

def GetTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# 是否输出打印信息
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



def GetTableRowsAndCols_xpath(browser, table_xpath, row_label, col_label):
    table = browser.find_element_by_xpath(table_xpath)
    table_rows = table.find_elements_by_tag_name(row_label)
    # 用1的原因：可能第一行是标题行数据会有不同
    table_cols = table_rows[0].find_elements_by_tag_name(col_label)
    return len(table_rows), len(table_cols)


def ErrorOrSleep(count, print_info="*" * 10, count_max=10):
    if count >= count_max:
        traceback.print_exc()
        return False
    else:
        print(print_info)
        sleep(0.5)
        return True


# 获得文本内容 测试通过
def GetText_Xpath(browser, xpath, sign=True, count=0, text=""):
    while (sign):
        try:
            count += 0.5
            resolved_during_customer_browser = browser.find_element_by_xpath(xpath)
            text = resolved_during_customer_browser.text
            sign = False
        except:
            sign = ErrorOrSleep(count)
    return text


# 单击操作 测试通过
def Click(browser, xpath, sign=True, count=0):
    while (sign):
        try:
            count += 0.5
            browser.find_element_by_xpath(xpath).click()
            sign = False
        except:
            sign = ErrorOrSleep(count)

# 清空编辑框内的值
def ClearInputText(browser, xpath_id, sign=True, count=0):
    while (sign):
        try:
            count += 0.5
            browser.find_element_by_id(xpath_id).clear()
            sign = False
        except:
            if count == 10:
                sign = False
                traceback.print_exc()
            else:
                time.sleep(0.5)


# 修改编辑框内的值
def ChangeInputText(browser, xpath_id, value, sign=True, count=0):
    # browser.find_element_by_id("baidu_translate_input").send_keys(self.subject.decode('utf-8'))

    while (sign):
        try:
            count += 0.5
            browser.find_element_by_id(xpath_id).send_keys(value.decode('utf-8'))

            sign = False
        except:
            if count == 10:
                sign = False
                traceback.print_exc()
            else:
                time.sleep(0.5)

#选择下拉框内容
def Selected(browser,xpath,val,sign=True,count=0):
    while sign:
        try:
            count += 0.5
            Select(browser.find_element_by_xpath(xpath)).select_by_value(val)
            #Select(browser.find_element_by_xpath(xpath)).select_by_index(val) 从0开始
            #Select(browser.find_element_by_xpath(xpath)).select_by_visible_text(val)
            sign = False
        except:
            sign = ErrorOrSleep(count)
#切换句柄
def HandOverHandle(browser):
    now_handle = browser.current_window_handle
    Click(browser, '//*[@id="pg:frm:pb:pbs1:Engineer_Name_lkwgt"]/img')
    all_handles = browser.window_handles
    for handle in all_handles:
        if now_handle != handle:
            browser.switch_to_window(handle)
            browser.switch_to.frame('searchFrame')
            browser.find_element_by_xpath('//*[@id="lksrch"]').send_keys('')
            Click(browser, '//*[@id="theForm"]/div/div[2]/input[2]')
            time.sleep(1)
            browser.switch_to.default_content()  # 切换到之前的frame
            browser.switch_to.frame('resultsFrame')
    browser.switch_to_window(now_handle)


def OpenChrome_(browser=None):
    os.environ['webdriver.chrome.driver']=chromedriver_path
    options = webdriver.ChromeOptions()
    # options.add_argument("--user-data-dir="+r"C:\Users\c_yansun\AppData\Local\Google\Chrome\User Data")
    options.add_argument("--user-data-dir=" + r"C:\Users\{}\AppData\Local\Google\Chrome\User Data".format(getpass.getuser()))
    if not browser:
        browser = webdriver.Chrome(chromedriver_path, chrome_options=options)
    browser.get(BaseUrl)
    sleep(5)
    try:
        browser.find_element_by_xpath("//*[@id=\"frmLogin\"]/input[8]").click()
    except:
        printt("browser already logged")
    browser.implicitly_wait(300)
    return browser


def main():

    browser = OpenChrome_()
    HandOverHandle(browser)


if __name__ == "__main__":
    main()