## selenium

selenium 是一个自动化的测试工具，用来模拟浏览器操作。

使用 pip 安装好 selenium 之后，可以看到它可以模拟很多目前主流的浏览器操作，像 Firefox ，Chrome 等。

```
webdriver.Android 
webdriver.Blackberry 
webdriver.Chrome 
webdriver.Common 
webdriver.Edge 
webdriver.Firefox 
webdriver.Ie 
webdriver.Opera 
webdriver.Phantomjs 
webdriver.Remote 
webdriver.Safari 
webdriver.Support 
```

在使用 selenium 测试我们的应用之前，我们需要先安装几个浏览器驱动程序，比如说 Firefox 的 geckodriver，和 chrome 的 chromedriver，这样就能够调用这些浏览器来完成对程序的自动化测试。

下载地址：geckodriver 的[官方下载](https://github.com/mozilla/geckodriver/releases)，或者在[本站下载](../others/geckodriver-v0.11.1-win64.zip)，chromedriver 的[官方下载](https://sites.google.com/a/chromium.org/chromedriver/downloads)，或者在[本站下载](../others/chromedriver_win32.zip)。

下载完成之后可以将驱动程序所在位置加入环境变量 PATH 中，或者在每次使用时指明驱动软件的位置，同时，对于 Firefox 和 Chrome 来说，如果想要调用也需指明其二进制文件的位置，或者将二进制文件所在位置加入环境变量。

```
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

binary = FirefoxBinary(r'F:\FirefoxPortable\Firefox.exe')
driver = webdriver.Firefox(executable_path=r'C:\Chrome\geckodriver', firefox_binary=binary)

```

### 简单应用

我们来模拟一个浏览器的简单操作。

```
# coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
print driver.page_source
assert "No results found." not in driver.page_source
driver.close()

```

### 复杂应用

```
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

browser = webdriver.Chrome()

print u'下面以微博来进行上面的综合应用'
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
```