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
		self.type=["һ����","������","Ӳ��","Ӳ��","����","������"]
		self.type_code=["M","0","1","3","4","9"]
		self.user_name=user_name
		self.pass_word=pass_word
		with open("code.json", 'r') as file:
			code=eval(file.read())
		self.from_station=code[input("From station:")]
		self.to_station=code[input("To station:")]
		self.train_date=input("����ʱ��(��-��-��):")
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
			print(u"���翪С��,���Ժ���")	
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
			print(u"ͼ�����������æ�����Ժ���")
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
			print("��{}��{}".format(i,item.text))
		num=input("������Ԥ�����α�ţ�")
		self.driver.find_elements_by_class_name("btn72")[int(num)].click()		
		ul=WebDriverWait(self.driver, 100).until(
				EC.presence_of_element_located((By.ID, "normal_passenger_id"))
				)
		time.sleep(1)
		lis=ul.find_elements_by_tag_name("li")
		for i,item in enumerate(lis):
			print("��{}��{}".format(i,item.find_elements_by_tag_name("label")[0].text))
		num=input("�����빺Ʊ�˱�ţ�")
		buy_num=int(num)
		lis[int(num)].find_elements_by_tag_name('input')[0].click()
		if self.is_student:
			self.driver.find_element_by_id("dialog_xsertcj_ok").click()
		else:
			self.driver.find_element_by_id("dialog_xsertcj_cancel").click()
		
		seatType=self.driver.find_element_by_id("seatType_1")
		
		for i,item in enumerate(self.type):
			print("��{}��{}".format(i,item))
		num=input("��������λ���ͣ�")
		code=self.type_code[int(num)]
		print("=======��Ʊ��ѯ=======")
		count=1
		flag=False
		while 1:
			print("��{}�β�ѯ".format(count))		
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
			num=input("��������λ��ţ�")
			for i,item in enumerate(self.position):
				print("��{}��{}".format(i,item))
			num=input("��������λ��ţ�")
			id="1"+self.position[int(num)]
			self.driver.find_element_by_id(id).click()
		time.sleep(1)
		isorder=input("������Ʊ,�Ƿ�Ԥ��(��0��ȡ�� ��1��Ԥ��):")
		if int(isorder):
			self.driver.find_element_by_id("qr_submit_id").click()
			print("Ԥ���ɹ����뼰ʱ����")
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

chrome_options.add_argument('--no-sandbox')#���DevToolsActivePort�ļ������ڵı���
chrome_options.add_argument('window-size=1920x3000') #ָ��������ֱ���
chrome_options.add_argument('--disable-gpu') #�ȸ��ĵ��ᵽ��Ҫ����������������bug
chrome_options.add_argument('--hide-scrollbars') #���ع�����, Ӧ��һЩ����ҳ��
chrome_options.add_argument('blink-settings=imagesEnabled=false') #������ͼƬ, �����ٶ�
chrome_options.add_argument('--headless') #��������ṩ���ӻ�ҳ��. linux�����ϵͳ��֧�ֿ���
driver = webdriver.Chrome("C:\\Windows\\System32\\chromedriver.exe",chrome_options=chrome_options)
#driver = webdriver.Chrome()
Demo()()
