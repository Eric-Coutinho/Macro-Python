import time
from pynput import mouse, keyboard
from pynput.mouse import Controller, Button
from pynput.keyboard import Key, Controller as Keyboard_Controller
import pyautogui

isRunning = False

movements = []
checkpoints = []

mouse_controller = Controller()
keyboard_controller = Keyboard_Controller()

last_time = time.time()
click_time = time.time()
release_time = time.time()
last_click_time = time.time()

last_key_time = time.time()

screen_width, screen_height = pyautogui.size()
print(f'Resolução da tela: {screen_width}x{screen_height}')

def running():
    global isRunning
    if isRunning:
        return True
    return False

def playMacro(movements):
    global last_click_time
    for movement in movements:
        checkpoints = movement['checkpoint']
        for i, checkpoint in enumerate(checkpoints):
            print(checkpoint)
            if 'mouse_position' in checkpoint:
                mouse_position = checkpoint['mouse_position']
                # print('Position: ', mouse_position)

                mouse_controller.position = (mouse_position)
                # print(f'Movendo o mouse para : {mouse_position}')
 
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
                    keyboard_controller.press(checkpoint['keyboard_key'])

                    if i > 0 and 'key_time' in checkpoint:
                        time_press = checkpoint['key_time']
                        time_interval = last_key_time - time_press 

                        if time_interval > 0:
                            time.sleep(time_interval)
                    
                    keyboard_controller.release(checkpoint['keyboard_key'])


def on_press(key):
    global isRunning
    global movements
    global checkpoints

    running()
    # print('Tecla pressionada: {0}'.format(
    #     key
    # ))

    if key == keyboard.Key.esc:
        checkpoint = {"checkpoint": movements.copy()}
        checkpoints.append(checkpoint)
        movements.clear()
        isRunning = False
        print("Parando listeners")
        # print("checkpoints: ", checkpoints)
        playMacro(movements = checkpoints)
        return False

    if key == keyboard.Key.right:
        # print("movimentos: ", movements)
        checkpoint = {"checkpoint": movements.copy()}
        checkpoints.append(checkpoint)
        movements.clear()

def on_release(key):
    running()
    global movements
    
    # print('Released {0}'.format(
    #     key
    # ))

    if key != keyboard.Key.right:
        last_key_time = time.time()
        movement = {"keyboard_key": key, "key_time": last_key_time}
        movements.append(movement)
 
def on_move(x,  y):
    global movements, last_time

    if running() is False:
        return False

    current_time = time.time()
    time_interval = current_time - last_time
    last_time = current_time
    # print('Mouse movido para {0}'.format((x, y)))
    movement  = {"mouse_position": (x, y), "time_interval": time_interval}
    movements.append(movement)
    

def on_click(x, y, button, pressed):
    global movements, click_time

    if running() is False:
        return False

    # print('{0} at {1}'.format(
    #     'Pressed' if pressed else 'Released', (x, y)
    # ))
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
    # print('Scrolled at {0} to {1}'.format(
    #     'down' if dy < 0 else 'up', (x, y)
    # ))
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