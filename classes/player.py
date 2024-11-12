import time
class player:
    def __init__(self, mouse_instance = None, keyboard_instance = None, control_instance = None):
        self.mouse_instance = mouse_instance
        self.keyboard_instance = keyboard_instance
        self.control_instance = control_instance
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

        if self.keyboard_instance is not None:
            key_inputs = self.keyboard_instance.remove_duplicate_presses(self.keyboard_instance.get_inputs())

        self.all_movements = clicks + movements + key_inputs
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

    def play_all_movements(self, actions_not_playable = []):
        self.sort_all_movements()
        self.split_by_checkpoint()

        for checkpoint in self.get_all_movements():
            print('checkpoint: ', checkpoint)
            for i, movement in enumerate(checkpoint):
                if i + 1 < len(checkpoint):
                    next_movement = checkpoint[i+1]

                keys = list(movement)
                values = list(movement.values())
                # print('keys', keys)

                skip = False

                for j in range(len(actions_not_playable)):
                    if keys[1] == actions_not_playable[j]:
                        skip = True
                        break

                if skip == True:
                    continue

                match values[0]:
                    case 'mouse':
                        match keys[1]:
                            case 'click':
                                self.mouse_instance.mouse_click(values[3])
                                print('click', values[3])

                            case 'release':
                                self.mouse_instance.mouse_release(values[3])
                                print('release', values[3])

                            case 'move':
                                self.mouse_instance.move_to(values[1])

                            case _:
                                print('Houve um erro ao reproduzir os movimentos do mouse')

                    case 'keyboard':
                        match keys[1]:
                            case 'press':
                                self.keyboard_instance.key_input(values[1])
                                print('press', values[1])

                            case 'release':
                                self.keyboard_instance.key_release(values[1])
                                print('release', values[1])

                            case _:
                                print('Houve um erro ao reproduzir os movimentos do teclado')

                    case _:
                        print('Houve um erro ao reproduzir os movimentos')
            
                if next_movement:
                    time_diff = next_movement['time'] - movement['time']
                    time.sleep(time_diff)

            self.control_instance.wait_for_confirm()
        
        # os._exit(1)
