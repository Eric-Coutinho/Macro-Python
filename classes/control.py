from pynput import keyboard as kb

class control:
    def __init__(self, stop_event):
        self.stop_event = stop_event
        self.listener = kb.Listener(on_press=self.on_press)

    def start(self):
        self.listener.start()
        self.listener.join()

    def on_press(self, key):
        if key == kb.Key.esc:
            print("Parando todos os listeners...")
            self.stop_event.set()
            self.listener.stop()
