# coding:utf-8
import os, sys,re
from time import sleep
import traceback
reload(sys)
sys.setdefaultencoding('utf8')
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

class Selenium_CE(object):
	def __init__(self):
		self.browser = None;
		self.case_ID = "";
		self.user_name = "";
		self.user_pwd = "";
		self.table_rows = None;
		self.table_cols = None;
		self.table_rows_len = 0;#获得table的列数
		self.table_cols_len = 0;#获得table的行数

	#测试通过
	def __del__(self):
		self.browser.close();
		self.browser.quit();

	#测试通过
	def GetURL(self, url):
		self.url = url;

	#测试通过
	def GetCaseId(self, case_id):
		self.case_ID = case_id;

	#测试通过,函数功能不对（20171208）
	def GetUserNameAndPwd(self):
		try:
			# print "sys.argv[0]:(%s)"%sys.argv[0]
			# print "sys.argv[1]:(%s)"%sys.argv[1]
			# print "sys.argv[2]:(%s)"%sys.argv[2]
			self.user_name = sys.argv[1];
			self.user_pwd = sys.argv[2];
		except:
			if self.user_name=="" or self.user_pwd=="":
				print "input user name and pwd"

	#无需登录的直接获得browser 测试通过
	def GetBrowser(self):
		url = None;
		if self.case_ID:
			url = "https://qualcomm-cdmatech-support.my.salesforce.com/" + self.case_ID;
		else:
			url = self.url;
		if url:
			#self.GetUserNameAndPwd();
			os.chdir("C:\python27");
			browser = webdriver.Chrome();
			browser.get(url);
			self.browser = browser;

	#测试通过
	def login(self):
		url = None;
		if self.case_ID:
			url = "https://qualcomm-cdmatech-support.my.salesforce.com/" + self.case_ID;
		else:
			url = self.url;
		if url:
			#self.GetUserNameAndPwd();
			os.chdir("C:\python27")
			browser = webdriver.Chrome()
			browser.get(url)
			browser.find_element_by_xpath("//*[@id=\"frmLogin\"]/input[4]").send_keys(self.user_name)
			browser.find_element_by_xpath("//*[@id=\"frmLogin\"]/input[5]").send_keys(self.user_pwd)
			browser.find_element_by_xpath("//*[@id=\"frmLogin\"]/input[8]").click()
			browser.implicitly_wait(30)
			self.browser=browser;
		else:
			print "url and case_ID all empty"

	# 获得文本内容 测试通过
	def GetText_Xpath(self, xpath, sign=True):
		count = 0;
		text = "";
		while (sign):
			try:
				count += 0.5;
				resolved_during_customer_browser = self.browser.find_element_by_xpath(xpath);
				text = resolved_during_customer_browser.text;
				print 1
				sign = False;
			except:
				if count == 10:
					sign = False;
					traceback.print_exc();
				else:
					sleep(0.5)
		return text;

	# 清空编辑框内的值
	def ClearInputText(self, xpath_id, sign=True):
		count = 0;
		while (sign):
			try:
				count += 0.5;
				self.browser.find_element_by_id(xpath_id).clear();
				print 1
				sign = False;
			except:
				if count == 10:
					sign = False;
					traceback.print_exc();
				else:
					sleep(0.5)

	#修改编辑框内的值
	def ChangeInputText(self, xpath_id, value, sign=True):
		#browser.find_element_by_id("baidu_translate_input").send_keys(self.subject.decode('utf-8'))
		count = 0;
		while (sign):
			try:
				count += 0.5;
				self.browser.find_element_by_id(xpath_id).send_keys(value.decode('utf-8'));
				print 1
				sign = False;
			except:
				if count == 10:
					sign = False;
					traceback.print_exc();
				else:
					sleep(0.5)

	# 获得url 测试通过
	def GetUrl_Xpath(self, xpath, sign=True):
		count = 0;
		text = "";
		while (sign):
			try:
				count += 0.5;
				resolved_during_customer_browser = self.browser.find_element_by_xpath(xpath);
				text = resolved_during_customer_browser.get_attribute('href');
				sign = False;
			except:
				if count == 10:
					sign = False;
					traceback.print_exc();
				else:
					sleep(0.5)
		return text;

	#设置select的值
	def SetSelect_Text_Xpath(self,xpath,select_value,sign=True):
		count = 0;
		while (sign):
			try:
				count += 0.5;
				resolved_during_customer_browser = self.browser.find_element_by_xpath(xpath);
				Select(resolved_during_customer_browser).select_by_value(select_value);
				sign = False;
			except:
				if count == 10:
					sign = False;
					traceback.print_exc();
				else:
					sleep(0.5)

	#单击操作 测试通过
	def Click(self, xpath, sign=True):
		count = 0;
		while (sign):
			try:
				count += 0.5;
				self.browser.find_element_by_xpath(xpath).click()
				sign = False;
			except:
				if count == 10:
					sign = False;
					traceback.print_exc();
				else:
					sleep(0.5)

	#滚动条，滚动到顶端	测试通过
	def ScrollBar_TOP(self):
		# js = "var q=document.body.scrollTop=0"
		js = "var q=document.documentElement.scrollTop=0"
		self.browser.execute_script(js)

	#滚动条，滚动到底端	测试通过
	def ScrollBar_Bottom(self):
		js = "var q=document.documentElement.scrollTop=100000"
		self.browser.execute_script(js)

	#获取id table的列数 测试通过
	def GetTableAllRows(self, table_id, label):
		#table_id = "%s_RelatedCommentsList_body" % case_ID;
		#label = 'tr'
		table = self.browser.find_element_by_id(table_id);
		# table的总行数，包含标题
		table_rows = table.find_elements_by_tag_name(label)
		self.table_rows = table_rows;
		self.table_rows_len =len(table_rows);
		return len(table_rows);#test
		
	#add function sunyan 20171128
	#根据class直接获得行数
	def GetTableAllRows_ClassName(self,class_name, label):
		'''根据class直接获得行数'''
		#label = 'tr'
		table = self.browser.find_element_by_class_name(class_name);
		# table的总行数，包含标题
		table_rows = table.find_elements_by_tag_name(label)
		self.table_rows = table_rows;
		self.table_rows_len =len(table_rows);
		return len(table_rows);#test

	#获得table的行数 测试通过
	def GetTableAllCols(self, label):
		'''获得table的行数,根据tag name'''
		#label = 'th'
		if self.table_rows!=0:
			# 在table中找到第一个tr,之后在其下找到所有的th,即是tabler的总列数
			table_cols = self.table_rows[0].find_elements_by_tag_name(label)
			self.table_cols = table_cols;
			self.table_cols_len=len(table_cols);
			return self.table_cols_len #test

	#仅仅适用于comments.html 测试通过
	def GetTableText_comments(self, row_begin_index):
		'''仅仅适用于comments.html,不具备普遍性'''
		#label = 'td'
		table_info = [];
		for row in range(self.table_rows_len-2):
			print
			xpath_name = '//*[@id="fchArea"]/table/tbody/tr[%s]/td[1]/a' % (str(row + row_begin_index));
			xpath_comment = '//*[@id="fchArea"]/table/tbody/tr[%s]/td[2]'%(str(row+row_begin_index));
			print self.GetText_Xpath(xpath_name),self.GetUrl_Xpath(xpath_name),self.GetText_Xpath(xpath_comment);
			sleep(10)
			
	#add function sunyan 20171208
	def GetNameAndPwd(self, name, pwd):
		self.user_name = name;
		self.user_pwd = pwd;
		#print "("+name+")";
		#print "("+pwd+")";

	#获得当前窗口句柄 20171129
	def GetWindowHandleName(self):
		'''获得当前窗口句柄'''
		now_handle = self.browser.current_window_handle  # 获取当前窗口句柄
		return now_handle;

	#获得d的所有窗口句柄（程序打开的窗口） 20171129
	def GetAllWindowHanldesName(self):
		'''#获得d的所有窗口句柄（程序打开的窗口）'''
		all_handles = self.browser.window_handles;#获取当前窗口句柄
		return all_handles

	#根据句柄名称，切换到相应的句柄 20171129
	def GetHandle(self, handle_name):
		self.browser.switch_to_window(handle_name);#切换的相应的句柄

	#利用js的dom(document object model)，也就是文档对象模型，获取到input标签， 然后通过js来改变这个input标签的value属性。20171129
	def ChangeInputValue(self, input_xpath_id="", value=""):
		search_button = self.browser.find_element_by_id(input_xpath_id)
		try:
			# arguments[0]对应的是第一个参数，可以理解为python里的%s传参，与之类似
			value_ = "return arguments[0].value = '%s';"%value;
			self.browser.execute_script(value_, search_button);
		except:
			print "通过js设置input的value失败"

	#获得Browser,用于避免创建实例窗口 20171201
	def GetBrowser(self, browser):
		self.browser = browser
		
		
class Selenium_CE_NEW(object):
	def __init__(self):
		# self.table_rows = None;
		# self.table_cols = None;
		# self.table_rows_len = 0;#获得table的列数
		# self.table_cols_len = 0;#获得table的行数
		
		self.url=None;
		self.browser=None;
		self.wait_time=5;

	def CheckInitialInformation(self):
		'''
		该函数用于检测初始信息是否满足要求；
		返回False时，同时返回错写提示信息；返回Ture时，则返回None；
		'''
		if self.url==None:
			return False,"self.URL None";
			
		return True,None;
	
	#测试通过
	def __del__(self):
		self.browser.close();
		self.browser.quit();

	#测试通过
	def Login(self):
		if self.url:
			#self.GetUserNameAndPwd();
			os.chdir("C:\python27")
			browser = webdriver.Chrome()
			print self.url;
			browser.get(self.url)
			browser.implicitly_wait(self.wait_time)
			self.browser=browser;
		else:
			print "self.url and case_ID all empty"

	# 获得文本内容 测试通过
	def GetText_Xpath(self, xpath, sign=True,count=0,text=""):
		while (sign):
			try:
				count += 0.5;
				resolved_during_customer_browser = self.browser.find_element_by_xpath(xpath);
				text = resolved_during_customer_browser.text;
				sign = False;
			except:
				if count == 10:
					sign = False;
					traceback.print_exc();
				else: sleep(0.5)
		return text;

	# 清空编辑框内的值
	def ClearInputText(self, xpath_id, sign=True,count=0):
		while (sign):
			try:
				count += 0.5;
				self.browser.find_element_by_id(xpath_id).clear();
				sign = False;
			except:
				if count == 10:
					sign = False;
					traceback.print_exc();
				else: sleep(0.5)

	#修改编辑框内的值
	def ChangeInputText(self, xpath_id, value, sign=True,count=0):
		while (sign):
			try:
				count += 0.5;
				self.browser.find_element_by_id(xpath_id).send_keys(value.decode('utf-8'));
				sign = False;
			except:
				if count == 10:
					sign = False;
					traceback.print_exc();
				else: sleep(0.5)

	# 获得url 测试通过
	def GetUrl_Xpath(self, xpath, sign=True,count=0,text=""):
		while (sign):
			try:
				count += 0.5;
				resolved_during_customer_browser = self.browser.find_element_by_xpath(xpath);
				text = resolved_during_customer_browser.get_attribute('href');
				sign = False;
			except:
				if count == 10:
					sign = False;
					traceback.print_exc();
				else: sleep(0.5)
		return text;

	#设置select的值
	def SetSelect_Text_Xpath(self,xpath,select_value,sign=True,count=0):
		while (sign):
			try:
				count += 0.5;
				resolved_during_customer_browser = self.browser.find_element_by_xpath(xpath);
				Select(resolved_during_customer_browser).select_by_value(select_value);
				sign = False;
			except:
				if count == 10:
					sign = False;
					traceback.print_exc();
				else: sleep(0.5)

	#单击操作 测试通过
	def Click(self, xpath, sign=True,count=0):
		while (sign):
			try:
				count += 0.5;
				self.browser.find_element_by_xpath(xpath).click()
				sign = False;
			except:
				if count == 10:
					sign = False;
					traceback.print_exc();
				else: sleep(0.5)

	#滚动条，滚动到顶端	测试通过
	def ScrollBar_TOP(self):
		# js = "var q=document.body.scrollTop=0"
		js = "var q=document.documentElement.scrollTop=0"
		self.browser.execute_script(js)

	#滚动条，滚动到底端	测试通过
	def ScrollBar_Bottom(self):
		js = "var q=document.documentElement.scrollTop=100000"
		self.browser.execute_script(js)

	#获取id table的列数 测试通过
	def GetTableAllRows(self, table_id, label):
		#table_id = "%s_RelatedCommentsList_body" % case_ID;
		#label = 'tr'
		table = self.browser.find_element_by_id(table_id);
		# table的总行数，包含标题
		table_rows = table.find_elements_by_tag_name(label)
		self.table_rows = table_rows;
		self.table_rows_len =len(table_rows);
		return len(table_rows);#test
		
	#add function sunyan 20171128
	#根据class直接获得行数
	def GetTableAllRows_ClassName(self,class_name, label):
		'''根据class直接获得行数'''
		#label = 'tr'
		table = self.browser.find_element_by_class_name(class_name);
		# table的总行数，包含标题
		table_rows = table.find_elements_by_tag_name(label)
		self.table_rows = table_rows;
		self.table_rows_len =len(table_rows);
		return len(table_rows);#test

	#获得table的行数 测试通过
	def GetTableAllCols(self, label):
		'''获得table的行数,根据tag name'''
		#label = 'th'
		if self.table_rows!=0:
			# 在table中找到第一个tr,之后在其下找到所有的th,即是tabler的总列数
			table_cols = self.table_rows[0].find_elements_by_tag_name(label)
			self.table_cols = table_cols;
			self.table_cols_len=len(table_cols);
			return self.table_cols_len #test

	#仅仅适用于comments.html 测试通过
	def GetTableText_comments(self, row_begin_index):
		'''仅仅适用于comments.html,不具备普遍性'''
		#label = 'td'
		table_info = [];
		for row in range(self.table_rows_len-2):
			print
			xpath_name = '//*[@id="fchArea"]/table/tbody/tr[%s]/td[1]/a' % (str(row + row_begin_index));
			xpath_comment = '//*[@id="fchArea"]/table/tbody/tr[%s]/td[2]'%(str(row+row_begin_index));
			print self.GetText_Xpath(xpath_name),self.GetUrl_Xpath(xpath_name),self.GetText_Xpath(xpath_comment);
			sleep(10)
			
	#add function sunyan 20171208
	def GetNameAndPwd(self, name, pwd):
		self.user_name = name;
		self.user_pwd = pwd;
		#print "("+name+")";
		#print "("+pwd+")";

	#获得当前窗口句柄 20171129
	def GetWindowHandleName(self):
		'''获得当前窗口句柄'''
		now_handle = self.browser.current_window_handle  # 获取当前窗口句柄
		return now_handle;

	#获得d的所有窗口句柄（程序打开的窗口） 20171129
	def GetAllWindowHanldesName(self):
		'''#获得d的所有窗口句柄（程序打开的窗口）'''
		all_handles = self.browser.window_handles;#获取当前窗口句柄
		return all_handles

	#根据句柄名称，切换到相应的句柄 20171129
	def GetHandle(self, handle_name):
		self.browser.switch_to_window(handle_name);#切换的相应的句柄

	#利用js的dom(document object model)，也就是文档对象模型，获取到input标签， 然后通过js来改变这个input标签的value属性。20171129
	def ChangeInputValue(self, input_xpath_id="", value=""):
		search_button = self.browser.find_element_by_id(input_xpath_id)
		try:
			# arguments[0]对应的是第一个参数，可以理解为python里的%s传参，与之类似
			value_ = "return arguments[0].value = '%s';"%value;
			self.browser.execute_script(value_, search_button);
		except:
			print "通过js设置input的value失败"

	#获得Browser,用于避免创建实例窗口 20171201
	def GetBrowser(self, browser):
		self.browser = browser
	
	#根据元素classname
	def MoveScrollBar_ClassName(self, xpath_class):
		target = self.browser.find_element_by_class_name(xpath_class)
		self.browser.execute_script("arguments[0].scrollIntoView();", target)  # 拖动到可见的元素去

	#根据元素id
	def MoveScrollBar_ID(self, xpath_id):
		target = self.browser.find_element_by_id(xpath_id)
		# print "target:=========:{}".format(target);
		self.browser.execute_script("arguments[0].scrollIntoView();", target)  # 拖动到可见的元素去

'''
se_ce = Selenium_CE_NEW()
#se_ce.GetCaseId('5003A00000n0yWc');
se_ce.GetURL(r'https://qualcomm-cdmatech-support.my.salesforce.com/5003A00000n0yWc');
se_ce.login();
# se_ce.ScrollBar_Bottom();
# sleep(10)
# se_ce.ScrollBar_TOP();
# sleep(10)
# se_ce.GetBrowser();
# print se_ce.GetTableAllRows('fchArea','tr');
# print se_ce.GetTableAllCols('th');
#se_ce.GetTableText_comments(2);
#//*[@id="pg:frm:CustProOrHWConfigSec"]/table/tbody/tr[1]/td[2]/select
print se_ce.GetText_Xpath('//*[@id="pg:frm:CustProOrHWConfigSec"]/table/tbody/tr[1]/td[2]/select')
sleep(100)
#se_ce.Click('//*[@id="fchArea"]/table/tbody/tr[3]/td[1]/a')
sleep(100)


del se_ce;'''