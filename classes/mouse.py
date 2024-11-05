import time
from pynput import mouse as ms
from pynput.mouse import Controller, Button

class mouse:

    def __init__(self, stop_event):
        self.stop_event = stop_event
        self.mouse_movements = []
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
        pass

    def start(self):
        self.listener.start()
        while not self.stop_event.is_set():
            pass
        self.listener.stop()

    def get_listener(self):
        return self.listener

    def get_movements(self):
        return self.mouse_movements

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
                current_time = time.time()

                if pressed:
                    click_time = current_time
                    movement = {"mouse_clicked": (x, y), "time": click_time}
                else:
                    release_time = current_time
                    movement = {"mouse_released": (x, y), "time": release_time}
                
                self.mouse_movements.append(movement)
                
                # if button is Button.right:
                    # print('movements: ', self.mouse_movements)
                    # self.listener.stop()
                
                # print(button)

                return self.mouse_movements
            else:
                pass
        except:
            print('Erro ao salvar clique')
    
    def on_move(self, x, y):
        if self.stop_event.is_set():
            return

        try:
            if self.record_move is True:
                print('Pointer moved to {0}'.format(
                (x, y)))
                movement = {"mouse_moved": (x, y), "time": time.time()}
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
                movement = {"mouse_scroll": ((x, y), (dx, dy)), "time": time.time()}
                self.mouse_movements.append(movement)

                return self.mouse_movements
            else:
                pass
        except:
            print('Erro ao salvar scroll')
        