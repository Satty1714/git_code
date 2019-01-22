#coding:utf-8
#python:3
import sys
import time
import os
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
#是否输出打印信息
print_SIGN = True


def printt(everything, SIGN=True):
    def GetTime():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

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
        print("{}{} {} {} {}".format(py_file, GetTime(), func_name, lines, everything))


def test():
    list_ = ['F1(SM8150)(SM8150.LA.1.0)','ED103(SM8150)(SM8150.LA.1.0)','BD186(SM8150)(SM8150.LA.1.0)']
    list2 = ['2019/1/20','2019/3/4','2019/3/15']
    x_list = [11, 12, 1, 2, 3, 4, 5]
    for index in range(len(list_)):
        y_list = [list_[index],list_[index],list_[index],list_[index]
            ,list_[index],list_[index],list_[index]]
        plt.plot(x_list,y_list, color='red',ls='-',lw=1)
        plt.scatter(list2,list_,color='blue',marker='d')
    #
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_color('none')

    plt.title("test")
    # plt.grid()  # 网格虚线
    plt.ylabel("some numbers")
    # plt.axis('equal')
    plt.legend(loc='upper right')
    plt.xticks(x_list,
               [r"$Nov$",r"$Dec$",r"$Jan$",r"$Feb$",r"$Mar$",r"$Apr$",r"$May$"])
    plt.show()


def ttt():
    data = {'Barton LLC': 109438.50,
            'Frami, Hills and Schmidt': 103569.59,
            'Fritsch, Russel and Anderson': 112214.71,
            'Jerde-Hilpert': 112591.43,
            'Keeling LLC': 100934.30,
            'Koepp Ltd': 103660.54,
            'Kulas Inc': 137351.96,
            'Trantow-Barrows': 123381.38,
            'White-Trantow': 135841.99,
            'Will LLC': 104437.60}
    group_data = list(data.values())
    group_names = list(data.keys())
    group_mean = np.mean(group_data)
    list_ = ['F1(SM8150)(SM8150.LA.1.0)', 'ED103(SM8150)(SM8150.LA.1.0)', 'BD186(SM8150)(SM8150.LA.1.0)']
    list2 = ['2019/1/20', '2019/3/4', '2019/3/15']
    fig,ax = plt.subplots()
    ax.scatter(list2,list_,marker='d')
    plt.show()



ttt()
def Main():
    # test()
    pass

if __name__ == "__main__":
    Main()