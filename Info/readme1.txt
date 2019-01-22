**** Project_Sync.py****说明

1.运行环境python3
2.需要的库
pip install ：
	xlrd
	pandas
	xlutils
3.需要将写入数据的excel表保存成后缀名为 “.xls” 格式
	例如："HTA_Weekly_Status.xlsx"保存为 "HTA_Weekly_Status.xls"实现过程
	打开"HTA_Weekly_Status.xlsx" 点击左上角"文件" --> "另存为" 然后选择后缀为".xls"即可
4.进入到 Project_Sync.py文件目录 运行  python Project_Sync.py -from "China Active Projects on Dec 24.xlsx" -to "HTA_Weekly_Status.xls" 即可