from threading import Thread
from classes.mouse import mouse
from classes.keyboard import keyboard

if __name__ == "__main__":
    mouse_instance = mouse()
    keyboard_instance = keyboard()

    mouse_thread = Thread(target=mouse_instance.start)
    keyboard_thread = Thread(target=keyboard_instance.start)

    mouse_thread.start()
    keyboard_thread.start()

    mouse_thread.join()
    keyboard_thread.join()

# movements = mouse.get_movements()
# print('movements: ', movements)