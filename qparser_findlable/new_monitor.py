#coding:utf-8
#python:3

import getpass
import logging
import os
import re
import subprocess
import sys
import time
import traceback
from logging import handlers
from time import sleep

import pandas as pd
import xlrd
from bs4 import BeautifulSoup
from selenium import webdriver

# BaseUrl = "https://qualcomm-cdmatech-support.my.salesforce.com/00O3A000009FfVy"
# BaseUrl = 'https://qualcomm-cdmatech-support.my.salesforce.com/00O3A000009SbBv'
dirname_tool, _ = os.path.split(os.path.abspath(__file__))
chromedriver_path = "{}\\tools\\chromedriver\\chromedriver.exe".format(dirname_tool)
wget_path = '{}\\tools\\wget\\wget.exe'.format(dirname_tool)
qruler_file = "LabconfRulerDB.xlsx"
base_folder = r"C:\monitor_log\lable"
cookies_path = r"C:\Users\{}\Downloads".format(getpass.getuser())

class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }#日志级别关系映射

    def __init__(self,filename,level='info',when='D',backCount=3,fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)
log = Logger('all.log',level='debug')
# log.logger.debug('debug')
# log.logger.info('info')
# log.logger.warning('警告')
# log.logger.error('报错')
# log.logger.critical('严重')
# Logger('error.log', level='error').logger.error('error')

def OpenQRulerDB(qruler_file):
    # dirname_temp = r"C:\Users\liuye\Documents\GitHub\QParser\Qparser_FindLable"
    dirname_temp = r"C:\workpy3_code\QParser\Qparser_FindLable"
    if not os.path.isfile(dirname_temp + "\\" + qruler_file):
        path_t = "{}\\Qparser_FindLable\\{}".format(dirname_temp, qruler_file)
    else:
        path_t = "{}\\{}".format(dirname_temp, qruler_file)
    printt(path_t)
    log.logger.info(path_t)
    qruler_db = pd.read_excel(path_t)
    return qruler_db

def GetKeyWords(qruler_db):
    keywords_container = qruler_db['key_words'].iloc[0].strip('\n')
    keywords_list_temp = keywords_container.split('\n')
    keywords_list = []
    for index in range(len(keywords_list_temp)):
        temp = keywords_list_temp[index].replace('[', "").replace(']', "").replace(':', "")
        keywords_list.append(temp.strip())
    printt("Keywords_list contains: {}".format(keywords_list))
    log.logger.info("Keywords_list contains: {}".format(keywords_list))
    return keywords_list


def GetTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

#是否输出打印信息
print_SIGN=False
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


def ReadCaseID(file_name):
    if not os.path.isfile("{}\\{}".format(dirname_tool, file_name)):
        return []
    with open("{}\\{}".format(dirname_tool, file_name), 'r') as f:
        case_id_list = f.readlines()
    return case_id_list

def SaveCaseID(file_name, case_id_list):
    with open("{}\\{}".format(dirname_tool, file_name), 'a') as f:
        for case_id in case_id_list:
            f.write("{}\n".format(case_id))

def OpenChrome_(qruler_db,browser=None):
    new_case_report_url = qruler_db['new_case_report'].iloc[0].strip('\n')
    printt("{}".format(new_case_report_url))
    log.logger.info("{}".format(new_case_report_url))
    os.environ['webdriver.chrome.driver'] = chromedriver_path
    options = webdriver.ChromeOptions()
    # options.add_argument("--user-data-dir="+r"C:\Users\c_yansun\AppData\Local\Google\Chrome\User Data")
    options.add_argument("--user-data-dir=" + r"C:\Users\{}\AppData\Local\Google\Chrome\User Data".format(getpass.getuser()))
    if not browser:
        browser = webdriver.Chrome(chromedriver_path, chrome_options=options)
    # new_case_report_url = 'https://qualcomm-cdmatech-support.my.salesforce.com/00O3A000009FfVy'
    browser.get(new_case_report_url)
    sleep(5)
    try:
        browser.find_element_by_xpath("//*[@id=\"frmLogin\"]/input[8]").click()
    except:
        printt("browser already logged")
        log.logger.info("browser already logged")
    browser.implicitly_wait(5)
    return browser

def ErrorOrSleep(count, print_info="*"*10, count_max=10):
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
            if count == 10:
                sign = False
                traceback.print_exc()
            else:
                sleep(1)
    return text


def GetTableRowsAndCols_xpath(browser, table_xpath, row_label, col_label):
    table = browser.find_element_by_xpath(table_xpath)
    table_rows = table.find_elements_by_tag_name(row_label)
    #用1的原因：可能第一行是标题行数据会有不同
    table_cols = table_rows[0].find_elements_by_tag_name(col_label)
    return len(table_rows),len(table_cols)

def GetReportsCaseId(browser):
    try:
        rows, cols = GetTableRowsAndCols_xpath(browser,
                    '//*[@id="fchArea"]/table/tbody', "tr", 'th')
    except:
        exit()
    printt("rows:{};cols:{}".format(rows, cols))
    log.logger.info("rows:{};cols:{}".format(rows, cols))
    case_id_list = []
    # 获得主页的所有的cr和caseID以及parent_case_id
    owner_base_xpath = '//*[@id="fchArea"]/table/tbody/tr'
    #//*[@id="fchArea"]/table/tbody/tr[2]/td[2]
    for row in range(2, rows - 1):
        case_id_list.append(GetText_Xpath(browser,
                    '{}[{}]/td[2]'.format(owner_base_xpath, row)))
    return case_id_list

def GetBestNewCaseIdInfo(browser):
    try:
        rows, cols = GetTableRowsAndCols_xpath(browser,
                                               '//*[@id="fchArea"]/table/tbody', "tr", 'th')
    except:
        exit()
    printt("rows:{};cols:{}".format(rows, cols))
    if rows == 3:
        printt("rows==3; exit")
        log.logger.info("rows==3; exit")
        exit()
    log.logger.info("rows:{};cols:{}".format(rows, cols))
    # 获得最新一条数据
    owner_base_xpath = '//*[@id="fchArea"]/table/tbody/tr'
    id_number_time_list = []
    for index in [2, 3, 5]:
        id_number_time_list.append(GetText_Xpath(browser, "{}[{}]/td[{}]".format(owner_base_xpath, rows - 2, index)))
    # case_id = GetText_Xpath(browser, "{}[{}]/td[2]".format(owner_base_xpath, rows - 2))
    # case_number = GetText_Xpath(browser, "{}[{}]/td[3]".format(owner_base_xpath, rows - 2))
    # case_create_time = GetText_Xpath(browser, "{}[{}]/td[5]".format(owner_base_xpath, rows - 2))
    printt(id_number_time_list)
    return id_number_time_list


def GetLable_Head(description_list,keyword):
    lable, index = "", 0
    reg_ = re.compile("(\d{2}\.\d{3}(-\d{1})?)")
    for subject in description_list:
        index += 1
        search_g = reg_.search(subject)
        if search_g and keyword in subject:
            print("* " * 30)
            print(subject)
            print("{}:{}".format(index, search_g.group(0)))
            lable = search_g.group(0)
    return lable


def MatchingTemplate(keywords_list,description_str):

    def GetLabelHead():
        qruler_db_s = OpenQRulerDB("caselist.xlsx")
        keywords_container = qruler_db_s['testspec'].iloc[0].strip('\n')
        printt(keywords_container)
        log.logger.info(keywords_container)
        testspec = qruler_db_s['testspec']
        testspec = list(set(testspec))
        testcase = qruler_db_s['testcase']
        testcase_list = []
        for test in testcase:
            test = "{}".format(test)
            testcase_list.append(test.split("\n")[0])
        return testspec, testcase_list

    def FindLabel_t(description_list):
        # reg_ = re.compile("([G\.]{0,1}\d*[\.|_]\d*([-|\.]\d*)?[ |_|\-]?[a|b]?)")
        reg_ = re.compile("([G\.]{0,1}\d+\.\d+(\.\d+)?[ |_|\-]?\d*[a|b]?)")
        # reg_ = re.compile("( [G\.]{0,1}\d+\.\d+(\.\d+)?[ |_|\-]?\d*[a|b]? )")
        temp_list = []
        for desc in description_list:
            temp = re.findall(reg_, desc)
            if len(temp) == 0:
                continue
            temp_list += temp#将所有的list合并
        label_list = []
        temp_list = list(set(temp_list))
        for t in temp_list:
            try:
                label_list.append(t[0].strip())
            except:
                pass

        #正序排列
        printt(label_list)
        log.logger.info(label_list)
        label_list.sort(key = lambda i:len(i),reverse=False)#从小到大
        printt(label_list)
        log.logger.info(label_list)
        label_label_list = []
        #遍历每一个元素并且判断该元素是否包含在其他元素中
        for index in range(len(label_list)):
            sign = True
            for lab in label_list:
                #包含但是不等于，排除元素本身
                if label_list[index] in lab and label_list[index] != lab:
                    sign = False
            if sign:
                label_label_list.append(label_list[index])

        testspec_list, testcase_list= GetLabelHead()
        #label list长度如果大于2则说明多个label值(两个值说明可能是头和尾)
        if len(label_label_list) == 2:
            count = 0
            count_index = -1
            for index in range(len(label_label_list)):
                # if label_label_list[index] in testspec_list:
                for test in testcase_list:
                    if label_label_list[index] == test:
                        count += 1
                        count_index = index
            if count == 2:
                printt(count)
                log.logger.info("list中都是label头")#12.2类似的
                return "" #都是头没有尾
            if count == 1:
                if count_index == 0:
                    log.logger.info("=".join(label_label_list))#12.2=34.229\\34.229-1
                    return "=".join(label_label_list)
                else:
                    log.logger.info("=".join(label_label_list[::-1]))
                    printt("=".join(label_label_list[::-1]))
                    return "=".join(label_label_list[::-1])
            if count == 0:
                printt(count)
                log.logger.info("list中都是label尾，也就是重复label")#34.229\\34.229-1
                return "" #都是尾没有头
        elif len(label_label_list) == 1:#只有一条数据只需要判断是否为尾即可
            if label_label_list[0] in testcase_list:
                return label_label_list[0]
            else:
                printt("label_label_list[0]:[{}]".format(label_label_list[0]))
                log.logger.info("label_label_list[0]:[{}]".format(label_label_list[0]))
                return ""

        else:
            printt(len(label_label_list))
            log.logger.info("label或多或少 总之不唯一")
            return "" #说明label或多或少

    printt(keywords_list)
    log.logger.info(keywords_list)
    description_list = description_str.split("\n")
    lable, template_sign = "", {}
    for keyword in keywords_list:
        regex = re.compile("(\[{}\]:)".format(keyword))  # Compiles a regex.
        for description in description_list:
            match = regex.search(description)
            if not match:
                template_sign[keyword] = 0
                continue
            else:
                template_sign[keyword] = 1
                lable = GetLable_Head(description_list, keywords_list[1])
                break
    printt(lable)
    log.logger.info(lable)
    lable = FindLabel_t(description_list)
    sign = False
    tl = list(set(template_sign.values()))
    if len(tl) == 1 and tl[0] == 1:
        printt("模板全部匹配正确")
        log.logger.info("模板全部匹配正确")
        sign = True
    else:
        if template_sign[keywords_list[0]] == 1 and template_sign[keywords_list[1]] == 1:
            printt("模板部分匹配正确，但是关键信息正确")
            log.logger.info("模板部分匹配正确，但是关键信息正确")
            sign = True
        else:
            printt("模板匹配失败，关键信息缺失")
            # log.logger.error("模板匹配失败，关键信息缺失")
            log.logger.info("模板匹配失败，关键信息缺失")

    return sign, lable

def GetCommnets(browser,case_id):
    comments_list = []
    try:
        rows1, cols1 = GetTableRowsAndCols_xpath(browser,
                        '//*[@id="{}_RelatedCommentsList_body"]/table/tbody'.format(case_id), "tr", 'th')
    except:
        return []
    printt("rows1:{};cols1{}".format(rows1, cols1))
    log.logger.info("rows1:{};cols1{}".format(rows1, cols1))
    sleep(5)
    for row in range(2, rows1+1):
        try:
            comments_xpath = '//*[@id="{}_RelatedCommentsList_body"]/table/tbody/tr[{}]/td[2]/div'.format(case_id, row)
            printt(comments_xpath)
            log.logger.info(comments_xpath)
            resolved_during_customer_browser = browser.find_element_by_xpath(comments_xpath)
            description_str = resolved_during_customer_browser.text
        except:
            comments_xpath = '//*[@id="{}_RelatedCommentsList_body"]/table/tbody/tr[{}]/td[2]'.format(case_id, row)
            printt(comments_xpath)
            log.logger.info(comments_xpath)
            resolved_during_customer_browser = browser.find_element_by_xpath(comments_xpath)
            description_str = resolved_during_customer_browser.text
        comments_list.append(description_str)
        # printt("description_str:{}".format(description_str))
    return comments_list


def FindComments(firstcomment_reminder_str,comments_list):
    template_list = []
    for tl in firstcomment_reminder_str.split("\n"):        #excel中的
        if tl in [" ", ""]:
            continue
        template_list.append(tl)
    for comm in comments_list:                              #网页中的
        temp_list = []
        for t2 in template_list:
            if t2 in comm:                                  #excel中的在网页中
                temp_list.append(0)
            else:
                temp_list.append(1)
        temp_list = list(set(temp_list))
        if len(temp_list) == 1 and temp_list[0] == 0:
            return True#不要更新了

    return False

def Click(browser, xpath, sign=True, count=0):
    while(sign):
        try:
            count += 1
            browser.find_element_by_xpath(xpath).click()
            sign = False
        except:
            if count == 10:
                sign = False
                traceback.print_exc()
            else:
                sleep(1)

def UpdateComment(browser,template_case_id,comments_info, sign1=False, sign2=False):
    #sign1 表示没有高通工程师更新过
    #sign2 表示outputs不是唯一输出，和lable检测不出
    new_xpath = '//*[@id="{}_RelatedCommentsList"]/div[1]/div/div[1]/table/tbody/tr/td[2]/input'.format(template_case_id)
    printt(new_xpath)
    log.logger.info(new_xpath)
    Click(browser, new_xpath)
    printt(comments_info)
    log.logger.info(comments_info)
    browser.find_element_by_xpath('//*[@id="CommentBody"]').send_keys(comments_info)
    if sign1 and sign2:
        browser.find_element_by_xpath('//*[@id="IsPublished"]').click()
    # Click(browser,'//*[@id="bottomButtonRow"]/input[1]')#save
    sleep(5)
    Click(browser, '//*[@id="bottomButtonRow"]/input[2]')#cancel
    pass

def GetLable(lable,description_str):
    lable_str = ""
    return lable_str

def GetUrl_Xpath(browser, xpath, sign=True, count=0, text=""):
    while (sign):
        try:
            count += 0.5
            resolved_during_customer_browser = browser.find_element_by_xpath(xpath)
            text = resolved_during_customer_browser.get_attribute('href')
            sign = False
        except:
            if count == 10:
                sign = False
                traceback.print_exc()
            else:
                sleep(1)
    return text

def GetLogUrl(browser,case_id):
    url_list = []
    try:
        rows1, cols1 = GetTableRowsAndCols_xpath(browser,
                '//*[@id="{}_00N300000042No3_body"]/table/tbody'.format(case_id), "tr", 'th')
    except:
        printt("get log name and url error")
        # log.logger.error("get log name and url error")
        log.logger.info("get log name and url error")
        return url_list
    printt(rows1)
    log.logger.info(rows1)
    if rows1 < 2:
        printt("no log")
        log.logger.info("no log")
        return url_list
    for index in range(0, rows1 - 1):
        #//*[@id="5003A00000sYOKm_00N300000042No3_body"]/table/tbody/tr[2]/th/a
        link_xpath = '//*[@id="{}_00N300000042No3_body"]/table/tbody/tr[{}]/th/a'.format(case_id, index + 2)
        url_case = GetUrl_Xpath(browser, link_xpath)
        name_case = GetText_Xpath(browser, link_xpath)
        url_list.append("{},{}".format(name_case, url_case))
    printt(url_list)
    log.logger.info(url_list)
    return url_list

#参数：文件的全路径名
def check_contain_chinese(case_name):
    tempStr = ""
    for ch in case_name:
        if 128 <= ord(ch):
            tempStr += "_"
        else:
            tempStr += ch
    return tempStr
    # return case_name

#第一次下载
#参数说明：case_number_full_path 下载路径包括number号，case_name文件名称，case_link 下载链接
def First_DownloadLink(case_number_full_path, case_name,case_link):
    download_html = '"{}" -x -q -N --load-cookies'.format(wget_path)
    download_html += ' "{}"'.format(bestnew_cookies_path)
    download_html += ' "{}" {}'.format(case_link, " --no-check-certificate -O ")
    download_html += '"{}\\{}.html"'.format(case_number_full_path, case_name)
    printt("download_html:(%s)" % download_html)
    log.logger.info("download_html:(%s)" % download_html)
    subprocessCall(download_html)

def subprocessCall(download_html):
    status_html = subprocess.call(download_html)
    if not status_html:
        printt("{} downloaded succeed".format(download_html))
        log.logger.info("{} downloaded succeed".format(download_html))
    else:
        printt("{} cfailed".format(download_html))
        log.logger.info(("{} cfailed".format(download_html)))

#html全路径文件名
def ReadHtmlAndGetURL(full_all_path_html):
    the_second_url = ""
    try:
        input_file = open(full_all_path_html,"r")
        pageDoc = input_file.read()
        res_tr = r'window.location.href =\'(.*?)\''
        m_tr = re.findall(res_tr, pageDoc, re.S | re.M)
        if len(m_tr):
            the_second_url = m_tr[0]
    except:
        the_second_url = ""
    return the_second_url

#判断cookies是否过期
def CookiesIsInvalid(download_link):
    printt("in CookiesIsInvalid; download_link:({})".format(download_link))
    log.logger.info("in CookiesIsInvalid; download_link:({})".format(download_link))
    if download_link == "":
        printt("cookies no best new, update cookies ")
        log.logger.info("cookies no best new, update cookies ")
        try:
            case_name, case_pwd = sys.argv[1], sys.argv[2]
        except:
            case_name, case_pwd = "", ""
        # cmd = "start \"GetCookies\" python %s\GetCookies.py %s %s" % (sys.path[0], case_name, case_pwd)
        cmd = "python %s\GetCookies.py %s %s" % (sys.path[0], case_name, case_pwd)
        printt("cmd info:{}".format(cmd))
        log.logger.info("cmd info:{}".format(cmd))
        os.system(cmd)
        sleep(100)

def check_contain_chinese_zh(case_number_full_path, new_case_name, case_name):
    # 如果处理后名称不一样说明有中文
    if new_case_name != case_name:
        file = open(case_number_full_path + "\\" + new_case_name + ".zh", "w")
        file.write(case_number_full_path + "\\" + new_case_name + ",")
        file.write(case_number_full_path + "\\" + case_name)
        file.close()
#第二次下载
def Second_DownloadLink(case_number_full_path,case_name,case_link):
    new_case_name = check_contain_chinese(case_name)#中文文件名过滤
    check_contain_chinese_zh(case_number_full_path, new_case_name, case_name)
    download_case = '"{}" -c -x -q -N --load-cookies'.format(wget_path)
    download_case += ' "{}" "{}" --no-check-certificate -O '.format(bestnew_cookies_path, case_link)
    download_case += '"{}\\{}"'.format(case_number_full_path, new_case_name)
    printt("download_case:(%s)" % download_case)
    log.logger.info("download_case:(%s)" % download_case)
    #download
    subprocessCall(download_case)
    #处理中文文件名称
    # filename = case_number_full_path+"\\"+case_name
    # print "filename:(%s)"%filename
    #os.rename(filename,filename.decode("utf-8"))

# 一个case被下载完成后，将log_list信息写入相应文件中
def WriteDownloadedLog(case_number_full_path, name_link):
    printt("case_number_full_path:({});name_link:({})".format(case_number_full_path, name_link))
    log.logger.info("case_number_full_path:({});name_link:({})".format(case_number_full_path, name_link))
    case_number = case_number_full_path.split("\\")[-2]
    printt("case_number:({})".format(case_number))
    log.logger.info("case_number:({})".format(case_number))
    case_number_full_path_list=case_number_full_path.split("\\")[:-1]
    # with open("{}\\{}.txt".format(case_number_full_path, case_number), 'a') as f:
    with open("{}\\{}.txt".format("\\".join(case_number_full_path_list), case_number), 'a') as f:
        f.write("downloaded_{}\n".format(name_link))

def CreateFolder(folder):
    folder_name,_ = os.path.splitext(folder)
    folder_path = "{}\\{}".format(base_folder, folder_name)
    if not os.path.isdir(folder_path):
        try:
            os.makedirs(folder_path)
        except:
            printt("create {} fail".format(folder_path))
            # log.logger.error("create {} fail".format(folder_path))
            log.logger.info("create {} fail".format(folder_path))
            return ""
    return folder_path

#获得cookies列表
def GetNewCookies(cookies_path):
    cookies_list = []
    cookies_name = 'cookies'
    for parent in os.listdir(cookies_path):
        if ".crdownload" in parent:
            continue
        if not (".txt" in parent):
            continue
        cookies_name = re.escape(cookies_name)
        m = re.search(cookies_name + '.*'+".txt", parent)
        if m:
            cookies_list.append(cookies_path+"\\"+m.group(0))
    if len(cookies_list) == 0:
        printt("no cookies files")
        # log.logger.error("no cookies files")
        log.logger.info("no cookies files")
    return cookies_list

# 获得最新的cookies名称
def GetFileCreateTime(cookies_list):
    cookies_list_temp, cookies_time_t = [], []
    now_time = time.ctime()
    now_time_list = now_time.split()
    w_m_d = "{}_{}_{}".format(now_time_list[0], now_time_list[1], now_time_list[2])# 周几_月_天
    printt(w_m_d)
    log.logger.info(w_m_d)
    for cookies in cookies_list:
        cookies_time_list = time.ctime(os.path.getctime(cookies)).split()
        w_m_d_t = "{}_{}_{}".format(cookies_time_list[0], cookies_time_list[1], cookies_time_list[2])

        # 判断日期是否为当前，是否为当年
        if (w_m_d == w_m_d_t) and (now_time_list[-1] == cookies_time_list[-1]):
            temp = cookies_time_list[-2].split(":")
            temp_time = int(temp[0]) * 60 * 60 + int(temp[1]) * 60 + int(temp[2])  # 转换为妙
            cookies_time_t.append(temp_time)  # 存储秒数
            cookies_list_temp.append(cookies)
            # printt("{} -- c_t:({})".format(cookies, time.ctime(os.path.getctime(cookies))))
            # printt("{} -- temp_time:({})".format(cookies,temp_time))
    # 获得最大数字，并且获得最大数字的下标
    try:
        index = cookies_time_t.index(max(cookies_time_t))
        # 获得最新的cookies
        printt("best new cookies:(%s)" % cookies_list_temp[index])
        log.logger.info("best new cookies:(%s)" % cookies_list_temp[index])
        return cookies_list_temp[index]
    except:
        for index in range(10):
            printt("##### cookies no best new, update cookies ###### ")
            # log.logger.error("##### cookies no best new, update cookies ###### ")
            log.logger.info("##### cookies no best new, update cookies ###### ")
        try: case_name, case_pwd = sys.argv[1], sys.argv[2]
        except: case_name, case_pwd = "", ""
        # cmd = "start \"GetCookies\" py -3 %s\GetCookies.py %s %s" % (sys.path[0], case_name, case_pwd)
        cmd = "python %s\GetCookies.py %s %s" % (sys.path[0], case_name, case_pwd)
        printt("cmd info:{}".format(cmd))
        log.logger.info("cmd info:{}".format(cmd))
        os.system(cmd)
        printt("waiting sleep(120)")
        log.logger.info("waiting sleep(120)")
        # sleep(120)
        return ""


def UpdateCookies(cookies_path):
    bestnew_cookies = ""
    if bestnew_cookies == "":
        cookies_list = GetNewCookies(cookies_path)
        print(cookies_list)
        bestnew_cookies = GetFileCreateTime(cookies_list)

    bestnew_cookies_path = bestnew_cookies
    printt("bestnew_cookies_path:({})".format(bestnew_cookies_path))
    log.logger.info("bestnew_cookies_path:({})".format(bestnew_cookies_path))
    return bestnew_cookies_path

def Download(case_number,url):
    name, link = url.split(",")
    case_number_full_path = CreateFolder("{}\\{}".format(case_number,name))
    case_number_full_path = case_number_full_path.strip()
    if case_number_full_path == "":
        return ""
    printt("download begin, \ncase_name:{}\ncase_link:{}".format(name, link))
    log.logger.info("download begin, \ncase_name:{}\ncase_link:{}".format(name, link))
    # 修改含有中文的case_name
    first_case_html = check_contain_chinese(name)
    case_number_full_path = check_contain_chinese(case_number_full_path)
    # 第一次下载获得html文件
    First_DownloadLink(case_number_full_path, first_case_html, link)
    printt(first_case_html)
    log.logger.info(first_case_html)
    # 下面的if用于应对下载失败问题，下载失败将造成ReadHtmlAndGetURL报错，CookiesIsInvalid造成提前退出等问题
    down_log_url = "{}\\{}.html".format(case_number_full_path, first_case_html)
    printt(down_log_url)
    log.logger.info(down_log_url)
    if os.path.isfile(down_log_url):
        the_second_url = ReadHtmlAndGetURL(down_log_url)
        # 判断cookies是否过期
        CookiesIsInvalid(the_second_url)
        # 删除第一次下载的html
        os.remove(case_number_full_path + "\\" + first_case_html + ".html")
        with open(sys.path[0] + "\\time.txt", "w") as f_t:
            f_t.write(str(int(time.time())))
        # 进行第二次下载
        Second_DownloadLink(case_number_full_path, name, the_second_url)
        # 以下的操作均应该在if the_second_url!="": 条件下执行；暂时不具备测试条件所以才跳出写
        # 写记录下载情况
        WriteDownloadedLog(case_number_full_path, url)
        # 修改中文的文件名名称
        file_zh = "{}\\{}.zh".format(case_number_full_path, first_case_html)
        if os.path.isfile(file_zh):
            with open(file_zh, "r") as file:
                line_list = file.readline().split(",")
                try:
                    os.rename(line_list[0], line_list[1].decode("utf-8"))
                except:
                    pass

        # AnalysisCase(case_number_full_path,url)
        # 增加邮件发送调用模块
        # CallSendEmailFunc()
    log_path = '{}\\{}'.format(case_number_full_path, name)
    return log_path

def GetCommentsInfo(relus,tr,index,sign):
    try:
        if sign: return "{}\n".format(re.findall(relus, str(tr.find_all("td")[index]))[0])
        else: return "{}".format(re.findall(relus, str(tr.find_all("td")[index]))[0])
    except:
        return "None\n"

def GetOutput(case_path):
    file_name, _ = os.path.splitext(case_path)
    scenario_file = GetScenarioPath(file_name)
    # scenario_file = "{}_uim_mmode_lte_lc_ims_ds_config_Lattice\\Scenario.xls".format(file_name)
    printt(scenario_file)
    log.logger.info(scenario_file)
    if scenario_file == "phone_log":
        return [scenario_file]
    if not os.path.isfile(scenario_file):
        printt("{} is not exits; return []".format(scenario_file))
        log.logger.info("{} is not exits; return []".format(scenario_file))
        return ["not exits"]

    fsize = os.path.getsize(scenario_file)
    if fsize == 0:
        printt("{} size:0; return []".format(scenario_file))
        # log.logger.log("{} size:0; return []".format(scenario_file))
        return ["size:0"]

    # output_list = Getscenario_xlsOutput(scenario_file)
    with open(scenario_file, 'rb') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    output_list = []
    #遍历所有的tr节点
    relus = '<td style="vnd.ms-excel.numberformat:@"><font color="#000000">(.*)</font></td>'
    for tr in soup.find_all("tr"):
        try:
            output = re.findall(relus, str(tr.find_all("td")[6]))[0]
            output_list.append(output)
        except:
            pass
    return output_list

def Getscenario_xlsOutput(scenario_xls):
    with open(scenario_xls, 'rb') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    output_list = []
    #遍历所有的tr节点
    relus = '<td style="vnd.ms-excel.numberformat:@"><font color="#000000">(.*)</font></td>'
    for tr in soup.find_all("tr"):
        try:
            output = re.findall(relus, str(tr.find_all("td")[6]))[0]
            output_list.append(output)
        except:
            pass
    return output_list

def GetScenarioPath(path_):
    # path_ = r"C:\monitor_log\lable\03772663\19.5.6"
    printt("({})".format(path_))
    log.logger.info(("({})".format(path_)))
    xls_name = "Scenario.xls"
    uim_mode = "_lc_config_Lattice"
    sign = False
    for parent, dirnames, filenames in os.walk(path_):
        for filename in filenames:
            # find_qmdl_isf = os.path.join(parent, filename)
            _, find_qmdl_isf = os.path.splitext(filename)
            if find_qmdl_isf in [".qmdl", ".isf"]:
                sign = True
                break
    if not sign:
        return "phone_log"
    for parent, dirnames, filenames in os.walk(path_):
        for filename in filenames:
            if xls_name not in os.path.join(parent, filename):
                continue
            scenario_path = "{}".format(os.path.join(parent, filename))
            if uim_mode not in scenario_path:
                continue
            print("filename with full path:{}".format(scenario_path))
            return scenario_path
    return ""

def Call_Lattice_QParser(lable_value,case_number,name_link, qruler_db):
    qparser_path, _ = os.path.split(dirname_tool)
    case_name = name_link.split(",")[0]
    folder_name, _ = os.path.splitext(case_name)
    folder_name = folder_name.strip()
    #C:\monitor_log\lable\03748405\11.25\11.25.zip
    #修改input内容(填写当前的case全路径名称)
    case_path = "{}\\{}\\{}\\{}".format(base_folder, case_number, folder_name, case_name)
    input_path = "{}\\Input.txt".format(qparser_path)
    with open(input_path, "w") as f:
        f.write(case_path)
    #生成cmd，并执行
    # str_ = "34.229\\34.229-1,15.2"
    index_bengin = lable_value.find("\\")
    if index_bengin != -1:
        index_end = lable_value.find(",")
        replace_str = lable_value[index_bengin:index_end]
        lable_value = lable_value.replace(replace_str, "")
        print(lable_value)
    #perl Lattice.pl -lc -t -q4 -ext -label="34.229,15.11a" -s
    cmd = 'perl Lattice.pl -lc -t -q4 -ext -label="{}" -s'.format(lable_value)#暂时使用start模式
    printt(cmd)
    log.logger.info(cmd)
    os.chdir(qparser_path)  # 切换到Lattice_2目录下
    log.logger.info(qparser_path)
    os.system(cmd)
    os.chdir(dirname_tool)#切换完路径后就直接切回
    log.logger.info(qparser_path)
    output_list = GetOutput(case_path)
    if len(output_list) > 1:
        comment_ownercheck_str = qruler_db['comment_ownercheck'].iloc[0].strip('\n')
        return [comment_ownercheck_str]
    return output_list

def ListToDict(list):
    new_dict = {}
    if not len(list):
        return new_dict
    for temp in list:
        temp_list = temp.split(";")
        try:
            new_dict[temp_list[0]] = temp_list[1][:-1]
        except: pass
    return new_dict


def add_interoperability(browser,lable_str):
    # Click(browser, '//*[@id="topButtonRow"]/input[1]')
    text = GetText_Xpath(browser, '//*[@id="ep"]/div[2]/div[14]/table/tbody/tr[12]/td[2]')
    printt(text)
    if lable_str not in text:
        browser.find_element_by_xpath('//*[@id="topButtonRow"]/input[1]').click()
        # text = GetText_Xpath(browser,'//*[@id="pg:frm:blk:productData:interOperabilityIOTDeviceId"]')
        if len(text) != 0 and text != " ":
            lable_str = ",{}".format(lable_str)
        browser.find_element_by_xpath('//*[@id="pg:frm:blk:productData:interOperabilityIOTDeviceId"]').send_keys(lable_str)
        Click(browser,'//*[@id="pg:frm:blk:navBtns:btnSave"]') #save
        # sleep(10)
        # Click(browser,'//*[@id="pg:frm:blk:navBtns"]/input[3]') #cancel

def GetSubjectLable(subject_str):
    '''
        这里的逻辑写的比较差，原因对lable的书写和可能的出现形式以及latticeAPI的处理都不清楚，
        无法给出更具体的方法
        处理逻辑：
        1 读出excel中的所有lable_head lable_tail
        2 将lable_head lable_tail每行对应生成串并存入listA，用"="分割
            如12.18a=34.229\34.229-1
        3 倒序遍历listA(lable_tail长度从小到大)
            for(listA[::-1]):
                for b in 需要比对的字符串listB:
                    if lable_tail in b:
                        存储到listC中（"lable_tail=lable_head"）
        #
        5 设置切出listC循环的变量
        4 for(listC[::-1]):
            if 取出lable_tail 不在 listC中的lable_tail:
                切出变量设置未False
                break
        6 根据切出变量执行后续程序。
        之所以出现5执行逻辑的原因是存在15.1和15.11以及15.11和15.11a这样的数据
        '''
    qruler_db_s = OpenQRulerDB("caselist.xlsx")

    testspec = qruler_db_s['testspec']#34.229\34.229-1
    testcase = qruler_db_s['testcase']#6.2-G.12.4类似的
    counts = testspec.size
    lable_list = []
    for index in range(counts):
        testcase_tail = testcase[index]
        lable_list.append("{};{}".format(testcase_tail, testspec[index]))#6.2;34.229
    printt(lable_list)
    log.logger.info(lable_list)
    find_lable = []
    for lable in lable_list[::-1]:
        lable_tail = lable.split(";")[0]#12.2
        lable_head = lable.split(";")[1]#34.229
        str_list = subject_str.split("\n")
        for index in range(len(str_list)):
            if lable_tail in str_list[index]:
                # find_lable.append(r"12.2=34.229\34.229-1")
                find_lable.append("{}={}".format(lable_tail, lable_head))
    if not len(find_lable):
        return ""
    sign_count = 1
    #判断是否为多个lable值
    for lable in find_lable[::-1]:
        printt("lable:{}".format(lable))
        log.logger.info("lable:{}".format(lable))
        printt("find_lable[0]:{}".format(find_lable[0]))
        log.logger.info("find_lable[0]:{}".format(find_lable[0]))
        if lable.split("=")[0] not in find_lable[0].split("=")[0]:
            #存在多个lable值
            sign_count = 0
            # printt(sign_count)
            return "Not unique Label"
        printt("sign_count:{}".format(sign_count))
        log.logger.info("sign_count:{}".format(sign_count))
    return find_lable[0]


def UpdateSign(template_list,comment):
    for tl in template_list:
        if tl not in comment:
            print("tl:({})".format(tl))
            print("update comments")
            return True
    return False

#删除多余cookies的功能
def RemoveCookies(base_path):
    import re
    reg_ = re.compile("(cookies.*\.txt)")
    for parent in os.listdir(base_path):
        reg_g = reg_.search(parent)
        if reg_g:
            print(reg_g.group(0))
            try:
                os.remove("\\".join([base_path, reg_g.group(0)]))
            except:
                print("remove error:{}".format("\\".join([base_path, reg_g.group(0)])))
    printt("remove cookies")
    log.logger.info("remove cookies")

#删除过期文件夹
def RemoveFolder(base_path, day_time=1):
    import datetime
    import shutil
    import time
    '''把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12'''
    def TimeStampToTime(timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)

    '''获取文件的创建时间'''
    def get_FileCreateTime(filePath):
        t = os.path.getctime(filePath)
        return TimeStampToTime(t)

    '''获取文件的修改时间'''
    def get_FileModifyTime(filePath):
        t = os.path.getmtime(filePath)
        return TimeStampToTime(t)

    def GetTime():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    path_list = ["\\".join([base_path, dir]) for dir in os.listdir(base_path)]
    now_time = GetTime()
    def days(str1,str2):
        date1 = datetime.datetime.strptime(str1[0:10],"%Y-%m-%d")
        date2 = datetime.datetime.strptime(str2[0:10],"%Y-%m-%d")
        num = (date1-date2).days
        return num

    for path_ in path_list:
        create_time = get_FileCreateTime(path_)
        # print(create_time)
        time_difference = days(now_time, create_time)
        if time_difference >= day_time:
            try:
                shutil.rmtree(path_)
            except:
                printt("rmtree error :{}".format(path_))
                # log.logger.error("rmtree error :{}".format(path_))
                log.logger.info("rmtree error :{}".format(path_))

def PublicAndSaveEmail(browser,caseid):
    try:
        with open("onwer_email.txt", "r") as f:
            all = f.readlines()
    except:
        all = {}
    owner_email_dict = {}
    for info in all:
        info_list = info[:-1].split(";")
        owner_email_dict[info_list[0]] = info_list[1]

    name_xpath_dict = {}
    xpath_ = '//*[@id="{}_RelatedCommentsList_body"]/table/tbody'.format(caseid)
    try:
        rows1, cols1 = GetTableRowsAndCols_xpath(browser, xpath_, "tr", 'th')
    except:
        return False
    public = True  # public：True 高通工程师没有更新过
    for row in range(2, rows1 + 1):
        click_xpath = '//*[@id="{}_RelatedCommentsList_body"]/table/tbody/tr[{}]/td[2]/div/b/a'.format(caseid,
                                                                                                       row)
        try:
            name = browser.find_element_by_xpath(click_xpath).text
            if name in owner_email_dict.keys():
                public = False  # 高通工程师更新过
                break
            if name not in name_xpath_dict.keys():
                name_xpath_dict[name] = click_xpath
        except:
            printt("{} xpath error".format(click_xpath))
            # log.logger.error("{} xpath error".format(click_xpath))
            log.logger.info("{} xpath error".format(click_xpath))
    name_email = {}
    for key, value in name_xpath_dict.items():
        url_t = browser.current_url
        try:
            browser.find_element_by_xpath(value).click()
        except:
            printt("{} xpath error".format(value))
            # log.logger.error("{} xpath error".format(value))
            log.logger.info("{} xpath error".format(value))
        email_xpath = '//*[@id="ep"]/div[2]/div[2]/table/tbody/tr[3]/td[2]/a'
        email = browser.find_element_by_xpath(email_xpath).text
        name_email[key] = email
        printt("{}:{}".format(key, email))
        log.logger.info("{}:{}".format(key, email))
        if url_t != browser.current_url:
            browser.back()
            browser.refresh()
        sleep(2)
    with open("onwer_email.txt", "a") as f:
        for key, value in name_email.items():
            if "@qti.qualcomm.com" not in value:
                continue
            if public:
                public = False
            f.write("{};{}\n".format(key, value))
    return public


def Main():
    update_log = Logger('update.log', level='debug')
    if os.path.isfile("{}\\log.txt".format(dirname_tool)):
        os.remove("{}\\log.txt".format(dirname_tool))
    qruler_db = OpenQRulerDB(qruler_file)
    keywords_list = GetKeyWords(qruler_db)
    global bestnew_cookies_path
    bestnew_cookies_path = UpdateCookies(cookies_path)
    if bestnew_cookies_path == "":
        bestnew_cookies_path = UpdateCookies(cookies_path)
    update_log.logger.info("bestnew_cookies_path:[{}]".format(bestnew_cookies_path))
    #获得已经处理过的caseID和value
    finish_list = ReadCaseID("finish_caseid.txt")
    finish_dict = ListToDict(finish_list)
    printt(finish_dict)
    log.logger.info(finish_dict)

    browser = OpenChrome_(qruler_db)
    id_number_time = ";".join(GetBestNewCaseIdInfo(browser))
    printt(id_number_time)
    log.logger.info(id_number_time)
    #获得reports中所有的caseid
    report_id_list = GetReportsCaseId(browser)
    printt(report_id_list)
    log.logger.info(report_id_list)

    # report_case_id_list中有而finish_caseid_key_list中没有的
    finish_key_list = finish_dict.keys()
    need_id_list = (set(report_id_list).difference(set(finish_key_list)))
    printt(need_id_list)
    log.logger.info(need_id_list)

    base_url = "https://qualcomm-cdmatech-support.my.salesforce.com/{}"
    # need_id_list = ['5003A00000sXcrT']

    for template_case_id in need_id_list:
        printt(base_url.format(template_case_id))
        log.logger.info(base_url.format(template_case_id))
        update_log.logger.info("template_case_id:({})".format(template_case_id))
        update_log.logger.info(base_url.format(template_case_id))
        browser.get(base_url.format(template_case_id))

        # case close
        case_status = GetText_Xpath(browser, '//*[@id="ep"]/div[2]/div[2]/table/tbody/tr[10]/td[2]')
        if (case_status == "Closed") or (case_status == 'Closed-Customer Requested'):
            printt("case_status:{} ; continue.".format(case_status))
            log.logger.info("case_status:{} ; continue.".format(case_status))
            update_log.logger.info("caseid:{}; case_status:{}; continue".format(template_case_id, case_status))
            continue

        public = PublicAndSaveEmail(browser, template_case_id)#判断是否应该公开该comment
        public = False
        printt("public:({})".format(public))
        log.logger.info("public:({})".format(public))
        update_log.logger.info("public:({})".format(public))

        # 获得所有的comments
        comments_list = GetCommnets(browser, template_case_id)
        printt(len(comments_list))
        log.logger.info(len(comments_list))

        # 获得description text
        description_str = GetText_Xpath(browser, '//*[@id="ep"]/div[2]/div[14]/table/tbody/tr[2]/td[2]')

        template_sign, lable_str = MatchingTemplate(keywords_list, description_str)
        update_log.logger.info("description label:({})".format(lable_str))
        with open("description_label_test.txt", "a") as f:
            f.write("{}; {}\n".format(template_case_id, lable_str))

        # 模板不匹配
        #**************************************** 模板不匹配更新  ********************************************
        # if not template_sign:
        #     printt("匹配失败")
        #     firstcomment_reminder_str = qruler_db['firstcomment_reminder'].iloc[0].strip('\n')
        #     find_template_str = "[Test caseID ]:<- Describe the test case ID, e.g. 15.11"
        #     if not FindComments(find_template_str, comments_list):
        #         UpdateComment(browser, template_case_id, firstcomment_reminder_str)

        if lable_str == "":
            subject_str = GetText_Xpath(browser, '//*[@id="ep"]/div[2]/div[14]/table/tbody/tr[1]/td[2]')
            printt(subject_str)
            log.logger.info(subject_str)
            lable_str = GetSubjectLable(subject_str)
            update_log.logger.info("subject label:({})".format(lable_str))
            with open("subject_label_test.txt", "a") as f:
                f.write("{}; {}\n".format(template_case_id, lable_str))


        # **************************************** 没有label 或者多个label  ********************************************
        if lable_str == "" or lable_str == "Not unique Label":
            printt("没有找到lable")
            log.logger.info("没有找到lable")
            update_log.logger.info("没有找到lable")
            comment_ownercheck_update = qruler_db['comment_ownercheck'].iloc[0].strip('\n')
            comments_list1 = comments_list[:]
            if not FindComments(comment_ownercheck_update, comments_list1):
                update_log.logger.info("label不存在，没有更新过，因此需要更新一个comments")
                UpdateComment(browser, template_case_id, comment_ownercheck_update, public, True)
            else:
                update_log.logger.info("{}{} **in comments**".format(template_case_id, comment_ownercheck_update))
            printt("continue, lable_str:({})".format(lable_str))
            update_log.logger.info("label不存在，已经更新过，因此不需要更新一个comments")
            log.logger.info("continue, lable_str:({})".format(lable_str))
            update_log.logger.info("")
            add_interoperability(browser, 'QRuler_failed')
            update_log.logger.info("label不存在，需要更新QRuler_failed到web")
            continue

        add_interoperability(browser,'QRuler_passed')
        update_log.logger.info("label存在，需要更新QRuler_passed到web")
        printt("lable_str:{}".format(lable_str))
        log.logger.info("lable_str:{}".format(lable_str))
        lable_str_list = lable_str.split("=")[::-1]
        lable_str = ",".join(lable_str_list)
        printt("lable_str:{}".format(lable_str))
        log.logger.info("lable_str:{}".format(lable_str))
        update_log.logger.info("lable_str:{}".format(lable_str))

        # printt("匹配成功")
        # log.logger.info("匹配成功")
        # update_log.logger.info("匹配成功")
        #获得caseid下所有的log名称及url地址
        url_list = GetLogUrl(browser, template_case_id)
        printt(url_list)
        log.logger.info(url_list)
        if len(url_list) == 0:
            #保存没有log的caseid和lable
            printt("url_list empty,  continue")
            log.logger.info("url_list empty,  continue")
            continue
        case_number_xpath = '//*[@id="bodyCell"]/div[1]/div[1]/div[1]/h2'
        case_number = GetText_Xpath(browser, case_number_xpath)
        for name_link in url_list:
            log_path = Download(case_number, name_link)
            if log_path == "":
                printt("continue, log_path:({})".format(log_path))
                log.logger.info("continue, log_path:({})".format(log_path))
                continue
            _, log_path_t = os.path.splitext(log_path)
            if log_path_t == ".html":
                printt("continue, log_path:({})".format(log_path))
                log.logger.info("continue, log_path:({})".format(log_path))
                continue
            output_list = Call_Lattice_QParser(lable_str, case_number, name_link, qruler_db)
            #单个log的output超过一条提示不唯一
            _, log_path_name = os.path.split(log_path)
            if len(output_list) == 0 or output_list[0] == "phone_log" or output_list[0] == "size:0" or output_list[0] == "not exits":
                comment_ownercheck_update = qruler_db['comment_ownercheck'].iloc[0].strip('\n')
                comments_list1 = comments_list[:]
                if not FindComments("{}\n{}".format(log_path_name,comment_ownercheck_update), comments_list1):
                    update_log.logger.info("{}\n{}".format(log_path_name, comment_ownercheck_update))
                    UpdateComment(browser, template_case_id,
                                  "{}\n{}".format(log_path_name, comment_ownercheck_update), public)
                    try:
                        printt("continue,output_list[0]:({})".format(output_list[0]))
                        log.logger.info("continue,output_list[0]:({})".format(output_list[0]))
                        update_log.logger.info("continue,output_list[0]:({})".format(output_list[0]))
                    except:
                        printt("continue, len(output_list):({})".format(len(output_list)))
                        log.logger.info("continue, len(output_list):({})".format(len(output_list)))
                        update_log.logger.info("continue,output_list[0]:({})".format(output_list[0]))
                else:
                    update_log.logger.info("{}\n{} **in comments**".format(log_path_name, comment_ownercheck_update))
                continue

            if not FindComments("Qualcomm  Lab Conformance  Support Team", comments_list):
                add_interoperability(browser, 'QRuler')
                UpdateComment(browser, template_case_id, "{}\n{}".format(log_path_name, output_list[0]), public, True)
                update_log.logger.info("解析后获得的输出唯一，发送QRuler到web")
                update_log.logger.info("解析后获得的输出唯一，需要更新comments")
            else:
                update_log.logger.info("{}\n{}  **in comments**".format(log_path_name, output_list[0]))
        SaveCaseID("finish_caseid.txt", ["{};{}".format(template_case_id, lable_str)])

    #****************************************
    browser.close()
    browser.quit()
    browser = None
    base_path = r"C:\Users\{}\Downloads".format(getpass.getuser())
    RemoveCookies(base_path)
    with open("{}\\log.txt".format(dirname_tool), "w") as f:
        f.write(id_number_time)

    RemoveFolder(base_folder, 3)
    sleep_time = 10 * 60
    printt("sleep({}) ".format(sleep_time))
    log.logger.info("sleep({}) ".format(sleep_time))
    sleep(sleep_time)
    exit()

def Start():
    # 网页有新的case
    def monitor_web_change(browser):
        try:
            rows, cols = GetTableRowsAndCols_xpath(browser,
                                                   '//*[@id="fchArea"]/table/tbody', "tr", 'th')
        except:
            print('---try faild---')
            return ''
        printt("rows:{};cols:{}".format(rows, cols))

        if rows == 3:
            printt("rows==3; exit")
            log.logger.info("report caseid none")
            exit()

        owner_base_xpath = '//*[@id="fchArea"]/table/tbody/tr'
        id_number_time_list1 = []
        id_number_time_list2 = []
        try:
            for index in [2, 3, 5, 6]:
                id_number_time_list1.append(
                    GetText_Xpath(browser, "{}[{}]/td[{}]".format(owner_base_xpath, rows - 2, index)))
            for index in [2, 3, 5, 6]:
                id_number_time_list2.append(GetText_Xpath(browser, "{}[{}]/td[{}]".format(owner_base_xpath, 2, index)))
            if int(id_number_time_list1[-1]) < int(id_number_time_list2[-1]):
                id_number_time_list1 = id_number_time_list1[:-1]
                id_number_time_str = ";".join(id_number_time_list1)
            else:
                id_number_time_list2 = id_number_time_list2[:-1]
                id_number_time_str = ";".join(id_number_time_list2)
            return id_number_time_str
        except:
            return ""

    if not os.path.isfile("{}\\log.txt".format(dirname_tool)):
        printt("---log.txt not exist----")
        with open('time_count.txt', 'a') as f:
            C_time = GetTime()
            f.write("{}\n{}".format(C_time, "-" * 10))
        return True
    else:
        with open("{}\\log.txt".format(dirname_tool), 'r') as fr:
            id_num_time = fr.read()
        printt(id_num_time)
        qruler_db = OpenQRulerDB(qruler_file)
        browser = OpenChrome_(qruler_db)
        id_number_time_str = monitor_web_change(browser)
        browser.close()
        browser.quit()

        if id_number_time_str != '' and (id_number_time_str != id_num_time):
            printt('--- The two Unequal---')
            return True
        else:
            printt('-----The two are equal-----')
            return False

if __name__ == "__main__":
    if Start():
        Main()
    else:
        sleep(30)
        exit()