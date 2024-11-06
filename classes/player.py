class player:
    def __init__(self, mouse_instance = None, keyboard_instance = None):
        self.mouse_instance = mouse_instance
        self.keyboard_instance = keyboard_instance

    def __str__(self):
        pass

    def sort_all_movements(self):
        if self.mouse_instance is None and self.keyboard_instance is None:
            print("Nenhum movimento realizado")
            return None

        if self.mouse_instance is not None:
            clicks = self.mouse_instance.get_clicks()
            movements = self.mouse_instance.get_movements()
            scrolls = self.mouse_instance.get_scrolls()

        if self.keyboard_instance is not None:
            key_inputs = self.keyboard_instance.remove_duplicate_presses(self.keyboard_instance.get_inputs())

        all_movements = clicks + movements + scrolls + key_inputs
        all_movements.sort(key=lambda x: x['time'])

        return all_movements
        
    def play_movements(self, movements):
        for movement in movements:
            pass
        