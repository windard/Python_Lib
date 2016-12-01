# coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains #引入ActionChains鼠标操作类
from selenium.webdriver.common.keys import Keys #引入keys类操作
import time

def s(int):
    time.sleep(int)
browser = webdriver.Chrome()
browser.get('http://www.baidu.com')
print u'现在将浏览器最大化'
browser.maximize_window()
text = browser.find_element_by_id('jgwab').text
print text #打印备案信息

browser.find_element_by_id('kw').send_keys(u'杨彦星')
print browser.find_element_by_id('kw').get_attribute('type')
print browser.find_element_by_id('kw').size #打印输入框的大小
browser.find_element_by_id('su').click()
time.sleep(3)

print u'现在我将设置浏览器为宽480，高800显示'
browser.set_window_size(480,800)
browser.get('http://m.mail.10086.cn')
time.sleep(3)

print u'现在我将回到刚才的页面 -- 搜索结果'
browser.maximize_window()
browser.back()
time.sleep(3)

print u'现在我将回到之前的页面 -- 百度首页'
browser.forward()
time.sleep(5)
print u'现在我将打开杨彦星的网站进行json搜索'
browser.get('http://www.yangyanxing.com')
browser.find_element_by_xpath(".//*[@id='ls']").send_keys(u'json')
browser.find_element_by_xpath(".//*[@id='header']/div[1]/div/form/input[2]").click()
time.sleep(5)
browser.quit()

browser = webdriver.Chrome()

print u'以下将以登录人人网来进行上面的综合应用'
browser.get('http://www.renren.com/SysHome.do')
browser.find_element_by_id('email').clear()#这个是以id选择元素
browser.find_element_by_id('email').send_keys('email')
browser.find_element_by_id('email').send_keys(Keys.BACK_SPACE)
time.sleep(2)
browser.find_element_by_id('email').send_keys('m')
s(2)
browser.find_element_by_id('email').send_keys(Keys.CONTROL,'a')
s(2)
browser.find_element_by_id('email').send_keys(Keys.CONTROL,'x')#剪切掉里面的内容
s(2)
browser.find_element_by_id('email').send_keys(Keys.CONTROL,'v') #重新输入进去
s(2)
browser.find_element_by_name('password').clear()#这个是以name选择元素
browser.find_element_by_name('password').send_keys('password')
#browser.find_element_by_xpath(".//*[@id='login']").click()#这个是以xpath选择元素
browser.find_element_by_xpath(".//*[@id='login']").send_keys(Keys.ENTER) #这里通过点击Enter键来登录
browser.maximize_window()
article = browser.find_element_by_link_text(u'周碧华：社科院出现内鬼意味着什么？')
ActionChains(browser).move_to_element(article).perform()#将鼠标移动到这里，但是这里不好用
ActionChains(browser).context_click(article).perform()
time.sleep(5)

browser.quit()