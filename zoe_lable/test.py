import os
import re
import sys
import getpass
import traceback
import pandas as pd
from numpy import *
import xlrd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

pd.set_option('display.max_columns',1000)
pd.set_option('display.width',1000)
pd.set_option('display.max_colwidth',1000)

# NOTE: Please customerize the QRuler file name and the contents in this file
# qruler_file = "CVERulerDB.xlsx"
qruler_file = "China Camera CE Services mapping table_Project TA_2018SEP_2019_Part I.xlsx"

PDAF = 'PDAF\nTOP'


def read_file(qruler_file):
    import codecs
    data = xlrd.open_workbook(qruler_file)
    table = data.sheets()[0]
    keys = table.row_values(0)
    nrows = table.nrows
    col = table.ncols
    list = []

    for i in range(1,nrows):
        sheet_data = {}
        for j in range(col):
            sheet_data[keys[j]] = table.row_values(i)[j]
        list.append(sheet_data)
    return list

def write(list):
    import codecs
    f = codecs.open('qa.txt', "w",'utf-8')
    for i in list:
        f.write(str(i))



def OpenQRulerDB(qruler_file):
    dirname_temp = r"C:\workpy3_code\zoe_lable"
    path_t = "{}\\{}".format(dirname_temp, qruler_file)
    qruler_db = (pd.read_excel(path_t))
    head_list = list(qruler_db.columns)
    head_list = head_list[:1] + head_list[13:17] + head_list[24:34]
    # print(head_list)
    # print(len(head_list))


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

    dict_ = {"00000928":"xxxxx",'00000944':"eeeeee",'00000929':'efretfre','11111':'222'}
    need_list = []
    for excel_data in double_list:
        for key in dict_.keys():
            if key == excel_data[0]:
                need_list.append(excel_data)
    # all_list = []
    # for need in need_list:
    #     need[1] = "/".join(((need[1].split(" "))[0]).split("-"))
    #     need[2] = "/".join(((need[2].split(" "))[0]).split("-"))
    #     real_list = []
    #     for index in range(len(need)):
    #         if need[index] == "nan":
    #             need[index] = int("-1")
    #         elif ".0" in need[index]:
    #             need[index] = eval((need[index].split('.'))[0])
    #         real_list.append(need[index])
    #     all_list.append(real_list)
    #
    # print(all_list)
    all_list = [['00000928', '2018/12/15', '2019/02/13', 'Guangjun He', 'DRI', -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                ['00000944', '2018/07/02', '2018/10/15', 'Mingchen Gao', 'DRI', 2, -1, 1, 1, -1, -1, -1, -1, -1, -1]]
    new_list = []
    for new_data in all_list:
        if new_data[5] == -1 or new_data[5] == 0:
            new_list.append(new_data)
        else:
            for index in range(6,len(head_list)):
                if index != 5 and type(new_data[index]) == int and new_data[index] > 0:
                    for i in range(new_data[index]):
                        new_data1 = new_data[:]
                        new_data1[index] = head_list[index]
                        new_list.append(new_data1)

    a =[]
    for x in new_list:
        # print(x)
        x1 = []
        for inde_x in range(6,len(x)):
            if str == type(x[inde_x]):
                # print([x[inde_x]])
                x1 = x[0:5] + [x[inde_x]]
            else:
                x1 = x[0:5]
                # print(x1)
        a.append(x1)
    print(a)



OpenQRulerDB(qruler_file)

list_ = []
def digui(num,list_):

    if num < 100:
        for i in range(1,num+1):
            list_.append(i)
    else:
        for j in range(1,101):
            list_.append(j)
            num = num - 100
            digui(num,list_)
    # print(list_)
    return list_
