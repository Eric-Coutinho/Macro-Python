import pyautogui as pya
import time

def copy_clipboard():
    pya.hotkey('ctrl', 'c')
    time.sleep(0.1)

def paste_clipboard():
    time.sleep(0.1)
    pya.hotkey('ctrl', 'v')


# essa eh a play
def handle_alt_tab(amount):
    for i in range(amount):
        pya.hotkey('altleft', 'tab', interval = 0.1)
        time.sleep(0.1)

# essa aq tbm
def handle_mutiple_alt_tabs(amount):
    with pya.hold('altleft'):
        for i in range(amount):
            pya.press('tab')
            time.sleep(0.1)
        time.sleep(0.3)

# pya.doubleClick(pya.position())

# list = []
# var = copy_clipboard()

# list.append(var)
# print(list)
# paste_clipboard()
handle_alt_tab(amount = 2)