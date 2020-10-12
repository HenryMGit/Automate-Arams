import pyautogui
import time

time.sleep(5)
edit = pyautogui.locateOnScreen('./images/rune.png', confidence =0.5, grayscale = True)
print(edit)

pyautogui.click(edit)