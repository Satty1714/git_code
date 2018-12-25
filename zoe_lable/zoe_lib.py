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
test = 'https://qualcomm-cdmatech-support.my.salesforce.com/a2A3A000000Hi8R'
# base_url = "https://qualcomm-cdmatech-support.my.salesforce.com/00O3A000009FfVy"
qruler_file = "China Camera CE Services mapping table_Project TA_2018SEP_2019_Part I.xlsx"
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


def OpenQRulerDB(qruler_file):
    dirname_temp = r"C:\workpy3_code\zoe_lable"
    path_t = "{}\\{}".format(dirname_temp, qruler_file)
    qruler_db = (pd.read_excel(path_t))
    #表头信息
    head_list = list(qruler_db.columns)
    head_list = head_list[:1] + head_list[13:17] + head_list[24:34]

    #取所有行的指定列【【】,【】】二维
    data = qruler_db.ix[:,["CE Service Number","Enter Date","Exit Date","Assignment (CE)","Support Type","Service #",
                           "Basic tuning","IQ fine tuning","ISP/CPP","PDAF\nTOF","AWB\nColor","AEC","DualCam","ADRC","Misc"]].values
    #excel表中原始数据二维列表，每个格式转换成str
    double_list = []
    for sing_list in data:
        #将number补成8位 demo：00000928
        sing_list[0] = "0" * (8 - int(len(str(sing_list[0])))) + str(sing_list[0])
        odd_list = []
        for single in sing_list:
            odd_list.append(str(single))
        double_list.append(odd_list)
    return double_list,head_list


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

#获取所有number和link存放到字典里
def GetCameraServices(browser):
    #进来首先选择 Camera Service Lab
    Select(browser.find_element_by_xpath('//*[@id="00B3A000009VOTB_listSelect"]')).select_by_value('00B3A000009VOTB')
    time.sleep(5)
    #选择左下角的倒三角按钮
    browser.find_element_by_xpath('//*[@id="00B3A000009VOTB_paginator_rpp_target"]/img').click()
    time.sleep(2)
    # 选择一页100条
    browser.find_element_by_xpath('//*[@id="00B3A000009VOTB_paginator_rpp"]/tbody/tr[4]').click()
    time.sleep(5)
    #{'number':link}
    ce_number_dict = {}
    while True:
        # '1-100 of 228'
        num_str = browser.find_element_by_xpath('//*[@id="00B3A000009VOTB_paginator_rpp_target"]').text
        num_list = num_str.split(" ")
        rows = num_list[0].split('-')
        row = int(rows[1]) - int(rows[0]) + 1
        for num in range(1,row+1):
            text = browser.find_element_by_xpath('//*[@id="ext-gen11"]/div[{}]/table/tbody/tr/td[4]/div/a/span'.format(num)).text
            href = browser.find_element_by_xpath('//*[@id="ext-gen11"]/div[{}]/table/tbody/tr/td[4]/div/a'.format(num)).get_attribute('href')
            ce_number_dict[text] = href
        try:
            #next按钮
            browser.find_element_by_xpath('//*[@id="00B3A000009VOTB_bottomNav"]/div[1]/span[2]/span[3]/a').click()
        except:
            break

        time.sleep(5)

    printt(ce_number_dict)
    printt(len(ce_number_dict))
    return ce_number_dict


#对比信息
def ContrastInfo(ce_number_dict,data_list,head_list):
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

        # 转换格式
    all_list = []
    for need in need_list:
        #时间格式转换成'1/2/2018' '月/日/年 且月日中1-9前面不加0'
        need1 = ((need[1].split(" "))[0]).split("-")
        need2 = ((need[2].split(" "))[0]).split("-")
        if need1[1][0] == "0":
            need1[1] = need1[1].replace("0", "")
        if need1[2][0] == "0":
            need1[2] = need1[2].replace("0", "")
        if need2[1][0] == "0":
            need2[1] = need2[1].replace("0", "")
        if need2[2][0] == "0":
            need2[2] = need2[2].replace("0", "")

        need[1] = "/".join((need1[1:3] + [need1[0]]))
        need[2] = "/".join((need2[1:3] + [need2[0]]))
        real_list = []
        for index in range(len(need)):
            if need[index] == "nan":
                need[index] = int("-1")
            elif ".0" in need[index]:
                need[index] = eval((need[index].split('.'))[0])
            real_list.append(need[index])
        all_list.append(real_list)
    #
    # print(all_list)
    # all_list = [['00000928', '2018/12/15', '2019/02/13', 'Guangjun He', 'DRI', -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    #             ['00000944', '2018/07/02', '2018/10/15', 'Mingchen Gao', 'DRI', 2, -1, 1, 1, -1, -1, -1, -1, -1, -1]]

    # 将需要填写几次的数字转换成对应的表头字符串
    new_list = []
    for new_data in all_list:
        if new_data[5] == -1 or new_data[5] == 0:
            new_list.append(new_data)
        else:
            for index in range(6, len(head_list)):
                if index != 5 and type(new_data[index]) == int and new_data[index] > 0:
                    for i in range(new_data[index]):
                        new_data1 = new_data[:]
                        new_data1[index] = head_list[index]
                        new_list.append(new_data1)

    # 最终需要填写的数据
    finally_list = []
    for new in new_list:
        x1 = []
        for index_x in range(0, len(new)):
            if type(new[index_x]) == str:
                x1.append(new[index_x])
        finally_list.append(x1)
    return finally_list

#根据表与页面对应关系选择
def EditInfo(info_list,browser,current_urls):
    if len(info_list) == 5:
        if info_list[-1] == "DRI":
            Selected(browser,'//*[@id="pg:frm:pb:pbs1:Site_Lab"]','Debug Lab')
        elif info_list[-1] == "ServiceLab-TS":
            Selected(browser,'//*[@id="pg:frm:pb:pbs1:Site_Lab"]','TS Lab')
        else:
            Selected(browser,'//*[@id="pg:frm:pb:pbs1:Site_Lab"]','Service Lab')
        browser.find_element_by_xpath('//*[@id="pg:frm:pb:pbs1:Tuning_Testing_Start_Date"]').send_keys(info_list[1])
        browser.find_element_by_xpath('//*[@id="pg:frm:pb:pbs1:Tuning_Testing_End_Date"]').send_keys(info_list[2])
        Selected(browser,'//*[@id="pg:frm:pb:pbs1:Tuning_Test_Record_Type"]','Camera Tuning Activity')
        time.sleep(5)
        if info_list[-2] == "Gary Ge":
            browser.find_element_by_xpath('//*[@id="pg:frm:pb:pbs1:Engineer_Name"]').send_keys("Peiguang Ge")
        elif info_list[-2] == "Jun Yang":
            browser.find_element_by_xpath('//*[@id="pg:frm:pb:pbs1:Engineer_Name"]').send_keys("Jun Yang")
            Click(browser, '//*[@id="pg:frm:pb:navBtns:btnSave"]')  # save

            time.sleep(3)
            Selected(browser, '//*[@id="pg:frm:pb:pbs1:Engineer_Name_lkid"]', '0053A00000CaJ8x')
            time.sleep(2)
        elif info_list[-2] == "Yang Yang":
            browser.find_element_by_xpath('//*[@id="pg:frm:pb:pbs1:Engineer_Name"]').send_keys("Yang Yang")
            Click(browser, '//*[@id="pg:frm:pb:navBtns:btnSave"]')  # save

            time.sleep(3)
            Selected(browser, '//*[@id="pg:frm:pb:pbs1:Engineer_Name_lkid"]', '0053000000BiNlL')
            time.sleep(2)
        else:
            browser.find_element_by_xpath('//*[@id="pg:frm:pb:pbs1:Engineer_Name"]').send_keys(info_list[-2])

        Click(browser, '//*[@id="pg:frm:pb:navBtns"]/input[2]')  # cancel
        # Click(browser, '//*[@id="pg:frm:pb:navBtns:btnSave"]')  # save


    else:
        if info_list[-2] == "DRI":
            Selected(browser, '//*[@id="pg:frm:pb:pbs1:Site_Lab"]', 'Debug Lab')
        elif info_list[-2] == "ServiceLab-TS":
            Selected(browser, '//*[@id="pg:frm:pb:pbs1:Site_Lab"]', 'TS Lab')
        else:
            Selected(browser, '//*[@id="pg:frm:pb:pbs1:Site_Lab"]', 'Service Lab')
        browser.find_element_by_xpath('//*[@id="pg:frm:pb:pbs1:Tuning_Testing_Start_Date"]').send_keys(info_list[1])
        browser.find_element_by_xpath('//*[@id="pg:frm:pb:pbs1:Tuning_Testing_End_Date"]').send_keys(info_list[2])
        Selected(browser, '//*[@id="pg:frm:pb:pbs1:Tuning_Test_Record_Type"]', 'Camera Tuning Activity')
        if info_list[-1] == "Basic tuning":
            Selected(browser,'//*[@id="pg:frm:pb:pbs1:Tuning_Record_Category"]','Initial Tuning')
        elif info_list[-1] == "IQ fine tuning":
            Selected(browser,'//*[@id="pg:frm:pb:pbs1:Tuning_Record_Category"]','Other ISP/CPP Block Tuning')
        elif info_list[-1] == "ISP/CPP":
            Selected(browser, '//*[@id="pg:frm:pb:pbs1:Tuning_Record_Category"]','Noise/Sharpness Tuning')
        elif info_list[-1] == "PDAF\nTOF":
            Selected(browser, '//*[@id="pg:frm:pb:pbs1:Tuning_Record_Category"]','AF Tuning')
        elif info_list[-1] == "AWB\nColor":
            Selected(browser, '//*[@id="pg:frm:pb:pbs1:Tuning_Record_Category"]','AWB Tuning')
        elif info_list[-1] == "AEC":
            Selected(browser, '//*[@id="pg:frm:pb:pbs1:Tuning_Record_Category"]','AE Tuning')
        elif info_list[-1] == "DualCam":
            Selected(browser, '//*[@id="pg:frm:pb:pbs1:Tuning_Record_Category"]','Other Feature Tuning')
        elif info_list[-1] == "ADRC":
            Selected(browser, '//*[@id="pg:frm:pb:pbs1:Tuning_Record_Category"]','Contrast and Dynamic Range')
        else:
            Selected(browser, '//*[@id="pg:frm:pb:pbs1:Tuning_Record_Category"]','Miscellaneous Tuning')
        time.sleep(5)

        if info_list[-3] == "Gary Ge":
            browser.find_element_by_xpath('//*[@id="pg:frm:pb:pbs1:Engineer_Name"]').send_keys("Peiguang Ge")
            time.sleep(2)
        elif info_list[-3] == "Jun Yang":
            browser.find_element_by_xpath('//*[@id="pg:frm:pb:pbs1:Engineer_Name"]').send_keys("Jun Yang")
            Click(browser, '//*[@id="pg:frm:pb:navBtns:btnSave"]')  # save

            time.sleep(3)
            Selected(browser, '//*[@id="pg:frm:pb:pbs1:Engineer_Name_lkid"]', '0053A00000CaJ8x')
            time.sleep(2)
        elif info_list[-3] == "Yang Yang":
            browser.find_element_by_xpath('//*[@id="pg:frm:pb:pbs1:Engineer_Name"]').send_keys("Yang Yang")
            Click(browser, '//*[@id="pg:frm:pb:navBtns:btnSave"]')  # save

            time.sleep(3)
            Selected(browser, '//*[@id="pg:frm:pb:pbs1:Engineer_Name_lkid"]', '0053000000BiNlL')
            time.sleep(2)
        else:
            browser.find_element_by_xpath('//*[@id="pg:frm:pb:pbs1:Engineer_Name"]').send_keys(info_list[-3])

        Click(browser, '//*[@id="pg:frm:pb:navBtns"]/input[2]') #cancel
        # Click(browser, '//*[@id="pg:frm:pb:navBtns:btnSave"]')  # save


#取链接进入编辑
def SelectInfo(ce_number_dict,finally_list,browser):
    '''
    :param ce_number_dict:
    :param finally_list:
    :param browser:
    :return:
    '''
    for info_list in finally_list:
        for key,values in ce_number_dict.items():
            if info_list[0] == key:
                browser.get(values)
                time.sleep(5)
                current_urls = browser.current_url
                printt(current_urls)
                val = (values.split("/"))[-1]
                Click(browser,'//*[@id="massActionForm_{}_00N3A00000CBlJl"]/div[1]/table/tbody/tr/td[2]/input'.format(val))
                time.sleep(5)
                EditInfo(info_list,browser,current_urls)
                time.sleep(2)


def main():
    browser = None
    close_sign = True
    if not browser:
        for i in range(2):
            browser, close_sign = OpenChrome_(browser, close_sign)

    ce_number_dict = GetCameraServices(browser)
    data_list,head_list = OpenQRulerDB(qruler_file)
    finally_list = ContrastInfo(ce_number_dict,data_list,head_list)
    SelectInfo(ce_number_dict,finally_list,browser)

        
if __name__ == "__main__":
    main()
    os.system("pause")