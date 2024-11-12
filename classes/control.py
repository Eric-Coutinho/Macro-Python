from pynput import keyboard as kb
import time
from classes.player import player
from threading import Event

class control:
    def __init__(self, stop_event,):
        self.stop_event = stop_event
        self.listener = kb.Listener(on_press=self.on_press)
        self.checkpoints = []
        self.cancel = kb.Key.esc
        self.next = kb.Key.right

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
        if key == self.next:
            print('Next checkpoint\n')
            
    def wait_for_confirm(self):
        confirm_event = Event()
        print("Aperte a seta para direita para continuar")

        def on_press(key):
            if key == self.next:
                confirm_event.set()
                return False

        with kb.Listener(on_press=on_press) as listener:
            listener.join()
