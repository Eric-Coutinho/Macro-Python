from threading import Thread, Event
from classes.mouse import mouse
from classes.keyboard import keyboard
from classes.control import control
from classes.player import player

if __name__ == "__main__":
    stop_event = Event()

    mouse_instance = mouse(stop_event)
    keyboard_instance = keyboard(stop_event)
    player_instance = player(mouse_instance, keyboard_instance)
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

player = player(mouse_instance, keyboard_instance)

# player.sort_all_movements()
# player.split_by_checkpoint()
player.play_all_movements()

# aaa