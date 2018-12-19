#coding:utf-8
import os,sys
import time
import getpass
import traceback
from selenium import webdriver


file_path = os.path.split(os.path.abspath(__file__))[0]
chromedriver_path = "{}\\tools\\chromedriver\\chromedriver.exe".format(file_path)
BaseUrl = 'https://qualcomm-cdmatech-support.my.salesforce.com/00O3A000009SbBv'
base_path = r"C:\monitor_log\lable"

QXDM_TIME = 600
DIFFERENCE_TIME = 3600

def GetTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

#获得时间差
# def get_time_str():
#     def GetTime():
#         with open("{}\\time.txt".format(file_path), "r") as f:
#             old_time = f.readline()
#         return int(old_time)
#
#     number_ = GetTime()
#     if number_ == 0:
#         return -1
#     else:
#         now_time = int(time.time())
#         return now_time - number_

def get_time_str():
    def GetTime():
        with open("{}\\time.txt".format(file_path), "r") as f:
            old_time = f.readline()
        now_time = int(time.time())
        number_ = now_time - int(old_time)
        return number_
    return GetTime


#是否输出打印信息
print_SIGN=True
def printt(everything, SIGN=True):
    if print_SIGN and SIGN:
        py_file = sys._getframe(0).f_back.f_code.co_filename.split("\\")[-1]
        py_file = py_file.ljust(15, " ")
        func_name = sys._getframe(0).f_back.f_code.co_name
        if func_name != "<module>":
            func_name = func_name+"()"
        else:
            func_name = "--------"
        func_name = func_name.ljust(10, " ")
        lines = str(sys._getframe(0).f_back.f_lineno).ljust(5, " ")
        print("{}{} {} {} {}".format(py_file, GetTime(), func_name, lines, everything))


def OpenChrome_(browser=None):
    os.environ['webdriver.chrome.driver'] = chromedriver_path
    options = webdriver.ChromeOptions()
    # options.add_argument("--user-data-dir="+r"C:\Users\c_yansun\AppData\Local\Google\Chrome\User Data")
    options.add_argument("--user-data-dir=" + r"C:\Users\{}\AppData\Local\Google\Chrome\User Data".format(getpass.getuser()))
    if not browser:
        browser = webdriver.Chrome(chromedriver_path, chrome_options=options)
    browser.get(BaseUrl)
    time.sleep(5)
    try:
        browser.find_element_by_xpath("//*[@id=\"frmLogin\"]/input[8]").click()
    except:
        printt("browser already logged")
    browser.implicitly_wait(5)
    printt(browser)
    return browser


def ErrorOrSleep(count, print_info="*"*10, count_max=10):
    if count >= count_max:
        traceback.print_exc()
        return False
    else:
        print(print_info)
        time.sleep(0.5)
        return True

def GetTableRowsAndCols_xpath(browser,table_xpath,row_label,col_label):
    table = browser.find_element_by_xpath(table_xpath)
    table_rows = table.find_elements_by_tag_name(row_label)
    #用1的原因：可能第一行是标题行数据会有不同
    table_cols = table_rows[0].find_elements_by_tag_name(col_label)
    return len(table_rows),len(table_cols)


# 获得文本内容 测试通过
def GetText_Xpath(browser, xpath, sign=True, count=0, text=""):
    while (sign):
        try:
            count += 0.5
            resolved_during_customer_browser = browser.find_element_by_xpath(xpath)
            text = resolved_during_customer_browser.text
            sign = False
        except:
            sign=ErrorOrSleep(count)
    return text


def get_tasklist():
    tasklist_v_fo_csv = os.popen('tasklist /v /fo csv').read()
    tasklist_v_fo_csv_list = tasklist_v_fo_csv.split("\n")
    temp_list = []
    for tasklist in tasklist_v_fo_csv_list:
        tasklist = tasklist.replace("[", "").replace("]", "").replace("\"", "")
        temp = tasklist.split(",")
        if temp != "" and temp[0] in ["APEX.exe", "chrome.exe", "python.exe", "QCAT.exe", "QXDM.exe"]:
            temp_list.append(temp)

    return temp_list


def main():
    qxdm_info = ""
    while True:
        printt('---------- while start ----------')
        number_ = get_time_str()()
        printt("number:({})".format(number_))
        temp_list = get_tasklist()
        #kill restart_mon.... 原因：程序假死
        for temp in temp_list:
            if (number_ != -1) and ("restart_monitor" in temp) and (number_ > DIFFERENCE_TIME):
                cmd = 'taskkill /pid {} -t -f'.format(int(temp[1]))
                os.system(cmd)
                with open("{}\\time.txt".format(file_path),'w') as f:
                    f.write("{}".format(int(time.time())))

        temp_list = get_tasklist()
        for temp in temp_list:
            #处理 apex qcat error 死亡
            if temp[-1] in ['APEX', 'QCAT', 'Error']:
                cmd = 'taskkill /pid {} -t -f'.format(int(temp[1]))
                printt("temp[-1]:({})".format(temp[-1]))
                os.system(cmd)
            #处理qxdm死亡（文件缺失导致）
            if temp[0] == "QXDM.exe":
                printt("qxdm_info:({})".format(qxdm_info))
                at_time = int(time.time())
                if qxdm_info == "":
                    qxdm_info = "{},{}".format(at_time, temp[-1])
                    printt("qxdm_info:{}".format(qxdm_info))
                else:
                    info = qxdm_info.split(",")
                    if temp[-1] == info[-1]:
                        if (at_time - int(info[0])) > QXDM_TIME:
                            cmd = 'taskkill /pid {} -t -f'.format(int(temp[1]))
                            printt("cmd:{}".format(cmd))
                            os.system(cmd)
                        else:
                            printt("if (at_time - int(info[0])) > 10: else:")
                    else:
                        qxdm_info = "{},{}".format(at_time, temp[-1])

        sign2 = True
        temp_list = get_tasklist()
        printt(temp_list)
        #处理restart_mon... 关闭 分两种：一种异常，一种正常运行结束
        for temp in temp_list:
            if ("restart_monitor" in temp):
                printt('----restart_monitor exist------')
                sign2=False
                break
        if sign2:
            for temp in temp_list:
                if ("Google Chrome" in temp[-1]):
                    cmd = 'taskkill /pid {} -t -f'.format(int(temp[1]))
                    printt('---Google Chrome exist---')
                    os.system(cmd)
            printt("---log.txt not exist----")
            os.system('start "restart_monitor" python new_monitor.py')

        printt('---------- while end ----------')
        time.sleep(10*60)


if __name__ == '__main__':
    main()
