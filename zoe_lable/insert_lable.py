# -*- coding:utf-8 -*-
# python3.6

import os,sys
import time
import pandas as pd


# qruler_file = "Data.xlsx"
qruler_file = "caselist.xlsx"


def GetTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

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


def OpenQRulerDB(qruler_file):
    # dirname_temp = r"C:\Users\liuye\Documents\GitHub\QParser\Qparser_FindLable"
    dirname_temp = r"C:\workpy3_code\zoe_lable"
    path_t = "{}\\{}".format(dirname_temp, qruler_file)
    printt(path_t)
    qruler_db = pd.read_excel(path_t)
    return qruler_db


def main():
    qruler_db = OpenQRulerDB(qruler_file)
    # project = qruler_db['Project']
    test = qruler_db['testcase']
    print(type(test))

if __name__ == '__main__':
    main()