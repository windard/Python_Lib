## pyautogui

Python 3 的自动化处理库，可能因为有图像处理的库，所以依赖比较多。说的是支持 Python2 和 Python3 ，但是在 Mac 上的 Python2 有问题。

## 截图

```python
# coding=utf-8

import pyautogui


im1 = pyautogui.screenshot()
im1.save('my_screenshot.png')
im2 = pyautogui.screenshot('my_screenshot2.png')

```


## 处理

其实有一点问题，就是 `pyautogui.move` 的参数不能为 `None`

```python
# coding=utf-8


import pyautogui


screenWidth, screenHeight = pyautogui.size() # Returns two integers, the width and height of the screen. (The primary monitor, in multi-monitor setups.)
print(screenWidth, screenHeight)

currentMouseX, currentMouseY = pyautogui.position() # Returns two integers, the x and y of the mouse cursor's current position.
print(currentMouseX, currentMouseY)


pyautogui.moveTo(100, 150) # Move the mouse to the x, y coordinates 100, 150.
pyautogui.click() # Click the mouse at its current location.
pyautogui.click(200, 220) # Click the mouse at the x, y coordinates 200, 220.
pyautogui.move(0, 10)  # Move mouse 10 pixels down, that is, move the mouse relative to its current position.
pyautogui.doubleClick() # Double click the mouse at the
pyautogui.moveTo(500, 500, duration=2, tween=pyautogui.easeInOutQuad) # Use tweening/easing function to move mouse over 2 seconds.
# pyautogui.click()


pyautogui.write('Hello world!', interval=0.25)  # Type with quarter-second pause in between each key.
pyautogui.press('esc') # Simulate pressing the Escape key.
pyautogui.keyDown('shift')
pyautogui.write(['left', 'left', 'left', 'left', 'left', 'left'])
pyautogui.keyUp('shift')
pyautogui.hotkey('ctrl', 'c')

```

## 参考

[PyAutoGUI](https://github.com/asweigart/pyautogui)
