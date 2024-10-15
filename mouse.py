from pynput import mouse, keyboard

isRunning = False

def running():
    global isRunning
    if not isRunning:
        return False

def on_press(key):
    running()
    print('Tecla pressionada: {0}'.format(
        key
    ))

def on_release(key):
    running()
    global isRunning
    print('Released {0}'.format(
        key
    )) 
    
    if key == keyboard.Key.esc:
        isRunning = False
        print("Parando listeners")
        return False

def on_move(x,  y):
    if running() is False:
        return False
    print('Mouse movido para {0}'.format((x, y)))

def on_click(x, y, button, pressed):
    if running() is False:
        return False
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released', (x, y)
    ))

def on_scroll(x, y, dx, dy):
    if running() is False:
        return False
    print('Scrolled at {0} to {1}'.format(
        'down' if dy < 0 else 'up', (x, y)
    ))

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