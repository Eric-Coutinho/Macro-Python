from pynput import mouse, keyboard

isRunning = False

movements = []
checkpoints = []

def running():
    global isRunning
    if isRunning:
        return True
    return False

def playMacro(movements):
    for movement in movements:
        print(movement)

def on_press(key):
    global isRunning
    global movements
    global checkpoints

    running()
    print('Tecla pressionada: {0}'.format(
        key
    ))

    if key == keyboard.Key.esc:
        checkpoint = {"checkpoint": movements.copy()}
        checkpoints.append(checkpoint)
        movements.clear()
        isRunning = False
        print("Parando listeners")
        print("checkpoints: ", checkpoints)
        playMacro(movements = checkpoints)
        return False

    if key == keyboard.Key.right:
        print("movimentos: ", movements)
        checkpoint = {"checkpoint": movements.copy()}
        checkpoints.append(checkpoint)
        movements.clear()

def on_release(key):
    running()
    global movements
    
    print('Released {0}'.format(
        key
    ))

    if key != keyboard.Key.right:
        movement = {"keyboard": key}
        movements.append(movement)
 
def on_move(x,  y):
    global movements

    if running() is False:
        return False
    print('Mouse movido para {0}'.format((x, y)))
    movement  = {"mouse_position": (x, y)}
    movements.append(movement)
    

def on_click(x, y, button, pressed):
    global movements

    if running() is False:
        return False
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released', (x, y)
    ))
    if pressed:
        movement = {"mouse_clicked": (x, y)}
    else:
        movement = {"mouse_released": (x, y)}
    movements.append(movement)

def on_scroll(x, y, dx, dy):
    global movements

    if running() is False:
        return False
    print('Scrolled at {0} to {1}'.format(
        'down' if dy < 0 else 'up', (x, y)
    ))
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