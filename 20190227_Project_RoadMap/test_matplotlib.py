#coding:utf-8
#python:3

import matplotlib.pyplot as plt
import time
import sys
from datetime import datetime
import pandas as pd
import os
import random
import collections


BATH_PATH = os.path.dirname(os.path.abspath(__file__))
file_ = "{}\\HTA_Weekly_Status.xls".format(BATH_PATH)

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
        print("{} {} {} {} {}".format(py_file, GetTime(), func_name, lines, everything))


def RandomColor():
    color_list = ['1','2','3','4','5','6','7','8','9','A','B','C','E','F']
    colorArr = []
    for j in range(15):
        color = ""
        for i in range(6):
            color += color_list[random.randint(0,13)]
        colors = "#" + color
        colorArr.append(colors)

    return colorArr

def test1(data_dict):
    # ['F1(SM8150)(Xiaomi)', 'ED103(SM8150)(Oneplus)', 'BD186(SM8150)(OPPO)']
    list_key = list(data_dict.keys())
    list_value = ['2018/12/20', '2019/3/4', '2019/6/15']
    # list_value = list(data_dict.values())
    mod_times = [datetime.strptime(m, "%Y/%m/%d") for m in list_value]
    # 最大时间和最小时间
    max_time = max(mod_times)
    min_time = min(mod_times)
    # 差了几天
    day_ = (max_time - min_time).days
    month_dict = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8,"Sept":9, "Oct":10, "Nov":11, "Dec":12}

    # if 0 < day_ < 121:
    #     min_num_list = str(min_time).split('-')
    #     min_num = int(min_num_list[1])
    #     max_num_list = str(max_time).split('-')
    #     max_num = int(max_num_list[1])
    #     test_list = [x for x in range((max_num-min_num + 5))]
    #     print(test_list)
    #
    # elif 121 < day_ < 181:
    #     pass
    #
    # else:
    #     pass

    #反转字典建和值
    new_dict = {v:k for k,v in month_dict.items()}
    min_num_list = str(min_time).split('-')
    min_num = int(min_num_list[1])
    for k,v in month_dict.items():
        if v == min_num:
            key = new_dict[v]
            coll_list = list(month_dict.keys())
            index = coll_list.index(key)
            new_list = coll_list[index:] + coll_list[0:index + 1]

    fig = plt.figure(figsize=(8, 4))
    ax1 = fig.add_subplot(111)
    # list2 = [0.66, 2.13, 2.8]
    num_list = []
    for value in list_value:
        year_list = value.split('/')
        sing_dig = int(year_list[1]) - 1
        decimal = '%.2f'% (int(year_list[-1]) / 30)
        finall_dig = sing_dig + eval(decimal)
        num_list.append(finall_dig)

    # list3 = ["TA\n1/20", "TA\n3/4", "TA\n3/15"]
    note_list = []
    for val in list_value:
        month_day = val.split('/',1)
        month_day = month_day[1]
        str_1 = "TA\n{}".format(month_day)
        note_list.append(str_1)
    x_list = [x for x in range(13)]
    for index in range(len(list_key)):
        y_list = [list_key[index] for y in range(13)]
        ax1.plot(x_list, y_list, color='gray', ls='-', lw=1)
    for index in range(len(num_list)):
        ax1.scatter(num_list[index], index, color='blue', marker='d')
        ax1.annotate(note_list[index], xy=(num_list[index], index), xytext=(num_list[index]-0.08, index+0.03))

    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_color('none')
    # plt.grid()  # 网格虚线
    plt.legend(loc='upper right')
    plt.xticks(x_list,new_list)
    plt.show()

def DropMap(data_dict,colorArr):
    # ['F1(SM8150)(Xiaomi)', 'ED103(SM8150)(Oneplus)', 'BD186(SM8150)(OPPO)']
    snpe_dict = {'2019/3/31':'1.23.0', '2019/5/28':'1.24.0'}
    # list_key = list(data_dict.keys())
    # list_value = list(data_dict.values())
    list_key = ['ED103(SM8150)(OPPO)','Sharkll(SM8150)(Blackshark Technologies (Nanchang) Co., Ltd.)',
                'ED139(SM8150)(OPPO)','M1971(SM8150)(Meizu)','BD186(SM8150)(OPPO)','ED113(SM8150)(OPPO)',
                'F10(SM7150)(Xiaomi)','F11(SM8150)(Xiaomi)','JD20(SM7150)(Lenovo)','QL1828-Lenovo(SM7150)(Huaqin)']
    lists_value = ['3/4/2019', '3/19/2019', '3/25/2019','4/12/2019','4/20/2019','4/25/2019',
                  '5/6/2019','5/13/2019','6/30/2019','6/30/2019']

    #日期列表年/月/日的形式，方便下面进行操作
    list_value = []
    for ii in lists_value:
        i_list = ii.split('/')
        i_list = i_list[-1:] + i_list[:2]
        new_data = "/".join(i_list)
        list_value.append(new_data)

    mod_times = [datetime.strptime(m, "%Y/%m/%d") for m in list_value]
    # 最大时间和最小时间，以及最大和最小时间对应的月份数字和年份数字
    min_time = min(mod_times)
    min_num_list = str(min_time).split('-')
    min_num = int(min_num_list[1])
    min_year = int(min_num_list[0])
    max_time = max(mod_times)
    max_num_list = str(max_time).split('-')
    max_num = int(max_num_list[1])
    max_year = int(max_num_list[0])
    #月份对照字典
    month_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
                  "Nov": 11, "Dec": 12}
    # 将月份对应字典的键值反转
    new_dict = {v: k for k, v in month_dict.items()}
    #存放要表示x轴刻度月份的列表
    new_list = []
    # 两个时间的时间差，按天来计算
    day_ = (max_time - min_time).days
    printt(day_)
    #英文的月份列表
    coll_list = list(month_dict.keys())
    if 0 < day_ < 121:
        for k, v in month_dict.items():
            if v == min_num == 1:
                key = new_dict[max_num]
                index = coll_list.index(key)
                new_list = coll_list[10:] + coll_list[:index+3]
                break

            elif v == min_num == 2:
                key = new_dict[max_num]
                index = coll_list.index(key)
                new_list = coll_list[11:] + coll_list[:index + 3]

            elif v == min_num == 11 or v == min_num == 12 or v == max_num == 1 or v == max_num == 2:
                k1 = new_dict[min_num]
                k2 = new_dict[max_num]
                index1 = coll_list.index(k1)
                index2 = coll_list.index(k2)
                new_list = coll_list[index1-2:] + coll_list[:index2 + 3]

            elif v == max_num == 12:
                key = new_dict[min_num]
                index = coll_list.index(key)
                new_list = coll_list[index-2:] + coll_list[:2]

            elif v == max_num == 11 :
                key = new_dict[min_num]
                index = coll_list.index(key)
                new_list = coll_list[index - 2:] + coll_list[:1]

            elif v != 1 and v != 2 and v != 11 and v != 12:
                key1 = new_dict[min_num]
                key2 = new_dict[max_num]
                index1 = coll_list.index(key1)
                index2 = coll_list.index(key2)
                new_list = coll_list[index1 - 2:index2 + 3]

    elif 121 < day_ < 181:
        for k, v in month_dict.items():
            if v == min_num == 1:
                key = new_dict[max_num]
                index = coll_list.index(key)
                new_list = coll_list[11:] + coll_list[:index+2]
                break


            if v == max_num == 12:
                key = new_dict[min_num]
                index = coll_list.index(key)
                new_list = coll_list[index-1:] + coll_list[:1]
                break

            if min_year != max_year:
                key1 = new_dict[min_num]
                key2 = new_dict[max_num]
                index1 = coll_list.index(key1)
                index2 = coll_list.index(key2)
                new_list = coll_list[index1 - 1:] + coll_list[:index2 + 2]
                break


            if min_year == max_year and v != 1 and v != 12 :
                key1 = new_dict[min_num]
                key2 = new_dict[max_num]
                index1 = coll_list.index(key1)
                index2 = coll_list.index(key2)
                new_list = coll_list[index1 - 1:index2 + 2]
                break

    else:
        if min_year == max_year:
            if max_num != 12:
                key1 = new_dict[min_num]
                key2 = new_dict[max_num]
                index1 = coll_list.index(key1)
                index2 = coll_list.index(key2)
                new_list = coll_list[index1:index2 + 2]

            else:
                key1 = new_dict[min_num]
                index1 = coll_list.index(key1)
                new_list = coll_list[index1:] + coll_list[:1]

        if min_year != max_year:
            key1 = new_dict[min_num]
            key2 = new_dict[max_num]
            index1 = coll_list.index(key1)
            index2 = coll_list.index(key2)
            new_list = coll_list[index1:] + coll_list[:index2+2]


    fig = plt.figure(figsize=(10, 5))
    ax1 = fig.add_subplot(111)
    #对应时间转换成数字对应在x轴上的刻度值位置
    num_list = []
    for value in list_value:
        year_list = value.split('/')
        if int(year_list[1]) == 2:
            decimal = '%.2f' % (int(year_list[-1]) / 28)
        else:
            decimal = '%.2f' % (int(year_list[-1]) / 31)
        integer = int(year_list[1])
        eng_integer = new_dict[integer]
        in_dex = new_list.index(eng_integer)
        finall_dig = in_dex + eval(decimal)
        num_list.append(finall_dig)

    #snpe时间对应的数字刻度
    snpe_time_list = []
    for snpe_time in list(snpe_dict.keys()):
        time_data = snpe_time.split('/')
        if int(time_data[1]) == 2:
            deci = '%.2f' % (int(time_data[-1]) / 28)
        else:
            deci = '%.2f' % (int(time_data[-1]) / 31)
        inte = int(time_data[1])
        eng_inte = new_dict[inte]
        index_1 = new_list.index(eng_inte)
        fin_dig = index_1 + eval(deci)
        snpe_time_list.append(fin_dig)

    #注释列表
    note_list = []
    for val in list_value:
        month_day = val.split('/',1)
        month_day = month_day[1]
        str_1 = " TA\n{}".format(month_day)
        note_list.append(str_1)

    #横坐标的列表,画水平线
    x_list = [x for x in range(len(new_list))]
    for index in range(len(list_key)):
        y_list = [list_key[index] for y in range(len(new_list))]
        ax1.plot(x_list, y_list, color='b', ls='-', lw=1,)

    #画点 随机颜色 并且给点注释
    offset = "%.2f" %(len(list_key) / 100) #在点的正上方注释
    for index_t in range(len(num_list)):
        ax1.scatter(num_list[index_t], index_t, color=colorArr[random.randint(0,14)], marker='d')
        ax1.annotate(note_list[index_t], xy=(num_list[index_t], index_t), xytext=(num_list[index_t]-0.07, index_t + eval(offset)))

    #画一条带箭头的垂直于x轴的线，目前采用注释的方法
    # ax1.plot([2.5,2.5],[0,2],color='red',linewidth=2.5,linestyle="-")
    snpe_values = list(snpe_dict.values())
    for temp_index in range(len(snpe_time_list)):
        ax1.annotate("",xy=(snpe_time_list[temp_index],len(list_key)-1),xytext=(snpe_time_list[temp_index],0),arrowprops=dict(arrowstyle="->"))
        ax1.annotate("",xy=(snpe_time_list[temp_index],0),xytext=(snpe_time_list[temp_index],len(list_key)-1),arrowprops=dict(arrowstyle="->"))
        ax1.annotate("SNPE\n{}".format(snpe_values[temp_index]),xy=(snpe_time_list[temp_index],0),xytext=(snpe_time_list[temp_index],0))

    #将其他三个轴隐藏
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax1.xaxis.tick_top() #刻度置顶

    # plt.grid()  # 网格虚线
    plt.xticks(x_list,new_list)
    #可以设置y轴的刻度大小以及旋转角度
    # plt.yticks(range(len(list_key)),fontsize=7，rotation=70)
    #调整图片在画布中的分配
    plt.subplots_adjust(left=0.25)
    plt.show()

def OpenFile(file_):
    projects = pd.read_excel(file_,sheet_name='Key Projects')
    data = projects.ix[:,['OEM','Project','Chipset','TA Date']].values
    data_dict = {}
    for info in data:
        temp_list = []
        for single_data in info:
            temp_list.append(single_data)
        key_ = temp_list[1] + "(" + temp_list[2] + ")" + "(" + temp_list[0] + ")"
        data_dict[key_] = temp_list[-1]

    return data_dict



def main():
    data_dict = OpenFile(file_)
    colorArr = RandomColor()
    # test1(data_dict)
    DropMap(data_dict,colorArr)

if __name__ == "__main__":
    main()