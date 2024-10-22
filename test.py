import pyautogui
import pyperclip
import time

def copy_clipboard():
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.1)

def paste_clipboard():
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'v')

pyautogui.doubleClick(pyautogui.position())

list = []
var = copy_clipboard()

# list.append(var)
# print(list)
paste_clipboard()
