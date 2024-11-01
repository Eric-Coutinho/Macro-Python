from pynput import mouse as ms
import time

from pynput.mouse import Controller, Button

class mouse:
    def move_to(self, x, y):
        self.controller.position = (x, y)

    def on_click(self, x, y, button, pressed):
        try:
            current_time = time.time()

            if pressed:
                click_time = current_time
                movement = {"mouse_clicked": (x, y), "time": click_time}
            else:
                release_time = current_time
                movement = {"mouse_released": (x, y), "time": release_time}
            
            print(movement)
            return

        except:
            print('Botão inválido')
    
    def on_move(self, x, y):
        print('Pointer moved to {0}'.format(
        (x, y)))
        return {"mouse_moved": (x, y), "time": time.time()}
        

    def on_scroll(x, y, dx, dy):
        return {"mouse_scroll": ((x, y), (dx, dy)), "time": time.time()}
    

    def __init__(self):
        self.controller = Controller()
        self.listener = ms.Listener(
            on_move = self.on_move,
            on_click = self.on_click,
            on_scroll = self.on_scroll
        )
        self.listener.start()
        self.listener.join()
    
    def __str__(self):
        pass