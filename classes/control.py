from pynput import keyboard as kb
import time

class control:
    def __init__(self, stop_event):
        self.stop_event = stop_event
        self.listener = kb.Listener(on_press=self.on_press)
        self.checkpoints = []
        self.confirm = kb.Key.right
        self.cancel = kb.Key.esc

    def set_confirm(self, key):
        self.confirm = key

    def set_cancel(self, key):
        self.cancel = key

    def get_checkpoints(self):
        return self.checkpoints

    def start(self):
        self.listener.start()
        self.listener.join()

    def on_press(self, key):
        if key == kb.Key.cancel:
            print("Parando todos os listeners...")
            self.stop_event.set()
            self.listener.stop()
        if key == confirm:
            self.checkpoints.append({"device": "checkpoint", "time": time.time()})
