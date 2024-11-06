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
            self.print_all_movements()

            temp_array = []
            checkpoint_found = False

            for i, movement in enumerate(self.all_movements):
                # Verifica se o movimento é de um checkpoint com release
                if movement['device'] == 'checkpoint' and 'release' in movement:
                    # Se encontrar o checkpoint, divide a lista até esse ponto
                    temp_array = self.all_movements[:i + 1]  # Inclui o checkpoint de release
                    self.all_movements = self.all_movements[i + 1:]  # Restante da lista após o checkpoint
                    hold_array.append(temp_array)  # Adiciona a parte à lista de partes
                    checkpoint_found = True
                    break

            if not checkpoint_found:
                # Se não encontrar mais nenhum checkpoint, adiciona o restante dos movimentos
                hold_array.append(self.all_movements)
                self.all_movements = []  # Limpa a lista para terminar o loop

        self.set_all_movements(hold_array)
        print('\nall movements final: ', hold_array)
