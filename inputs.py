import time
from pynput import mouse, keyboard
from pynput.mouse import Controller, Button
from pynput.keyboard import Key, KeyCode, Controller as Keyboard_Controller
import pyautogui
import sys
import os
import numpy as np

isRunning = False

movements = []
checkpoints = []
special_keys = [Key.ctrl_l, Key.alt_l, Key.alt_r, Key.shift, Key.cmd]

mouse_controller = Controller()
keyboard_controller = Keyboard_Controller()

last_time = time.time()
click_time = time.time()
release_time = time.time()
last_click_time = time.time()

last_key_time = time.time()

confirm = keyboard.Key.right
cancel = keyboard.Key.esc

screen_width, screen_height = pyautogui.size()
print(f'Resolução da tela: {screen_width}x{screen_height}')

def running():
    global isRunning
    if isRunning:
        return True
    return False

def check_for_esc():
    def on_press(key):
        if key == keyboard.Key.esc:
            print('Execução cancelada pelo usuário.')
            os._exit(1)

def wait_for_confirm():
    right_arrow_pressed = False

    def on_press(key):
        nonlocal right_arrow_pressed
        if key == confirm:
            right_arrow_pressed = True
            return False 
        elif key == cancel:
            print('Execução cancelada pelo usuário.')
            os._exit(1)

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def clipboard(char):
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', char)
    time.sleep(0.1)

def paste_clipboard():
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'v')

def is_ctrl_unicode(code) -> bool:
    if isinstance(code, KeyCode) and code.char:
        unicode_val = ord(code.char)
        return 1 <= unicode_val <= 26
    return False

def get_unicode_order_from_char(char: str) -> int:
    if len(char) != 1:
        return -1
    return ord(char)

def character_from_ctrl_unicode(order: int) -> str:
    if not 1 <= order <= 26:
        return ''
    pool = "abcdefghijklmnopqrstuvwxyz"
    return pool[order-1]

def playMacro(movements):
    global last_click_time

    check_for_esc()

    for movement in movements:
        checkpoints = movement['checkpoint']

        for i, checkpoint in enumerate(checkpoints):
            # print(checkpoint)
            
            if 'mouse_position' in checkpoint:
                mouse_position = checkpoint['mouse_position']

                mouse_controller.position = (mouse_position)
 
                if i > 0 and 'time_interval' in checkpoint:
                    time_interval = checkpoint['time_interval']
                    time.sleep(time_interval)

            if 'mouse_clicked' in checkpoint:
                mouse_controller.press(Button.left)
                last_click_time = time.time()

            if 'mouse_released' in checkpoint:
                if 'time_released' in checkpoint:
                    time_released = checkpoint['time_released']
                    time_interval = time_released - last_click_time

                    if time_interval > 0:
                        time.sleep(time_interval)

                    mouse_controller.release(Button.left)
    
            if 'keyboard_key' in checkpoint:
                # print(checkpoint['keyboard_key'])

                if i + 1 < len(checkpoints):
                    next_checkpoint = checkpoints[i+1]

                if 'special_key' in next_checkpoint:

                    special_key = next_checkpoint['keyboard_key']

                    keyboard_key = checkpoint['keyboard_key']

                    is_ctrl = is_ctrl_unicode(keyboard_key)
                    
                    if is_ctrl:
                        ctrl_code = get_unicode_order_from_char(keyboard_key.char)
                        char = character_from_ctrl_unicode(ctrl_code)

                        with keyboard_controller.pressed(next_checkpoint['keyboard_key']):
                            keyboard_controller.press(char)

                            if i > 0 and 'key_time' in checkpoint:
                                time_press = checkpoint['key_time']
                                time_interval = last_key_time - time_press 

                                if time_interval > 0:
                                    time.sleep(time_interval)

                            keyboard_controller.release(char)

                    elif special_key == special_keys[1] or special_key == special_keys[2]:
                        previous = []

                        for previous_inputs in checkpoints[::-1]:
                            previous.append(previous_inputs)

                        print(i, previous)

                        # ALT TAB FUNCIONA 1 VEZ ASSIM

                        with keyboard_controller.pressed(previous[0]['keyboard_key']):
                            keyboard_controller.press(previous[1]['keyboard_key'])

                            if i > 0 and 'key_time' in checkpoint:
                                time_press = checkpoint['key_time']
                                time_interval = last_key_time - time_press 

                                if time_interval > 0:
                                    time.sleep(time_interval)

                            keyboard_controller.release(previous[1]['keyboard_key'])

                        # SEPARAR O PREVIOUS CASO TENHA MAIS DE 1 SPECIAL KEY

                        # indexes = []
                        # for item in previous:
                        #     if item['keyboard_key'] == special_keys[1] or item['keyboard_key'] == special_keys[2]:
                        #         indexes.append(previous.index(item))

                        # list_previous = []
                        # print('indexes: ', indexes)

                        # if len(indexes) > 1:
                        #     for i in range(0, len(indexes), 2):
                        #         if i + 1 <= len(indexes):
                        #             temp = previous[indexes[i] : indexes[i+1]]
                        #             list_previous.append(temp)
                                
                        
                        # print('lp: ', list_previous)

                    # aaa
                    # bbb
                    # ccc

                else:
                    keyboard_controller.press(checkpoint['keyboard_key'])
            
                    if i > 0 and 'key_time' in checkpoint:
                        time_press = checkpoint['key_time']
                        time_interval = last_key_time - time_press 

                        if time_interval > 0:
                            time.sleep(time_interval)
                    
                    keyboard_controller.release(checkpoint['keyboard_key'])

        if len(checkpoints) > 1 and i < len(movements):
            print("Aperte a tecla {confirm.value} para continuar...")
            wait_for_confirm()

def on_press(key):
    global isRunning
    global movements
    global checkpoints

    running()

    if key == cancel:
        checkpoint = {"checkpoint": movements.copy()}
        checkpoints.append(checkpoint)
        movements.clear()
        isRunning = False
        print("Parando listeners")
        playMacro(movements = checkpoints)

        return False

    if key == confirm:
        checkpoint = {"checkpoint": movements.copy()}
        checkpoints.append(checkpoint)
        movements.clear()

def on_release(key):
    running()
    global movements    

    if key != confirm:
        last_key_time = time.time()
        movement = {"keyboard_key": key, "key_time": last_key_time, "special_key": special_keys.__contains__(key) if True else False}
        print(movement)
        movements.append(movement)
 
def on_move(x,  y):
    global movements, last_time

    if running() is False:
        return False

    current_time = time.time()
    time_interval = current_time - last_time
    last_time = current_time
    movement  = {"mouse_position": (x, y), "time_interval": time_interval}
    movements.append(movement)
    

def on_click(x, y, button, pressed):
    global movements, click_time

    if running() is False:
        return False

    current_time = time.time()

    if pressed:
        click_time = current_time
        movement = {"mouse_clicked": (x, y), "time_clicked": click_time}
    else:
        release_time = current_time
        movement = {"mouse_released": (x, y), "time_released": release_time}
    movements.append(movement)

def on_scroll(x, y, dx, dy):
    global movements

    if running() is False:
        return False

    movement = {"mouse_scroll": ((x, y), (dx, dy))}
    movements.append(movement)

def start_listeners():
    global isRunning
    isRunning = True
    
    mouse_listener =  mouse.Listener (
        on_move = on_move,
        on_click = on_click,
        on_scroll = on_scroll
    ) 

    keyboard_listener = keyboard.Listener (
        on_scroll = on_scroll,
        on_press = on_press,
        on_release = on_release
    )

    mouse_listener.start()
    keyboard_listener.start()

    mouse_listener.join()
    keyboard_listener.join()

start_listeners()

def keep_playing_macro():
    pass