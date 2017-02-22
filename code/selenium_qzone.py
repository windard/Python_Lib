# coding = utf-8

import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.keys import Keys 


class QzoneSpider(object):
	"""docstring for QzoneSpider"""
	def __init__(self, qq, ownqq, ownpassword):
		self.ownqq = ownqq
		self.ownpassword = ownpassword
		self.qq = qq
		self.browser = webdriver.Chrome()
		self.browser.maximize_window()

	def login(self):
		self.browser.get('http://user.qzone.qq.com/'+self.qq)
		time.sleep(2)
		print "prepare to login"
		if not self.browser.current_url.startswith('http://user.qzone.qq.com/'+self.qq):
			print "need login"
			self.browser.switch_to_frame('login_frame')
			self.browser.find_element_by_id('switcher_plogin').click()
			self.browser.find_element_by_id('u').clear()
			self.browser.find_element_by_id('u').send_keys(self.ownqq)
			self.browser.find_element_by_id('p').clear()
			self.browser.find_element_by_id('p').send_keys(self.ownpassword)
			self.browser.find_element_by_id('login_button').send_keys(Keys.ENTER)
			try:
				self.browser.find_element_by_id('login_button').send_keys(Keys.ENTER)
			except:
				pass
			print "click down"
			time.sleep(5)
			print self.browser.current_url
			if not self.browser.current_url.startswith('http://user.qzone.qq.com/'+self.qq):
				print 'inner iframe'
				try:
					self.browser.find_element_by_tag_name('iframe')
					time.sleep(2)
					self.browser.switch_to_frame(0)
					print "need to captcha"
					captcha = raw_input(">")
					self.browser.find_element_by_id("capAns").clear()
					self.browser.find_element_by_id("capAns").send_keys(captcha)
					self.browser.find_element_by_id('submit').click()
				except:
					self.browser.refresh()
					self.login()
			else:
				print "needn't captcha"
		else:
			print "needn't login"

	def find(self, method, num):
		methods = {"journal":'2', "messageBoard":'334', "photoAlbum":'4', "shuoshuo":'311'}
		self.browser.get("http://user.qzone.qq.com/"+self.qq+'/'+methods[method])
		self.browser.save_screenshot(self.qq+method+'.jpg')
		print "save image"
		self.browser.switch_to_frame('app_canvas_frame')
		# driver.switch_to.frame('app_canvas_frame')
		content = self.browser.find_elements_by_css_selector('.content')
		stime = self.browser.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
		for con,sti in zip(content,stime):
			data = {
				'time':sti.text,
				'shuos':con.text
			}
			print(data['shuos'])

		time.sleep(10)

	def exit(self):
		self.browser.quit()

if __name__ == '__main__':
	qz = QzoneSpider("1106911190", "1106911190", "XXXXX")
	qz.login()
	qz.find("shuoshuo", 10)
	qz.exit()