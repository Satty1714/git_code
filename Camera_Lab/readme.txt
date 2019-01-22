
环境： windows下python3

********流程**********
（1）右键执行操作：
    1.安装python3 默认环境python3（必须使用python3默认）
    2.安装python库
        先在cmd下运行 pip -V 查看pip版本，若版本不是18.0，则执行 python -m pip install --upgrade pip
        然后执行 pip install -r requirements.txt
    3.运行python install.py Camera.bat
    4.右键将需要写入的excel发送到Camera
（2）也可以直接运行 python Camera_monitor.py "excel表格的全路径"

注意：
    * 1 需要保证python的默认环境是python3
    * 2 程序中获取列信息的表头是写成了固定的因此该表的表头名称以及表头的顺序不能变动
    * 3 表格式按照data_test.xlsx格式写，
        3.1其中sheet1 sheet2 以及两张表的内部表头我们只是临时性写，你们确认名称后告诉我们，我们来处理一下
        3.2 sheet1 sheet2中的内容可以自由添加 
        3.3 以后的新表需要由四个表页组合，如data_test.xlsx格式 
    * 4 chrome需要默认安装，并且在执行该程序期间chrome不能做其他的事情，避免异常的产生

通过一个监控程序调动主程序运行，目的是防止在进行页面操作填写数据时，chrome死掉导致程序异常，然后对结果造成影响。

具体：
	1.通过右键发送的方式将需要填写的excel发送到Camera 从而调动Camera_monitor程序，Camera_monitor将Camera主程序唤醒
	2.主程序先获得当前系统运行的程序，目的是在所有数据都写入页面并保存成功后将Camera_monitor程序kill
	3.读excel表格将需要的数据全部读取出来，存放到二维列表里
	4.打开浏览器到主页，取主页所有的ce services number以及对应的链接存放到字典里
	5.对比信息，将excel里和网页里相同的number取出来放到列表里
	6.将excel得到的数据进行处理，得到最终需要填写到网页中的格式和数据
	7.将6中得到的数据写到all.txt中，然后从all.txt中，然后从all.txt一条一条读取数据，然后将这条数据编辑到页面中保存
	8.将每一条保存过的数据存到save.txt中，直到程序正常运行完成 删掉这两个文件， 后退出浏览器 ，杀掉Camera_monitor和Camera和cmd 程序结束
	9.如果因为某种异常导致程序死掉，Camera_monitor会自动将主程序启动，然后对比两个文件中不同的数据然后将其填写到页面并保存，直到结束。
	