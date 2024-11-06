from pynput import keyboard as kb
import time
from classes.player import player

class control:
    def __init__(self, stop_event,):
        self.stop_event = stop_event
        self.listener = kb.Listener(on_press=self.on_press)
        self.checkpoints = []
        self.cancel = kb.Key.esc

    def set_cancel(self, key):
        self.cancel = key

    def get_checkpoints(self):
        return self.checkpoints

    def start(self):
        self.listener.start()
        self.listener.join()

    def on_press(self, key):
        if key == self.cancel:
            print("Parando todos os listeners...")
            self.stop_event.set()
            self.listener.stop()
