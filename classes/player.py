class player:
    def __init__(self, mouse_instance = None, keyboard_instance = None):
        self.mouse_instance = mouse_instance
        self.keyboard_instance = keyboard_instance
        self.all_movements = []

    def __str__(self):
        pass

    def get_all_movements(self):
        return self.all_movements
    
    def set_all_movements(self, array):
        self.all_movements = array

    def print_all_movements(self):
        print(self.all_movements)

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

        self.all_movements = clicks + movements + scrolls + key_inputs
        self.all_movements.sort(key=lambda x: x['time'])

        return self.all_movements
        
    def split_by_checkpoint(self):
        hold_array = []

        while self.all_movements:
            temp_array = []
            checkpoint_found = False

            for i, movement in enumerate(self.all_movements):
                if movement['device'] == 'checkpoint' and 'release' in movement:
                    temp_array = self.all_movements[:i - 1]

                    self.all_movements = self.all_movements[i + 1:]

                    hold_array.append(temp_array)

                    checkpoint_found = True

                    break

            if not checkpoint_found:
                hold_array.append(self.all_movements)
                self.all_movements = []

        self.set_all_movements(hold_array)
        self.print_all_movements()

    def play_all_movements(self):
        self.sort_all_movements()

        self.split_by_checkpoint()

        for checkpoint in self.get_all_movements():
            for movement in checkpoint:
                keys = list(movement)
                values = list(movement.values())
                match values[0]:
                    case 'mouse':
                        match keys[1]:
                            case 'click':
                                pass # Ajustar lógica de repetir o click aqui

                            case 'release':
                                pass # Ajustar lógica de repetir o release do click aqui

                            case 'move':
                                pass # Ajustar lógica de repetir o movimento do mouse aqui

                            case 'scroll':
                                pass # Ajustar lógica de repetir o scroll aqui

                            case _:
                                print('Houve um erro ao reproduzir os movimentos')

                    case 'keyboard':
                        match keys[1]:
                            case 'press':
                                pass # Ajustar lógica de repetir a tecla pressionada aqui

                            case 'release':
                                pass # Ajustar lógica de repetir o release da tecla aqui

                            case _:
                                print('Houve um erro ao reproduzir os movimentos')

                    case _:
                        print('Houve um erro ao reproduzir os movimentos')
    
    def play_movements_except(self, types):
        self.sort_all_movements()
        
        self.split_by_checkpoint()
        for movement in self.get_all_movements():
            for movement_type in types:
                if movement_type in movement:
                    pass
                else:
                    pass # Continuar aqui
