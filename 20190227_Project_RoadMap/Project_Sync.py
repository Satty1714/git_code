# -*- coding:utf-8 -*-
# python3.6

import os
import sys
import time
import xlrd
import shutil
import matplotlib.pyplot as plt
import pandas as pd
from xlutils.copy import copy


def ReplaceExcel():
    From_Excel = sys.argv[2]
    Excel = sys.argv[4]
    if ".xlsx" in Excel:
        To_Excel = Excel.replace(".xlsx", ".xls")
        shutil.copyfile(Excel, To_Excel)
        os.remove(Excel)
        return From_Excel,To_Excel
    else:
        return From_Excel,Excel


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

def OpenQRulerDB(From_Excel,To_Excel):
    read_data = pd.read_excel(From_Excel, sheet_name="CPEZ")
    write_data = pd.read_excel(To_Excel, sheet_name="Key Projects")
    head_list = ["Chipset","Software Product","TA Date","Assigned TAM: Full Name"]

    # 取所有行的指定列【【】,【】】二维
    data1 = read_data.ix[:,["Project","Chipset","Software Product","TA Date","Assigned TAM: Full Name"]].values
    data2 = write_data.ix[:,["Project","Chipset","Software Product","TA Date","Assigned TAM: Full Name"]].values

    dict_1 = {}
    for data1_list in data1:
        single_list = []
        for data in data1_list:
            data = str(data)
            if "00:00:00" in data:
                data = (data.split(" "))[0].split("-")
                if data[1][0] == '0':
                    data[1] = data[1].replace('0','')
                if data[2][0] == '0':
                    data[2] = data[2].replace('0','')
                data = "/".join(data)
            single_list.append(data)
        dict_1[single_list[0]] = single_list[1:]

    dict_2 = {}
    for data2_list in data2:
        mid_list = []
        for info in data2_list:
            info = str(info)
            if info == "nan":
                info = ""
            mid_list.append(str(info))
        dict_2[mid_list[0]] = mid_list[1:]
    printt(dict_2)

    keys_list = [val for val in dict_1.keys() if val in dict_2.keys()]
    # printt(keys_list)
    for index_x in range(len(keys_list)):
        read_list = dict_1[keys_list[index_x]]             #['SM8150', 'SM8150.LA.1.0', '2019/01/20', 'Wilson Fu']
        write_list = dict_2[keys_list[index_x]]            #['','','','']
        for index in range(len(write_list)):
            # 说明没有内容 然后将read_list对应的数据写到excel中保存 read_list[index]
            if write_list[index] == "":
                rb = xlrd.open_workbook(To_Excel)
                wb = copy(rb)
                ws = wb.get_sheet(1)
                ws.write(index_x+1,index+2,read_list[index])
                wb.save(To_Excel)

            else:
                # 说明有内容 ，有内容的话判断一下两个内容是否相等，如果相等不做处理，不等，输出不等的列，然后覆盖掉该信息
                if write_list[index] != read_list[index]:
                    printt("The ({}) column is different,old content is ({}) write new content is ({})".format(head_list[index],write_list[index],read_list[index]))
                    rb = xlrd.open_workbook(To_Excel)
                    wb = copy(rb)
                    ws = wb.get_sheet(1)
                    ws.write(index_x + 1, index + 2, read_list[index])
                    wb.save(To_Excel)
    printt('writing is finished')

def main():
    From_Excel,To_Excel = ReplaceExcel()
    OpenQRulerDB(From_Excel, To_Excel)

if __name__ == '__main__':
    main()

