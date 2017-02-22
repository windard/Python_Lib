# coding=utf-8

import time
from selenium import webdriver
# 引入 ActionChains 鼠标类操作
from selenium.webdriver.common.action_chains import ActionChains 
# 引入 keys 键盘类操作
from selenium.webdriver.common.keys import Keys 

browser = webdriver.Chrome()
browser.get('https://www.baidu.com')

print u'浏览器最大化'
browser.maximize_window()
text = browser.find_element_by_id('jgwab').text
print u"打印备案信息:", text 
time.sleep(2)

browser.find_element_by_id('kw').send_keys(u'windard')
print u"输入框的类型:", browser.find_element_by_id('kw').get_attribute('type')
print u"输入框的大小:", browser.find_element_by_id('kw').size 
browser.find_element_by_id('su').click()
time.sleep(2)

print u'设置浏览器为宽480，高800'
browser.set_window_size(480,800)
browser.get('https://windard.com')
time.sleep(2)

print u'页面返回刚才的搜索结果'
browser.maximize_window()
browser.back()
time.sleep(2)

print u'页面向前到我的个人网站'
browser.forward()
time.sleep(2)
browser.quit()

print u'下面以微博来进行上面的综合应用'

browser = webdriver.Chrome()

browser.get('http://weibo.com/')
time.sleep(5)
browser.find_element_by_id('loginname').clear()
browser.find_element_by_id('loginname').send_keys('usernamw')
time.sleep(2)
browser.find_element_by_id('loginname').send_keys(Keys.BACK_SPACE)
time.sleep(2)
browser.find_element_by_id('loginname').send_keys('e')
time.sleep(2)

# Ctrl + A
browser.find_element_by_id('loginname').send_keys(Keys.CONTROL,'a')
time.sleep(2)

# Ctrl + X
browser.find_element_by_id('loginname').send_keys(Keys.CONTROL,'x')
time.sleep(2)

# Ctrl + V
browser.find_element_by_id('loginname').send_keys(Keys.CONTROL,'v')
time.sleep(2)

browser.find_element_by_name('password').clear()
browser.find_element_by_name('password').send_keys('password')
# browser.find_element_by_xpath(".//*[@node-type='submitBtn']").click()
browser.find_element_by_xpath(".//*[@id='loginname']").send_keys(Keys.ENTER)
time.sleep(2)

browser.maximize_window()
article = browser.find_element_by_link_text(u'立即注册!')
ActionChains(browser).move_to_element(article).perform()
ActionChains(browser).context_click(article).perform()
time.sleep(2)
ActionChains(browser).click(article).perform()
time.sleep(2)

browser.quit()