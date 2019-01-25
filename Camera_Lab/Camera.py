#coding:utf-8
#python:3
import sys
import time
import os
import re
import getpass
import traceback
import pandas as pd
import smtplib
import datetime
from email.mime.text import MIMEText
from email.header import Header
from selenium import webdriver
from selenium.webdriver.support.select import Select


base_url = "https://qualcomm-cdmatech-support.my.salesforce.com/a2A?fcf=00B3A000009VOTB"
# base_url = "https://qualcomm-cdmatech-support.my.salesforce.com/a2A?fcf=00B3A00000A9ajO"
case_id_rule = re.compile("fcf=(.+)")
group_ = case_id_rule.findall(base_url)
base_case_id = group_[0]

dirname_tool, _ = os.path.split(os.path.abspath(__file__))
chromedriver_path = "{}\\tools\\chromedriver\\chromedriver.exe".format(dirname_tool)
ALL_TXT = r"{}\all.txt".format(dirname_tool)
SAVE_TXT = r"{}\save.txt".format(dirname_tool)
ERROR_TXT = r"{}\error.txt".format(dirname_tool)

def get_tasklist():
    tasklist_v_fo_csv = os.popen('tasklist /v /fo csv').read()
    tasklist_v_fo_csv_list = tasklist_v_fo_csv.split("\n")
    temp_list = []
    for tasklist in tasklist_v_fo_csv_list:
        tasklist = tasklist.replace("[", "").replace("]", "").replace("\"", "")
        temp = tasklist.split(",")
        if temp != "" and temp[0] in ["chrome.exe", "python.exe",'cmd.exe']:
            temp_list.append(temp)
    return temp_list

def open_file():
    if os.path.exists(r"{}\xls_name.txt".format(dirname_tool)):
        with open(r"{}\xls_name.txt".format(dirname_tool), "r") as f:
            path = f.readline()
        return path
    else:
        printt("excel not exists ERROR")
        exit()

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
    name_list = name_dict.keys()
    for type_ in sheet1_type:
        type_dict[type_[0]] = type_[1]
    type_list = type_dict.keys()
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
        for i in range(5,15):
            sing_list[i] = float(sing_list[i])
        odd_list = []
        for single in sing_list:
            odd_list.append(str(single))
        double_list.append(odd_list)

    temp_list = []
    for info_list in double_list:
        if (info_list[3] in name_list) and (info_list[4] in type_list):
            temp_list.append(info_list)
        else:
            with open(ERROR_TXT,'a') as f:
                f.write("Assignment Error or Support Type Error or data defect{}\n".format(info_list))

    return temp_list, head_list, name_dict, type_dict, turing_dict

def OpenChrome_(browser=None):
    os.environ['webdriver.chrome.driver'] = chromedriver_path
    options = webdriver.ChromeOptions()
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
    return browser
    
#获取所有number和link存放到字典里
def GetCameraServices(browser):
    #进来首先选择 Camera Service Lab
    Select(browser.find_element_by_xpath('//*[@id="{}_listSelect"]'.format(base_case_id))).select_by_value(base_case_id)
    time.sleep(3)
    #{'number':link}
    ce_number_dict = {}
    while True:
        # '1-100 of 228'
        #获取每一页的num和对应的href
        num_str = browser.find_element_by_xpath('//*[@id="{}_paginator_rpp_target"]'.format(base_case_id)).text
        num_list = num_str.split(" ")
        rows = num_list[0].split('-')
        row = int(rows[1]) - int(rows[0]) + 1
        for num in range(1,row+1):
            text = browser.find_element_by_xpath('//*[@id="ext-gen11"]/div[{}]/table/tbody/tr/td[4]/div/a/span'.format(num)).text
            href = browser.find_element_by_xpath('//*[@id="ext-gen11"]/div[{}]/table/tbody/tr/td[4]/div/a'.format(num)).get_attribute('href')
            ce_number_dict[text] = href
        try:
            #next按钮
            browser.find_element_by_xpath('//*[@id="{}_bottomNav"]/div[1]/span[2]/span[3]/a'.format(base_case_id)).click()
        except:
            break
        time.sleep(3)
    # printt(ce_number_dict)
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
        if excel_data[0] in ce_number_dict.keys():
            need_list.append(excel_data)
        else:
            with open(ERROR_TXT, 'a') as fn:
                fn.write("CE Service Number write ERROR {}\n".format(excel_data))

    # need_list = data_list[:]
    # 检查时间是否有误
    first_all_list = need_list[:]
    for need in need_list:
        for i in range(1,3):
            need_s = ((need[i].split(" "))[0])
            rule1 = re.compile("(\d{4})-0?(\d{1,2})-0?(\d{1,2})")
            line = rule1.findall(need_s)
            if not line:
               with open(ERROR_TXT,'a') as f:
                   f.write("Date Form Error{}\n".format(need))
                   first_all_list.remove(need)

    second_all__list = first_all_list[:]
    for need_date in first_all_list:
        need1 = (need_date[1].split(" ")[0])
        need2 = (need_date[2].split(" ")[0])
        date1 = time.strptime(need1, '%Y-%m-%d')
        date2 = time.strptime(need2, '%Y-%m-%d')
        date1 = datetime.datetime(date1[0], date1[1], date1[2])
        date2 = datetime.datetime(date2[0], date2[1], date2[2])
        TIME = (date2 - date1).days
        if TIME < 1:
            with open(ERROR_TXT, 'a') as fm:
                fm.write("Enter Date or Exit Date ERROR{}\n".format(need_date))
                second_all__list.remove(need_date)

    all_list = []
    for second_data in second_all__list:
        # 时间格式转换成'1/2/2018' '月/日/年 且月日中1-9前面不加0'
        for i in range(1,3):
            data = ((second_data[i].split(" "))[0])
            rules = re.compile("(\d{4})-0?(\d{1,2})-0?(\d{1,2})")
            lines = rules.findall(data)
            list1 = list(tuple(lines[0]))
            list2 = list1[1:]
            list2.append(list1[0])
            second_data[i] = "/".join(list2)
        real_list = []
        for index in range(len(second_data)):
            if second_data[index] == "nan":
                second_data[index] = int("0")
            elif ".0" in second_data[index]:
                second_data[index] = eval((second_data[index].split('.'))[0])
            real_list.append(second_data[index])
        all_list.append(real_list)

    mid_list = all_list[:]
    for total_list in all_list:
        number = 0
        for index_n in range(6, len(head_list)):
            number += total_list[index_n]
        if total_list[5] != number:
            with open(ERROR_TXT, 'a') as ft:
                ft.write("Service Number Error{}\n".format(total_list))
            mid_list.remove(total_list)

    # 将需要填写几次的数字转换成对应的表头字符串
    new_list = []
    for new_data in mid_list:
        if new_data[5] == 0:
            new_list.append(new_data)
        else:
            for index in range(6, len(head_list)):
                if type(new_data[index]) == int and new_data[index] > 0:
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
    # printt(finally_list)
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
    # Click(browser, '//*[@id="pg:frm:pb:navBtns:btnSave"]')  # save
    time.sleep(2)

#取链接进入编辑页面
def SelectInfo(ce_number_dict,finally_dict,browser):
    #取网页中CE Services Activities
    def GetCameraComments(browser,link):
        link_id = (link.split('/')[-1])
        while True:
            try:
                browser.find_element_by_xpath('//*[@id="{}_00N3A00000CBlJl_body"]/div/a[1]'.format(link_id)).click()
                time.sleep(2)
                # Click(browser,'//*[@id="{}_00N3A00000CBlJl_body"]/div/a[1]'.format(link_id))
            except:
                break
        table_xpath = "/html/body/div/div[2]/table/tbody/tr/td[2]/div[5]/div[1]/div/form/div[2]/table"
        try:
            rows, cols = GetTableRowsAndCols_xpath(browser, table_xpath, "tr", 'th')
        except:
            return []
        printt(rows)
        #二维列表，每一个一维列表就是CE Services Activities中的每一条数据 demo：[00000928,Weitao Lin,Debug Lab,4/2/2017,
                                                                    # 4/15/2017,Camera Tuning Activity,AF Tuning]
        comments_list = []
        for row in range(2, rows + 1):
            temp_ = []
            #取ce servers number
            xpath_number = "/html/body/div[1]/div[2]/table/tbody/tr/td[2]/div[4]/div[2]/div[2]/table/tbody/tr[3]/td[2]"
            case_number = GetText_Xpath(browser, xpath_number)
            temp_.append(case_number)
            for i in range(2, 8):
                xpath_tc = "/html/body/div/div[2]/table/tbody/tr/td[2]/div[5]/div[1]/div/form/div[2]/table/tbody/tr[{}]/td[{}]".format(row, i)
                temp = GetText_Xpath(browser, xpath_tc)
                temp_.append(temp)
            comments_list.append(temp_)
        #一维列表['00000928;Weitao Lin;Debug Lab;4/2/2017;4/15/2017,Camera Tuning Activity,AF Tuning',...]
        new_comments_list = []
        new_type_dict = {v: k for k, v in type_dict.items()}
        new_turing_dict = {val: keys for keys, val in turing_dict.items()}
        new_name_dict = {y:x for x,y in name_dict.items()}
        for com in comments_list:
            for sing in new_name_dict.keys():
                if com[1] == sing:
                    com[1] = new_name_dict[com[1]]
                else:
                    com[1] = com[1]

            if com[-1] == ' ':
                com = com[:1] + com[3:5] + com[1:3]
                com[-1] = new_type_dict[com[-1]]
            else:
                com = com[:1] + com[3:5] + com[1:3] + com[-1:]
                com[-2] = new_type_dict[com[-2]]
                com[-1] = new_turing_dict[com[-1]]
            new_comments_list.append(";".join(com))
        #new_comments_dict = {'00000928;Weitao Lin;Debug Lab;4/2/2017;4/15/2017':1,'00000928;Weitao Lin;Debug Lab;5/2/2017;6/15/2017':2,.....}
        new_comments_dict = {}
        for comm in new_comments_list:
            if comm in new_comments_dict.keys():
                new_comments_dict[comm] += 1
            else:
                new_comments_dict[comm] = 1
        return new_comments_dict

    for key, value in finally_dict.items():
        browser.get(ce_number_dict[key])
        comments_dict = GetCameraComments(browser,ce_number_dict[key])
        need_op_info_list = []
        new_need_op_info_list = []
        if comments_dict:
            #excel表中的数据
            new_value_dict = {}
            for com1 in value:
                #com_str = '00000928;4/2/2017;4/15/2017;Weitao Lin;Debug Lab'
                com_str = ";".join(com1)
                if com_str in new_value_dict.keys():
                    new_value_dict[com_str] += 1
                else:
                    new_value_dict[com_str] = 1

            for key_ in new_value_dict.keys():
                sign = True
                for key_com in comments_dict.keys():
                    if key_ == key_com:
                        int_value = abs(new_value_dict[key_com] - comments_dict[key_com])
                        for i in range(int_value):
                            need_op_info_list.append(key_com)
                        sign = False
                if sign:
                    for i in range(new_value_dict[key_]):
                        need_op_info_list.append(key_)
        else:
            new_need_op_info_list = value[:]

        if len(need_op_info_list) > 0:
            for op_info in need_op_info_list:
                end_list = op_info.split(";")
                new_need_op_info_list.append(end_list)

        printt(new_need_op_info_list)
        time.sleep(3)
        if len(new_need_op_info_list) > 0:
            currents_url = browser.current_url
            printt(currents_url)
            val = (ce_number_dict[key].split('/'))[-1]
            for op_info in new_need_op_info_list:
                Click(browser,
                      '//*[@id="massActionForm_{}_00N3A00000CBlJl"]/div[1]/table/tbody/tr/td[2]/input'.format(
                          val))
                time.sleep(3)
                EditInfo(op_info, browser)

            time.sleep(3)


def list_to_dict(temp_list):
    temp_dict = {}
    for line in temp_list:
        if line[0] not in temp_dict.keys():
            temp_dict[line[0]] = [line]
        else:
            temp_dict[line[0]] += [line]
    return temp_dict

def main():
    temp_list = get_tasklist()
    qruler_file = open_file()
    data_list, head_list, name_dict, type_dict, turing_dict = OpenQRulerDB(qruler_file)

    # browser = None
    # close_sign = True
    # if not browser:
    #     for i in range(1):
    browser = OpenChrome_()
    ce_number_dict = GetCameraServices(browser)
    finally_list = ContrastInfo(ce_number_dict,data_list,head_list)
    finally_dict = list_to_dict(finally_list)
    SelectInfo(ce_number_dict, finally_dict, browser)
    browser.close()
    browser.quit()
    # if os.path.exists(ERROR_TXT):
    #     with open(ERROR_TXT,'r') as f:
    #         line = f.readlines()
    #     lines = "\n".join(line)
        # SendEmail("hsiaochi@qti.qualcomm.com","hsiaochi@qti.qualcomm.com","error data",lines)
        # os.remove(ERROR_TXT)

    for temp in temp_list:
        if "Camera_monitor.py" in temp:
            cmd = 'taskkill /pid {} -t -f'.format(int(temp[1]))
            os.system(cmd)
        if "Camera.py" in temp:
            cmd = 'taskkill /pid {} -t -f'.format(int(temp[1]))
            os.system(cmd)
        if "cmd" in temp[0]:
            cmd = 'taskkill /pid {} -t -f'.format(int(temp[1]))
            os.system(cmd)

        
if __name__ == "__main__":
    main()
