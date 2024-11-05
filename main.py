from threading import Thread, Event
from classes.mouse import mouse
from classes.keyboard import keyboard
from classes.control import control

if __name__ == "__main__":
    stop_event = Event()

    mouse_instance = mouse(stop_event)
    keyboard_instance = keyboard(stop_event)
    control_instance = control(stop_event)

    mouse_thread = Thread(target=mouse_instance.start)
    keyboard_thread = Thread(target=keyboard_instance.start)
    control_thread = Thread(target=control_instance.start)

    mouse_thread.start()
    keyboard_thread.start()
    control_thread.start()

    mouse_thread.join()
    keyboard_thread.join()
    control_thread.join()

movements = mouse_instance.get_movements()
print('mouse movements: ', movements)

clean_inputs = keyboard_instance.remove_duplicate_presses(keyboard_instance.get_inputs())
print('clean keyboard inputs: ', clean_inputs)

# aaaaaaaaaaaaaaaaaaaaaa