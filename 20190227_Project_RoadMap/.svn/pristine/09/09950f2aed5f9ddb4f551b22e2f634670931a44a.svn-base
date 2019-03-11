# -*- coding:utf-8 -*-
# python3.6

'''
    需求：
1.	左边就是项目名称， 产品，客户名称
2.	右边坐标就是按月来。
3.	横线和项目对齐，标出来TA Date的位置。
4.	红线是SNPE Release Plan 的，Candidate Release Date， 在红线下面标一不SNPE 1.23.0, 或之类的。


    HTA_Weekly_Sync.xls内容为:
                                TA Date
    F1(SM8150)(Xiaomi)          2019/1/20
    ED103(SM8150)(Oneplus)      2019/3/4
    BD186(SM8150)(OPPO)         2019/3/15

    
'''

import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import numpy as np
import matplotlib as mpl
import datetime as dt
import pandas as pd
import os

BATH_PATH = os.path.dirname(os.path.abspath(__file__))
file_ = "{}\\HTA_Weekly_Status.xls".format(BATH_PATH)

# ax2 = fig.add_subplot(212)
# date2_1 = dt.datetime(2019, 1, 1)
# date2_2 = dt.datetime(2019, 12, 31)
# delta2 = dt.timedelta(days=30)
# dates2 = mpl.dates.drange(date2_1, date2_2, delta2)
# y2 = np.random.rand(len(dates2))
# ax2.plot_date(dates2, y2, linestyle='-')
# dateFmt = mpl.dates.DateFormatter('%Y-%m-%d')
# ax2.xaxis.set_major_formatter(dateFmt)
# monthsLoc = mpl.dates.MonthLocator()
# daysLoc = mpl.dates.DayLocator(interval=5)
# ax2.xaxis.set_major_locator(monthsLoc)
# ax2.xaxis.set_minor_locator(daysLoc)
# fig.autofmt_xdate(bottom=0.18)
# fig.subplots_adjust(left=0.1)

def test():
    fig = plt.figure(figsize=(15, 5))
    ax1 = fig.add_subplot(111)
    list_ = ['F1(SM8150)(Xiaomi)','ED103(SM8150)(OPPO)','BD186(SM8150)(PLUS)']
    list2 = ['2019/1/20','2019/3/4','2019/3/15']
    x_list = [11, 12, 1, 2, 3, 4, 5]
    for index in range(len(list_)):
        y_list = [list_[index],list_[index],list_[index],list_[index]
            ,list_[index],list_[index],list_[index]]
        ax1.plot(x_list,y_list, color='gray',ls='-',lw=1)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_color('none')
    plt.title("test")
    plt.legend(loc='upper right')
    plt.show()


# test()

def Map_Drow():
    #画水平线,垂直线
    #plt.axhline(y=0,xmin=0,xmax=1,**kwargs)
    #plt.axvline(y=0,xmin=0,xmax=1,**kwargs)

    fig = plt.figure(figsize=(10,3))
    ax1 = fig.add_subplot(111)
    date1_1 = dt.datetime(2019, 1, 1)
    date1_2 = dt.datetime(2019, 12, 31)
    delta1 = dt.timedelta(days=30)
    dates1 = mpl.dates.drange(date1_1,date1_2,delta1)
    y1 = np.random.rand(len(dates1))
    ax1.plot_date(dates1,y1,linestyle='-')
    monthsLoc = mpl.dates.MonthLocator()
    # weeksLoc = mpl.dates.WeekdayLocator()
    daysLoc = mpl.dates.DayLocator(interval=5)
    ax1.xaxis.set_major_locator(monthsLoc) #主刻度
    ax1.xaxis.set_minor_locator(daysLoc)  #次刻度
    monthsFmt = mpl.dates.DateFormatter('%b')
    ax1.xaxis.set_major_formatter(monthsFmt)
    ax1.xaxis.tick_top() #刻度放在顶上
    #在轴上移除次要刻度
    plt.minorticks_off()
    #轴在顶上
    # ax1.xaxis.set_ticks_position('bottom')
    # ax1.spines['bottom'].set_position(('data',1))
    # plt.axis('off')

    #设置去除边界线
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['bottom'].set_color('none')
    plt.grid(axis='y')
    plt.show()

Map_Drow()

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

if __name__ == "__main__":
    # main()
    pass