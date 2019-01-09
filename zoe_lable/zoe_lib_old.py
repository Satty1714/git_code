#coding:utf-8
#python:3
import sys
import time
import os
import getpass
import traceback
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from selenium import webdriver
from selenium.webdriver.support.select import Select


base_url = "https://qualcomm-cdmatech-support.my.salesforce.com/a2A?fcf=00B3A000009VOTB"
# base_url = "https://qualcomm-cdmatech-support.my.salesforce.com/a2A?fcf=00B3A00000A9ajO"
# test = 'https://qualcomm-cdmatech-support.my.salesforce.com/a2A3A000000Hi8R'
# qruler_file = "China Camera CE Services mapping table_Project TA_2018SEP_2019_Part I.xlsx"

dirname_tool, _ = os.path.split(os.path.abspath(__file__))
chromedriver_path = "{}\\tools\\chromedriver\\chromedriver.exe".format(dirname_tool)

def get_tasklist():
    tasklist_v_fo_csv = os.popen('tasklist /v /fo csv').read()
    tasklist_v_fo_csv_list = tasklist_v_fo_csv.split("\n")
    temp_list = []
    for tasklist in tasklist_v_fo_csv_list:
        tasklist = tasklist.replace("[", "").replace("]", "").replace("\"", "")
        temp = tasklist.split(",")
        if temp != "" and temp[0] in ["chrome.exe", "python.exe","cmd.exe"]:
            temp_list.append(temp)
    return temp_list

def open_file():
    if os.path.exists(r"{}\xls_name.txt".format(dirname_tool)):
        with open(r"{}\xls_name.txt".format(dirname_tool), "r") as f:
            path = f.readline()
            qruler_file = os.path.split(path)[1]
        return qruler_file
    else:
        printt("excel not exists ERROR")


def SendEmail(from_, to_, title, email_content):
    sender = from_
    receivers = []
    receivers.append(to_)

    message = MIMEText(email_content, 'plain', 'utf-8')
    message['From'] = Header(from_, 'utf-8')
    message['To'] = Header(to_, 'utf-8')

    message['Subject'] = Header(title, 'utf-8')

    try:
        smtpObj = smtplib.SMTP("smtphost.qualcomm.com")
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("send ok")
    except smtplib.SMTPException:
        print("Error: send error")


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

# 单击操作 测试通过
def Click(browser, xpath, sign=True, count=0):
    while (sign):
        try:
            count += 0.5
            browser.find_element_by_xpath(xpath).click()
            sign = False
        except:
            sign = ErrorOrSleep(count)


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
    #用1的原因：可能第一行是标题行数据会有不同
    table_cols = table_rows[0].find_elements_by_tag_name(col_label)
    return len(table_rows),len(table_cols)


def OpenQRulerDB(qruler_file):
    qruler_db = pd.read_excel(qruler_file)
    name_data = pd.read_excel(qruler_file, sheet_name="Name Mapping")
    type_data = pd.read_excel(qruler_file, sheet_name="Sheet1")
    turing_data = pd.read_excel(qruler_file, sheet_name="Sheet2")
    # 表头信息
    head_list = list(qruler_db.columns)
    head_list = head_list[:1] + head_list[13:17] + head_list[24:34]

    # 取所有行的指定列【【】,【】】二维
    data = qruler_db.ix[:,
           ["CE Service Number", "Enter Date", "Exit Date", "Assignment (CE)", "Support Type", "Service #",
            "Basic tuning", "IQ fine tuning", "ISP/CPP", "PDAF\nTOF", "AWB\nColor", "AEC", "DualCam", "ADRC",
            "Misc"]].values
    data_ = name_data.ix[:, ["Assignment (CE) Name in Project Tracking Sheet", "Name in CE Service System"]].values
    sheet1_type = type_data.ix[:, ["Support Type1", "Support Type2"]].values
    sheet2_data = turing_data.ix[:, ["A", "B"]].values

    global name_dict
    global type_dict
    global turing_dict
    name_dict, type_dict, turing_dict = {}, {}, {}
    for sing_list in data_:
        if '@' in sing_list[1]:
            sing_list[1] = sing_list[1].replace('(','').replace(')','')
            sing_list[1] = sing_list[1].split(' ')
            sing_list[1] = (sing_list[1])[-1]

        name_dict[sing_list[0]] = sing_list[1]
    for type_ in sheet1_type:
        type_dict[type_[0]] = type_[1]
    for turing in sheet2_data:
        if turing[0] == "PDAFTOF":
            turing[0] = "PDAF\nTOF"
        elif turing[0] == "AWBColor":
            turing[0] = "AWB\nColor"
        turing_dict[turing[0]] = turing[1]

    # excel表中原始数据二维列表，每个格式转换成str
    double_list = []
    for sing_list in data:
        # 将number补成8位 demo：00000928
        sing_list[0] = "0" * (8 - int(len(str(sing_list[0])))) + str(sing_list[0])
        odd_list = []
        for single in sing_list:
            odd_list.append(str(single))
        double_list.append(odd_list)
    return double_list, head_list, name_dict, type_dict, turing_dict



def OpenChrome_(browser=None):
    os.environ['webdriver.chrome.driver'] = chromedriver_path
    options = webdriver.ChromeOptions()
    # options.add_argument("--user-data-dir="+r"C:\Users\c_yansun\AppData\Local\Google\Chrome\User Data")
    options.add_argument("--user-data-dir=" + r"C:\Users\{}\AppData\Local\Google\Chrome\User Data".format(getpass.getuser()))
    if not browser:
        browser = webdriver.Chrome(chromedriver_path, chrome_options=options)
    # new_case_report_url = 'https://qualcomm-cdmatech-support.my.salesforce.com/00O3A000009FfVy'
    browser.get(base_url)
    try:
        browser.find_element_by_xpath("//*[@id=\"frmLogin\"]/input[8]").click()
    except:
        printt("browser already logged")
    browser.implicitly_wait(5)
    return browser


def OpenChrome_1(browser,sign):
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
    time.sleep(3)
    #选择左下角的倒三角按钮
    # browser.find_element_by_xpath('//*[@id="00B3A000009VOTB_paginator_rpp_target"]/img').click()
    # # 选择一页100条
    # browser.find_element_by_xpath('//*[@id="00B3A000009VOTB_paginator_rpp"]/tbody/tr[4]').click()
    # time.sleep(3)
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
    printt(finally_list)
    printt(len(finally_list))
    return finally_list

#根据表与页面对应关系选择
def EditInfo(info_list,browser):

    def Select_all(browser, xpath, dict_, key):
        Selected(browser, xpath, dict_[key])
        time.sleep(2)

    browser.find_element_by_xpath('//*[@id="pg:frm:pb:pbs1:Tuning_Testing_Start_Date"]').send_keys(info_list[1])
    browser.find_element_by_xpath('//*[@id="pg:frm:pb:pbs1:Tuning_Testing_End_Date"]').send_keys(info_list[2])
    Selected(browser, '//*[@id="pg:frm:pb:pbs1:Tuning_Test_Record_Type"]', 'Camera Tuning Activity')

    if len(info_list) == 5:
        index_list = [-1,-2]
    else:
        index_list = [-2,-3]
        Select_all(browser, '//*[@id="pg:frm:pb:pbs1:Tuning_Record_Category"]', turing_dict, info_list[-1])
    Select_all(browser, '//*[@id="pg:frm:pb:pbs1:Site_Lab"]', type_dict, info_list[index_list[0]])
    time.sleep(1)

    if '@' not in name_dict[info_list[index_list[1]]]:
        browser.find_element_by_xpath('//*[@id="pg:frm:pb:pbs1:Engineer_Name"]').send_keys(name_dict[info_list[index_list[1]]])
    else:
        now_handle = browser.current_window_handle
        Click(browser, '//*[@id="pg:frm:pb:pbs1:Engineer_Name_lkwgt"]/img')
        all_handles = browser.window_handles
        for handle in all_handles:
            if now_handle != handle:
                browser.switch_to_window(handle)
                browser.switch_to.frame('searchFrame')
                browser.find_element_by_xpath('//*[@id="lksrch"]').send_keys(info_list[index_list[1]])
                Click(browser, '//*[@id="theForm"]/div/div[2]/input[2]')
                time.sleep(1)
                browser.switch_to.default_content()#切换到之前的frame
                browser.switch_to.frame('resultsFrame')
                try:
                    rows, cols = GetTableRowsAndCols_xpath(browser,
                                                           '//*[@id="new"]/div/div[3]/div/div[2]/table/tbody', "tr",
                                                           'th')
                except:
                    exit()
                printt(rows)
                owner_base_xpath = '//*[@id="new"]/div/div[3]/div/div[2]/table/tbody/tr'
                for row in range(2, rows + 1):
                    text = (GetText_Xpath(browser, '{}[{}]/td[2]'.format(owner_base_xpath, row)))
                    if text == name_dict[info_list[index_list[1]]]:
                        Click(browser, '{}[{}]/th/a'.format(owner_base_xpath, row))
                        time.sleep(1)
                        break
        browser.switch_to_window(now_handle)
    Click(browser, '//*[@id="pg:frm:pb:navBtns"]/input[2]')  # cancel
    time.sleep(2)
    #Click(browser, '//*[@id="pg:frm:pb:navBtns:btnSave"]')  # save


#取链接进入编辑页面
def SelectInfo(ce_number_dict,finally_list,browser):
    '''
    :param ce_number_dict:
    :param finally_list:
    :param browser:
    :return:
    '''
    if os.path.exists('all.txt') == False:
        with open("all.txt",'w') as f:
            for info_list in finally_list:
                if len(info_list) != 3:
                    f.write("{}\n".format(info_list))
        with open('error.txt','w') as fa:
            for info_list in finally_list:
                if len(info_list) == 3:
                    fa.write("{}\n".format(info_list))

        with open("all.txt",'r') as fb:
            lines = fb.readlines()
            for line in lines:
                info = eval(line)
                for key,values in ce_number_dict.items():
                    if info[0] == key:
                        browser.get(values)
                        time.sleep(5)
                        currents_url = browser.current_url
                        printt(currents_url)
                        val = (values.split('/'))[-1]
                        Click(browser,
                              '//*[@id="massActionForm_{}_00N3A00000CBlJl"]/div[1]/table/tbody/tr/td[2]/input'.format(
                                  val))
                        time.sleep(3)
                        EditInfo(info, browser)
                        with open("save.txt", 'a') as fc:
                            fc.write("{}".format(line))
                        time.sleep(3)

        os.remove("all.txt")
        os.remove("save.txt")
        time.sleep(5)

    else:
        with open("all.txt","r") as f:
            data1 = f.readlines()
            num1 = len(data1)
        if os.path.exists("save.txt"):
            with open("save.txt",'r') as f:
                data2 = f.readlines()
                num2 = len(data2)

            for num in range(num2,num1):
                for keys, vals in ce_number_dict.items():
                    data_info = eval(data1[num])
                    if data_info[0] == keys:
                        browser.get(vals)
                        time.sleep(5)
                        currents_url = browser.current_url
                        printt(currents_url)
                        case_id = (vals.split('/'))[-1]
                        Click(browser,
                              '//*[@id="massActionForm_{}_00N3A00000CBlJl"]/div[1]/table/tbody/tr/td[2]/input'.format(
                                  case_id))
                        time.sleep(3)
                        EditInfo(data_info, browser)
                        with open("save.txt", "a") as f1:
                            f1.write("{}".format(data1[num]))
                        time.sleep(3)
        else:
            with open("all.txt", 'r') as ff:
                lines = ff.readlines()
                for line in lines:
                    info = eval(line)
                    for key, values in ce_number_dict.items():
                        if info[0] == key:
                            browser.get(values)
                            time.sleep(5)
                            currents_url = browser.current_url
                            printt(currents_url)
                            val = (values.split('/'))[-1]
                            Click(browser,
                                  '//*[@id="massActionForm_{}_00N3A00000CBlJl"]/div[1]/table/tbody/tr/td[2]/input'.format(
                                      val))
                            time.sleep(3)
                            EditInfo(info, browser)
                            with open("save.txt", 'a') as fm:
                                fm.write("{}".format(line))
                            time.sleep(3)

        os.remove("all.txt")
        os.remove("save.txt")
        time.sleep(3)


def main():
    temp_list = get_tasklist()
    # browser = None
    # close_sign = True
    # if not browser:
    #     for i in range(2):
    #         browser, close_sign = OpenChrome_(browser, close_sign)
    browser = OpenChrome_()
    qruler_file = open_file()
    data_list, head_list, name_dict, type_dict, turing_dict = OpenQRulerDB(qruler_file)
    ce_number_dict = GetCameraServices(browser)
    finally_list = ContrastInfo(ce_number_dict,data_list,head_list)
    SelectInfo(ce_number_dict,finally_list,browser)
    browser.close()
    browser.quit()

    # if os.path.exists('error.txt'):
    #     with open('error.txt','r') as f:
    #         line = f.readlines()
    #     lines = "\n".join(line)
    #     SendEmail("hsiaochi@qti.qualcomm.com","hsiaochi@qti.qualcomm.com","error data",lines)
    #     os.remove('error.txt')

    for temp in temp_list:
        if "zoe_start.py" in temp:
            cmd = 'taskkill /pid {} -t -f'.format(int(temp[1]))
            os.system(cmd)
        if "zoe_lib.py" in temp:
            cmd = 'taskkill /pid {} -t -f'.format(int(temp[1]))
            os.system(cmd)
        if "cmd" in temp[0]:
            cmd = 'taskkill /pid {} -t -f'.format(int(temp[1]))
            os.system(cmd)

        
if __name__ == "__main__":
    main()
