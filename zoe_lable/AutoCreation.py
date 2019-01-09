# coding:utf-8
# python:3
import sys
import time
import os
import getpass
import traceback
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.select import Select

base_url = "https://qualcomm-cdmatech-support.my.salesforce.com/a2A?fcf=00B3A000009VOTB"
Excel_name = "China Camera CE Services mapping_for CE Service Creation_20190102.xlsx"

dirname_tool, _ = os.path.split(os.path.abspath(__file__))
chromedriver_path = "{}\\tools\\chromedriver\\chromedriver.exe".format(dirname_tool)
cookies_path = r"C:\Users\{}\Downloads".format(getpass.getuser())

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
        print("[{}] {} {} {} {}".format(py_file, GetTime(), func_name, lines, everything))

def ErrorOrSleep(count, print_info="*" * 10, count_max=10):
    if count >= count_max:
        traceback.print_exc()
        return False
    else:
        print(print_info)
        time.sleep(0.5)
        return True

# 单击操作 测试通过
def Click(browser, xpath, sign=True, count=0):
    while (sign):
        try:
            count += 0.5
            browser.find_element_by_xpath(xpath).click()
            sign = False
        except:
            sign = ErrorOrSleep(count)

# 选择下拉框内容
def Selected(browser, xpath, val, sign=True, count=0):
    while sign:
        try:
            count += 0.5
            Select(browser.find_element_by_xpath(xpath)).select_by_value(val)
            # Select(browser.find_element_by_xpath(xpath)).select_by_index(val) 从0开始
            # Select(browser.find_element_by_xpath(xpath)).select_by_visible_text(val)
            sign = False
        except:
            sign = ErrorOrSleep(count)

def SendKey(browser,xpath,val,sign=True,count=0):
    while (sign):
        try:
            count += 0.5
            browser.find_element_by_xpath(xpath).send_keys(val)
            sign = False
        except:
            if count == 10:
                sign = False
                traceback.print_exc()
            else:
                time.sleep(1)

def GetText_Xpath(browser, xpath, sign=True, count=0, text=""):
    while (sign):
        try:
            count += 0.5
            resolved_during_customer_browser = browser.find_element_by_xpath(xpath)
            text = resolved_during_customer_browser.text
            sign = False
        except:
            if count == 10:
                sign = False
                traceback.print_exc()
            else:
                time.sleep(1)
    return text

def GetTableRowsAndCols_xpath(browser, table_xpath, row_label, col_label):
    table = browser.find_element_by_xpath(table_xpath)
    table_rows = table.find_elements_by_tag_name(row_label)
    # 用1的原因：可能第一行是标题行数据会有不同
    table_cols = table_rows[0].find_elements_by_tag_name(col_label)
    return len(table_rows), len(table_cols)

def OpenChrome_(browser, sign):
    os.environ['webdriver.chrome.driver'] = chromedriver_path
    options = webdriver.ChromeOptions()
    # options.add_argument("--user-data-dir="+r"C:\Users\c_yansun\AppData\Local\Google\Chrome\User Data")
    options.add_argument(
        "--user-data-dir=" + r"C:\Users\{}\AppData\Local\Google\Chrome\User Data".format(getpass.getuser()))
    if not browser:
        browser = webdriver.Chrome(chromedriver_path, chrome_options=options)
    browser.get(base_url)
    time.sleep(5)
    try:
        browser.find_element_by_xpath("//*[@id=\"frmLogin\"]/input[8]").click()
    except:
        printt("browser already logged")
    browser.implicitly_wait(5)
    if not sign:
        printt("First open chrome")
        printt("sleep(30); " * 5)
        time.sleep(5)
        browser.close()
        browser.quit()
        printt("close chrome; " * 5)
        return None, True
    printt(browser)
    printt(sign)
    return browser, sign

def OpenExcel(Excel_name):

    data = pd.read_excel(Excel_name,sheet_name="Project Tracking (12.16)New")
    head_list = list(data.columns)
    write_data = data.ix[:,["Account","Project","Chipset","TA Date","Camera Projects CCB \noverall Score","Schedule Note"]].values
    double_list = []
    for single_list in write_data:
        old_list = []
        for single in single_list:
            old_list.append(str(single))
        double_list.append(old_list)

    all_data_list = []
    for need in double_list:
        # 时间格式转换成'1/2/2018' '月/日/年 且月日中1-9前面不加0'
        need1 = ((need[3].split(" "))[0]).split("-")
        if need1[1][0] == "0":
            need1[1] = need1[1].replace("0", "")
        if need1[2][0] == "0":
            need1[2] = need1[2].replace("0", "")
        need[3] = "/".join((need1[1:3] + [need1[0]]))
        real_list = []
        for index in range(len(need)):
            if need[index] == "nan":
                need[index] = ""
            elif ".0" in need[index]:
                need[index] = eval((need[index].split('.'))[0])
            real_list.append(need[index])
        all_data_list.append(real_list)
    printt(all_data_list)
    return all_data_list


def CreateCeServices(browser,all_data_list):
    for data_list in all_data_list:
        Click(browser, '//*[@id="00B3A000009VOTB_listButtons"]/ul/li[1]/input')
        time.sleep(2)
        Selected(browser, '//*[@id="p3"]', '0123A000001O8qC')
        Click(browser, '//*[@id="bottomButtonRow"]/input[1]')
        time.sleep(2)
        str1 = "[" + data_list[0] + "]" + "[" + data_list[1] + "]" + "[" + data_list[2] + "]"
        SendKey(browser,'//*[@id="pg:frm:blk:DescriptionInformation:Subject"]',str1)
        SendKey(browser,'//*[@id="pg:frm:blk:KeyInformation:Project_Ownership_Note"]',data_list[-2])
        SendKey(browser,'//*[@id="pg:frm:blk:KeyInformation:Design_Review_Note"]',data_list[2])
        SendKey(browser,'//*[@id="pg:frm:blk:KeyInformation:Schedule_Note"]',data_list[-1])
        SendKey(browser,'//*[@id="pg:frm:blk:Stage3CameraFineTuning:Stage_3_End_Date"]',data_list[3])
        Selected(browser,'//*[@id="pg:frm:blk:title:Project_Stage"]','Stage 3 – Fine Tuning')
        SendKey(browser,'//*[@id="pg:frm:blk:DescriptionInformation:Description"]','Tuning')
        SendKey(browser,'//*[@id="pg:frm:blk:KeyInformation:Camera_Project_Status_Note"]','open')
        Click(browser,'//*[@id="pg:frm:blk:navBtns"]/input[2]')
        time.sleep(3)
        browser.get(base_url)



    time.sleep(100)

def main():
    all_data_list = OpenExcel(Excel_name)
    browser = None
    close_sign = True
    if not browser:
        for i in range(2):
            browser, close_sign = OpenChrome_(browser, close_sign)


    CreateCeServices(browser,all_data_list)

    time.sleep(100)


if __name__ == "__main__":
    main()
