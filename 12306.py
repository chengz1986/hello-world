# coding=gbk

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
import base64
import re
import time
import os

class Demo():
	def __init__(self,user_name="531218020@qq.com",pass_word="***********"):
		self.coordinate=[[-105,-20],[-35,-20],[40,-20],[110,-20],[-105,50],[-35,50],[40,50],[110,50]]
		self.position=["A","B","C","D","E","F"]
		self.type=["一等座","二等座","硬座","硬卧","软卧","商务座"]
		self.type_code=["M","0","1","3","4","9"]
		self.user_name=user_name
		self.pass_word=pass_word
		with open("code.json", 'r') as file:
			code=eval(file.read())
		self.from_station=code[input("From station:")]
		self.to_station=code[input("To station:")]
		self.train_date=input("出发时间(年-月-日):")
		self.is_student=bool(input("Is student(0/1):"))
		login_url="https://kyfw.12306.cn/otn/resources/login.html"
		#driver = webdriver.Chrome()
		driver.set_window_size(1200, 900)
		driver.get(login_url)
		self.driver=driver
		if not os.path.exists("verify"):
			os.mkdir("verify")
		if os.path.exists("verify.jpg"):
			name=os.path.join("verify",str(len(os.listdir("verify")))+".jpg")
			os.rename("verify.jpg",name)			
	def login(self):		
		account=self.driver.find_element_by_class_name("login-hd-account")
		account.click()
		userName=self.driver.find_element_by_id("J-userName")
		userName.send_keys(self.user_name)
		password=self.driver.find_element_by_id("J-password")
		password.send_keys(self.pass_word)		
	def getVerifyImage(self):
		try:			
			img_element =WebDriverWait(self.driver, 100).until(
				EC.presence_of_element_located((By.ID, "J-loginImg"))
				)
		except Exception as e:
			print(u"网络开小差,请稍后尝试")	
		base64_str=img_element.get_attribute("src").split(",")[-1]
		imgdata=base64.b64decode(base64_str)
		with open('verify.jpg','wb') as file:
			file.write(imgdata)
		self.img_element=img_element
	def getVerifyResult(self):
		url="http://littlebigluo.qicp.net:47720/"
		response=requests.post(url,data={"type":"1"},files={'pic_xxfile':open('verify.jpg','rb')})
		result=[]
		#print(response.text)
		try:
			for i in re.findall("<B>(.*)</B>",response.text)[0].split(" "):
				result.append(int(i)-1)
		except Exception as e:
			print(u"图像处理服务器繁忙，请稍后尝试")
		self.result=result
	def moveAndClick(self):
		try:
			self.Action=ActionChains(self.driver)
			for i in self.result:
				self.Action.move_to_element(self.img_element).move_by_offset(self.coordinate[i][0],self.coordinate[i][1]).click()
			self.Action.perform()
		except Exception as e:
			print(e.message())
	def submit(self):
		self.driver.find_element_by_id("J-login").click()
	def queryTicket(self):
		query_url="https://kyfw.12306.cn/otn/leftTicket/init"
		self.driver.get(query_url)
		self.driver.execute_script("document.getElementById('fromStation').removeAttribute('type')")
		fromStation=self.driver.find_element_by_id("fromStation")
		fromStation.send_keys(self.from_station)
		self.driver.execute_script("document.getElementById('toStation').removeAttribute('type')")
		toStation=self.driver.find_element_by_id("toStation")
		toStation.send_keys(self.to_station)
		self.driver.execute_script("document.getElementById('train_date').removeAttribute('readonly')")
		trainDate=self.driver.find_element_by_id("train_date")
		trainDate.clear()
		trainDate.send_keys(self.train_date)
		if self.is_student:
			self.driver.find_element_by_id("sf2").click()
		self.driver.find_element_by_id("query_ticket").click()
	def ticketOrder(self):
		trains=self.driver.find_elements_by_class_name("number")
		for i,item in enumerate(trains):
			print("【{}】{}".format(i,item.text))
		num=input("请输入预定车次编号：")
		self.driver.find_elements_by_class_name("btn72")[int(num)].click()		
		ul=WebDriverWait(self.driver, 100).until(
				EC.presence_of_element_located((By.ID, "normal_passenger_id"))
				)
		time.sleep(1)
		lis=ul.find_elements_by_tag_name("li")
		for i,item in enumerate(lis):
			print("【{}】{}".format(i,item.find_elements_by_tag_name("label")[0].text))
		num=input("请输入购票人编号：")
		buy_num=int(num)
		lis[int(num)].find_elements_by_tag_name('input')[0].click()
		if self.is_student:
			self.driver.find_element_by_id("dialog_xsertcj_ok").click()
		else:
			self.driver.find_element_by_id("dialog_xsertcj_cancel").click()
		
		seatType=self.driver.find_element_by_id("seatType_1")
		
		for i,item in enumerate(self.type):
			print("【{}】{}".format(i,item))
		num=input("请输入座位类型：")
		code=self.type_code[int(num)]
		print("=======余票查询=======")
		count=1
		flag=False
		while 1:
			print("第{}次查询".format(count))		
			count+=1
			for i,item in enumerate(seatType.find_elements_by_tag_name("option")):
				if item.get_attribute("value") is code:
					flag=True
					item.click()
					break;
			if flag:
				break;
			self.driver.back()
			time.sleep(1)
			self.driver.forward()
			#================================================
			ul=WebDriverWait(self.driver, 100).until(
				EC.presence_of_element_located((By.ID, "normal_passenger_id"))
				)
			time.sleep(1.5)
			lis=ul.find_elements_by_tag_name("li")
			lis[buy_num].find_elements_by_tag_name('input')[0].click()
			if self.is_student:
				self.driver.find_element_by_id("dialog_xsertcj_ok").click()
			else:
				self.driver.find_element_by_id("dialog_xsertcj_cancel").click()
			seatType=self.driver.find_element_by_id("seatType_1")
			#================================================
			
		self.driver.find_element_by_id("submitOrder_id").click()
		if code is "M" or code is"0": 
			num=input("请输入座位编号：")
			for i,item in enumerate(self.position):
				print("【{}】{}".format(i,item))
			num=input("请输入座位编号：")
			id="1"+self.position[int(num)]
			self.driver.find_element_by_id(id).click()
		time.sleep(1)
		isorder=input("已有余票,是否预订(【0】取消 【1】预定):")
		if int(isorder):
			self.driver.find_element_by_id("qr_submit_id").click()
			print("预定成功，请及时付款")
		else:
			print("Bye~")
	def __call__(self):
		self.login()
		time.sleep(2)
		self.getVerifyImage()
		time.sleep(1)
		self.getVerifyResult()
		time.sleep(1)
		self.moveAndClick()
		time.sleep(1)
		self.submit()
		time.sleep(10)
		self.queryTicket()
		time.sleep(2)
		self.ticketOrder()
		time.sleep(10000)
		
chrome_options= webdriver.ChromeOptions()

chrome_options.add_argument('--no-sandbox')#解决DevToolsActivePort文件不存在的报错
chrome_options.add_argument('window-size=1920x3000') #指定浏览器分辨率
chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
chrome_options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视
driver = webdriver.Chrome("C:\\Windows\\System32\\chromedriver.exe",chrome_options=chrome_options)
#driver = webdriver.Chrome()
Demo()()
