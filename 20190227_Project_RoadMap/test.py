# -*- coding:utf-8 -*-
# python3.6

import matplotlib.pyplot as plt
import numpy as np
# from pylab import *



'''
    plt.plot 折线图 其中线的参数
    scatter 点状图
    pie 饼状图
    bar 柱状图
    contour 圆图
'''
'''
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

fig    = Figure()
canvas = FigureCanvas(fig)
ax     = fig.add_axes([0.1, 0.1, 0.8, 0.8])

line,  = ax.plot([0,1], [0,1])
ax.set_title("a straight line (OO)")
ax.set_xlabel("x value")
ax.set_ylabel("y value")

---------------------------------------------------------------

plt.figure(1)                # 第一张图
plt.subplot(211)             # 第一张图中的第一张子图
plt.plot([1,2,3])
plt.subplot(212)             # 第一张图中的第二张子图
plt.plot([4,5,6])


plt.figure(2)                # 第二张图
plt.plot([4,5,6])            # 默认创建子图subplot(111)

plt.figure(1)                # 切换到figure 1 ; 子图subplot(212)仍旧是当前图
plt.subplot(211)             # 令子图subplot(211)成为figure1的当前图
plt.title('Easy as 1,2,3')   # 添加subplot 211 的标题
----------------------------------------------------------------
ax = plt.subplot(111)

t = np.arange(0.0, 5.0, 0.01)
s = np.cos(2*np.pi*t)
line, = plt.plot(t, s, lw=2,lable='sine')
plt.legend(loc="upper left")

plt.annotate('local max', xy=(1, 1), xytext=(3, 1.5),
            arrowprops=dict(facecolor='red', shrink=0.05),
            )

plt.ylim(-2,2)
plt.show()
-----------------------------------------------------------------
labels='frogs','hogs','dogs','logs'
sizes=15,20,45,10
colors='yellowgreen','gold','lightskyblue','lightcoral'
explode=0,0,0,0
plt.pie(sizes,explode=explode,labels=labels,colors=colors,autopct='%1.1f%%',shadow=True,startangle=50)
plt.axis('equal')
plt.show()

plt.rcParams['font.sas-serig']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
-------------------------------------------------------------------------
mu, sigma = 100, 15
x = mu + sigma * np.random.randn(10000)

# 数据的直方图
n, bins, patches = plt.hist(x, 50, normed=1, facecolor='g', alpha=0.75)
plt.xlabel('Smarts')
plt.ylabel('Probability')
#添加标题
plt.title('Histogram of IQ')
#添加文字
plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
plt.axis([40, 160, 0, 0.03])  #坐标范围
# plt.grid(True) #网格
plt.show()


'''


from pylab import *

# # 创建一个 8 * 6 点（point）的图，并设置分辨率为 80
# figure(figsize=(8,6), dpi=80)
#
# # 创建一个新的 1 * 1 的子图，接下来的图样绘制在其中的第 1 块（也是唯一的一块）
# subplot(1,1,1)
#
# X = np.linspace(-np.pi, np.pi, 256,endpoint=True)
# C,S = np.cos(X), np.sin(X)
#
# # 绘制余弦曲线，使用蓝色的、连续的、宽度为 1 （像素）的线条
# plot(X, C, color="blue", linewidth=1.0, linestyle="-",label='sine')
#
# # 绘制正弦曲线，使用绿色的、连续的、宽度为 1 （像素）的线条
# plot(X, S, color="r", lw=4.0, linestyle="-")
#
# legend(loc='upper left')
#
# plt.axis([-4,4,-1.2,1.2])
# # 设置轴记号
#
# xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
#        [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
#
# yticks([-1, 0, +1],
#        [r'$-1$', r'$0$', r'$+1$'])
# # 在屏幕上显示
# show()
#
# a = np.arange(24)
# b = a.reshape(1,6,4) # 数量, 4行, 3列
# print(b.ndim)
# print(b)

# import datetime
def Caltime(date1,date2):
    date1 = time.strptime(date1,'%Y-%m-%d')
    date2 = time.strptime(date2,'%Y-%m-%d')
    print(date1)

    date1 = datetime.datetime(date1[0],date1[1],date1[2])
    date2 = datetime.datetime(date2[0],date2[1],date2[2])
    print(date2)

    a = (date2 - date1).days
    if a > 1:
        print("11")
    else:
        print('22')


# Caltime('2019-4-25',"2019-12-12")




# list2 = ['2019/3/20','2019/5/4','2019/5/15']
# for i in list2:
#     i = i.replace('/','-')
#     print(i)
# list2_ = [4.66, 6.13, 6.5]

# list3 = ['2018/11/20','2019/5/4','2019/11/25']

from datetime import datetime

month_dict = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8,"Sept":9, "Oct":10, "Nov":11, "Dec":12}
new_dict = {v:k for k,v in month_dict.items()}

list_value = ['3/4/2019', '3/19/2019', '3/25/2019','4/12/2019','4/20/2019','4/25/2019','5/13/2019','6/30/2019','6/30/2019']
mod_times = [datetime.strptime(m, "%m/%d/%Y") for m in list_value]
# print(mod_times)





#
# num_list = []
# for value in list_value:
#     mod = datetime.strptime(value, "%Y/%m/%d")
#     year_list = value.split('/')
#     decimal = '%.2f' % (int(year_list[-1]) / 30)
#     if mod == min_time:
#         finall_dig = 2 + eval(decimal)
#     else:
#         finall_dig = 2 + int(year_list[1]) + eval(decimal)
#     num_list.append(finall_dig)
#
# print(num_list)

import random

a = random.randint(0,14)
print(a)





