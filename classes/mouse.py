import time
from pynput import mouse as ms
from pynput.mouse import Controller, Button

class mouse:

    def __init__(self, stop_event):
        self.stop_event = stop_event
        self.mouse_movements = []
        self.mouse_clicks = []
        self.mouse_scrolls = []
        self.controller = Controller()

        self.record_click = True
        self.record_move = True
        self.record_scroll = True

        self.listener = ms.Listener(
            on_move = self.on_move,
            on_click = self.on_click,
            on_scroll = self.on_scroll
        )

    def __str__(self):
        return f'mouse_movements: {self.mouse_movements}\nmouse_clicks: {self.mouse_clicks}\nmouse_scrolls: {self.mouse_scrolls}\n'

    def start(self):
        self.listener.start()
        while not self.stop_event.is_set():
            pass
        self.listener.stop()

    def get_listener(self):
        if self is not None:
            return self.listener
        return None

    def get_movements(self):
        if self is not None:
            return self.mouse_movements
        return None

    def get_clicks(self):
        if self is not None:
            return self.mouse_clicks
        return None
    
    def get_scrolls(self):
        if self is not None:
            return self.mouse_scrolls
        return None

    def move_to(self, x, y):
        if self.stop_event.is_set():
            return

        self.controller.position = (x, y)
    
    def mouse_click(self, button):
        if self.stop_event.is_set():
            return

        self.controller.press(button)
    
    def mouse_release(self, button):
        if self.stop_event.is_set():
            return

        self.controller.release(button)

    def on_click(self, x, y, button, pressed):
        if self.stop_event.is_set():
            return

        try:
            if self.record_click is True:
                if pressed:
                    click = {"device": "mouse", "click": (x, y), "time": time.time(), "button": button}
                else:
                    click = {"device": "mouse", "release": (x, y), "time": time.time(), "button": button}
                
                self.mouse_clicks.append(click)

                return self.mouse_clicks
            else:
                pass
        except:
            print('Erro ao salvar clique')
    
    def on_move(self, x, y):
        if self.stop_event.is_set():
            return

        try:
            if self.record_move is True:
                movement = {"device": "mouse", "move": (x, y), "time": time.time()}
                self.mouse_movements.append(movement)

                return self.mouse_movements
            else:
                pass
        except:
            print('Erro ao salvar movimento')

    def on_scroll(x, y, dx, dy):
        if self.stop_event.is_set():
            return

        try:
            if self.record_scroll is True:
                movement = {"device": "mouse", "scroll": ((x, y), (dx, dy)), "time": time.time()}
                self.mouse_scroll.append(movement)

                return self.mouse_scroll
            else:
                pass
        except:
            print('Erro ao salvar scroll')
        