import time
from pynput import keyboard as kb
from pynput.keyboard import Controller, Key, KeyCode

class keyboard:

    def __init__(self):
        self.keyboard_inputs = []
        self.controller = Controller()
        
        self.record_inputs = True

        self.listener = kb.Listener(
            on_press = self.on_press,
            on_release = self.on_release
        )

    def __str__(self):
        pass
    
    def start(self):
        self.listener.start()
        self.listener.join()

    def get_listener(self):
        return self.listener
    
    def get_inputs(self):
        return self.keyboard_inputs

    def on_press(self, key):
        print('key {0} pressed'.format(
            key))
    
    def on_release(self, key):
        print('key {0} released'.format(
            key))

        if key == kb.Key.esc:
            print("Stoping execution")
            self.listener.stop()

    
