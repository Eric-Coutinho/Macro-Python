import time
from pynput import keyboard as kb
from pynput.keyboard import Controller, Key, KeyCode

class keyboard:

    def __init__(self, stop_event):
        self.stop_event = stop_event
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
        while not self.stop_event.is_set():
            pass
        self.listener.stop()

    def get_listener(self):
        if self is not None:
            return self.listener
        return None
    
    def get_inputs(self):
        if self is not None:
            return self.keyboard_inputs
        return None

    def on_press(self, key):
        if self.stop_event.is_set():
            return

        try:

            current_time = time.time()
            movement = {"press": key, "time": current_time}
            self.keyboard_inputs.append(movement)
        except:
            print("Erro ao salvar press")

    
    def on_release(self, key):
        if self.stop_event.is_set():
            return
        
        try:
            current_time = time.time()
            movement = {"release": key, "time": current_time}
            self.keyboard_inputs.append(movement)
        except:
            print('Erro ao salvar input')

    def remove_duplicate_presses(self, inputs):
        cleaned_inputs = []
        press_added = False

        for event in inputs:
            if 'release' in event:
                cleaned_inputs.append(event)
                press_added = False

            elif 'press' in event and not press_added:
                cleaned_inputs.append(event)
                press_added = True
        
        cleaned_inputs.pop()

        return cleaned_inputs