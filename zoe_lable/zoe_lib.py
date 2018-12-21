#coding:utf-8
#python:3
import sys
import time
import os
import getpass
import traceback
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.select import Select


base_url = "https://qualcomm-cdmatech-support.my.salesforce.com/a2A?fcf=00B3A000009VOTB"
# base_url = "https://qualcomm-cdmatech-support.my.salesforce.com/00O3A000009FfVy"
qruler_file = "China Camera CE Services mapping table_Project TA_2018SEP_2019_Part I"
# qruler_file = "Data.xlsx"
dirname_tool, _ = os.path.split(os.path.abspath(__file__))
chromedriver_path = "{}\\tools\\chromedriver\\chromedriver.exe".format(dirname_tool)
cookies_path = r"C:\Users\{}\Downloads".format(getpass.getuser())

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
        print("[{}] {} {} {} {}".format(py_file, GetTime(), func_name, lines, everything))


def ErrorOrSleep(count, print_info="*" * 10, count_max=10):
    if count >= count_max:
        traceback.print_exc()
        return False
    else:
        print(print_info)
        time.sleep(0.5)
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


def OpenQRulerDB(qruler_file):
    dirname_temp = r"C:\workpy3_code\zoe_lable"
    path_t = "{}\\{}".format(dirname_temp, qruler_file)
    qruler_db = (pd.read_excel(path_t))

    #取所有行的指定列【【】,【】】二维
    data = qruler_db.ix[:,["CE Service Number","Enter Date","Exit Date","Assignment (CE)","Support Type","Service #",
                           "Basic tuning","IQ fine tuning","ISP/CPP","PDAF\nTOF","AWB\nColor","AEC","DualCam","ADRC","Misc"]].values
    double_list = []
    for sing_list in data:
        sing_list[0] = "0" * (8 - int(len(str(sing_list[0])))) + str(sing_list[0])
        odd_list = []
        for single in sing_list:
            odd_list.append(str(single))
        double_list.append(odd_list)
    return double_list


def OpenChrome_(browser,sign):
    os.environ['webdriver.chrome.driver'] = chromedriver_path
    options = webdriver.ChromeOptions()
    # options.add_argument("--user-data-dir="+r"C:\Users\c_yansun\AppData\Local\Google\Chrome\User Data")
    options.add_argument("--user-data-dir=" + r"C:\Users\{}\AppData\Local\Google\Chrome\User Data".format(getpass.getuser()))
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
        printt("close chrome; "*5)
        return None,True
    printt(browser)
    printt(sign)
    return browser,sign


def GetCameraServices(browser):
    Select(browser.find_element_by_xpath('//*[@id="00B3A000009VOTB_listSelect"]')).select_by_value('00B3A000009VOTB')
    time.sleep(10)
    browser.find_element_by_xpath('//*[@id="00B3A000009VOTB_paginator_rpp_target"]/img').click()
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="00B3A000009VOTB_paginator_rpp"]/tbody/tr[3]').click()
    time.sleep(5)

    ce_number_dict = {}
    while True:
        num_str = browser.find_element_by_xpath('//*[@id="00B3A000009VOTB_paginator_rpp_target"]').text
        num_list = num_str.split(" ")
        rows = num_list[0].split('-')
        row = int(rows[1]) - int(rows[0]) + 1
        for num in range(1,row+1):
            text = browser.find_element_by_xpath('//*[@id="ext-gen11"]/div[{}]/table/tbody/tr/td[4]/div/a/span'.format(num)).text
            href = browser.find_element_by_xpath('//*[@id="ext-gen11"]/div[{}]/table/tbody/tr/td[4]/div/a'.format(num)).get_attribute('href')
            ce_number_dict[text] = href
        try:
            browser.find_element_by_xpath('//*[@id="00B3A000009VOTB_bottomNav"]/div[1]/span[2]/span[3]/a').click()
        except:
            break

        time.sleep(10)

    printt(ce_number_dict)
    printt(len(ce_number_dict))
    return ce_number_dict


#对比信息
def ContrastInfo(ce_number_dict,data_list):
    '''

    :param ce_number_dict: 页面中所有的number和link
    :param data_list: excel中所有数据 是一个二维列表
    :return:
    '''

    #页面中存在的数和excel中存在且相同的数
    need_list = []
    for excel_data in data_list:
        for key in ce_number_dict.keys():
            if key == excel_data[0]:
                need_list.append(excel_data)

    #最终转换为真正想要格式的数据
    finally_list = []
    for need in need_list:
        need[1] = (need[1].split(" "))[0]
        need[2] = (need[2].split(" "))[0]
        real_list = []
        for index in range(len(need)):
            if need[index] == "nan":
                need[index] = int("-1")
            elif ".0" in need[index]:
                need[index] = eval((need[index].split('.'))[0])
            real_list.append(need[index])
        finally_list.append(real_list)



def main():
    browser = None
    close_sign = True
    if not browser:
        for i in range(2):
            browser, close_sign = OpenChrome_(browser, close_sign)

    ce_number_dict = GetCameraServices(browser)
    data_list = OpenQRulerDB(qruler_file)
    ContrastInfo(ce_number_dict,data_list)


        
if __name__ == "__main__":
    main()
    os.system("pause")