	*******Qparser_FindLable 说明文档*****
	
	
1.程序的运行环境是windows下的python3.6

2.运行该程序需要安装的库存放在requirements.txt文件下，直接运行 pip install -r requirements.txt即可安装
	
3.程序的主入口是Main()函数

4.程序会生成几个重要的文件：
	(1)log.txt 是存放所有的打印log信息
	(2)finish_caseid.txt 存放的是经过循环遍历页面完成下载的caseid和lable
	(3)time.txt 是在第二次下载之前写入的时间，为了方便判断程序是否异常处于假死状态