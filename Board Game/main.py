from typing import List, Union
from Animals import *
from enum import Enum
import random
import logging

logging.basicConfig(filename='board_logs.txt', level=logging.INFO, format='%(message)s', filemode='w')

NUMBER_OF_TRIES = 15


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


class Board:
    def __init__(self, list_of_animals: List, board_size: int = 50):
        self.size = board_size
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.list_of_animals = list_of_animals
        self.instances = []

    def init_simulation(self, amount: int) -> bool:
        if amount <= self.size ** 2:
            logging.info(f'Preparing for the game, board size: {self.size ** 2} '
                         '\nPositioning of animals on the board:')
            # Randomize the animal
            for i in range(amount):
                random_animal = random.choice(self.list_of_animals)

                counter = 0
                while counter < NUMBER_OF_TRIES:
                    # Randomize the row and column
                    random_row_idx = random.randint(0, self.size - 1)
                    random_col_idx = random.randint(0, self.size - 1)

                    # Setting the animals on the board
                    if self.board[random_row_idx][random_col_idx] is None:
                        new_instance = random_animal(init_x=random_row_idx, init_y=random_col_idx)
                        self.board[random_row_idx][random_col_idx] = new_instance
                        self.instances.append(new_instance)
                        logging.info(f'{new_instance} has appeared on '
                                     f'field x = {random_row_idx + 1}, y = {random_col_idx + 1}')
                        break

                    counter += 1
            return True
        else:
            print('Error, amount of animals is greater than the size of the board')
            return False

    def find_animal_by_position(self, x: int, y: int) -> Union[Animal, None]:
        for animal in self.instances:
            if animal.position.x == x and animal.position.y == y:
                return animal
        return None

    def get_free_fields(self, animal: Animal):
        free_fields = []
        x = animal.position.x
        y = animal.position.y

        if y > 0 and self.board[x][y - 1] is None:
            free_fields.append((x, y - 1))
        elif y < self.size - 1 and self.board[x][y + 1] is None:
            free_fields.append((x, y + 1))
        elif x < self.size - 1 and self.board[x + 1][y] is None:
            free_fields.append((x + 1, y))
        elif x > 0 and self.board[x - 1][y] is None:
            free_fields.append((x - 1, y))

        return free_fields

    def get_neighbours(self, animal: Animal) -> List[Union[Animal, None]]:
        neighbours = []
        x = animal.position.x
        y = animal.position.y

        if y > 0 and self.board[x][y - 1] is not None:
            result = self.find_animal_by_position(x, y - 1)
            neighbours.append(result)
        elif y < self.size - 1 and self.board[x][y + 1] is not None:
            result = self.find_animal_by_position(x, y + 1)
            neighbours.append(result)
        elif x < self.size - 1 and self.board[x + 1][y] is not None:
            result = self.find_animal_by_position(x + 1, y)
            neighbours.append(result)
        elif x > 0 and self.board[x - 1][y] is not None:
            result = self.find_animal_by_position(x - 1, y)
            neighbours.append(result)

        return neighbours

    def delete_animal(self, animal: Animal):
        self.instances.remove(animal)
        self.board[animal.position.x][animal.position.y] = None

    def is_valid_position(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def move_animal(self, animal, new_x, new_y):
        self.board[animal.position.x][animal.position.y] = None
        animal.change_position(new_x, new_y)
        self.board[new_x][new_y] = animal

    def animals_fight(self, attacker, defender):
        attacker.attack_target(defender)  # Attack
        if defender.hp <= 0:
            logging.info(f'{defender} has been defeated by {attacker}')
            attacker.level_up()
            self.delete_animal(defender)
        else:
            defender.attack_target(attacker)  # Counterattack
            if attacker.hp <= 0:
                logging.info(f'{attacker} has been defeated by {defender}')
                defender.level_up()
                self.delete_animal(attacker)

    def next_round(self):
        # Take those animals which are on board
        move_counter = 1
        random.shuffle(self.instances)
        for animal in self.instances:
            move_successful = False

            # Setting new position
            for _ in range(NUMBER_OF_TRIES):
                direction = random.randint(0, 3)
                new_x, new_y = animal.position.x, animal.position.y
                if direction == Direction.LEFT.value and animal.position.y > 0:
                    new_y -= 1
                elif direction == Direction.RIGHT.value and animal.position.y < self.size - 1:
                    new_y += 1
                elif direction == Direction.UP.value and animal.position.x < self.size - 1:
                    new_x += 1
                elif direction == Direction.DOWN.value and animal.position.x > 0:
                    new_x -= 1

                # Moving the animal on the board
                if self.is_valid_position(new_x, new_y) and self.board[new_x][new_y] is None:
                    logging.info(f'-' * 100)
                    logging.info(f'Move on the board: {move_counter}, Animal: {animal}, '
                                 f'Position: {animal.position.x + 1}, {animal.position.y + 1}')
                    self.move_animal(animal, new_x, new_y)
                    animal.heal()
                    animal.level_up()

                    # Animal attack
                    if animal.chance_for_attack():
                        neighbours = self.get_neighbours(animal)
                        # Choosing an animal to attack
                        if neighbours:
                            chosen_animal_idx = random.randint(0, len(neighbours) - 1)
                            animal_under_attack = neighbours[chosen_animal_idx]
                            # Get free fields for animal under attack
                            free_fields = self.get_free_fields(animal_under_attack)
                            # A scenario in which a land animal attacks a flying one
                            if animal.type_of_animal.name == 'LAND' and \
                                    animal_under_attack.type_of_animal.name == 'FLYING' and free_fields:
                                chosen_free_field_idx = random.randint(0, len(free_fields) - 1)
                                x, y = free_fields[chosen_free_field_idx]
                                self.move_animal(animal_under_attack, x, y)
                                animal_under_attack.rounds_without_fight += 1
                            else:
                                if animal_under_attack.chance_to_escape(animal) and free_fields:
                                    chosen_free_field_idx = random.randint(0, len(free_fields) - 1)
                                    x, y = free_fields[chosen_free_field_idx]
                                    self.move_animal(animal_under_attack, x, y)
                                    animal_under_attack.rounds_without_fight += 1
                                else:
                                    self.animals_fight(animal, animal_under_attack)

                    logging.info(f'End of move: {move_counter}, Animal: {animal}')
                    logging.info(f'-' * 100)
                    move_successful = True
                    move_counter += 1
                    break

            if not move_successful:
                logging.info(f'-' * 100)
                logging.info(f'Move on the board: {move_counter}, '
                             f'Animal: {animal}, Position: {animal.position.x + 1}, {animal.position.y + 1}')
                logging.info(f'{animal} remains in place, too many attempts')
                logging.info(f'End of move: {move_counter}, Animal: {animal}')
                logging.info(f'-' * 100)
                move_counter += 1

    def sum_up(self):
        try:
            num_of_animals = len(self.instances)
            highest_level = max(animal.level for animal in self.instances)
            lowest_level = min(animal.level for animal in self.instances)

            # Printing number of animals on board
            print(f'\nNumber of animals on board: {num_of_animals}\n')
            logging.info('\n' + 40 * '-' + 'Statistics after game' + 40 * '-')
            logging.info(f'Number of animals on board: {num_of_animals}\n')
            if highest_level == lowest_level:
                highest_level_animals = [animal for animal in self.instances if animal.level == highest_level]
                string = 'Highest level animals: \n'
                for animal in highest_level_animals:
                    string += str(animal) + '\n'
                print(string)
                logging.info(string)
            else:
                highest_level_animals = [animal for animal in self.instances if animal.level == highest_level]
                lowest_level_animals = [animal for animal in self.instances if animal.level == lowest_level]
                highest_string = 'Highest level animals: \n'
                for animal in highest_level_animals:
                    highest_string += animal.animal_information() + '\n'

                print(highest_string)
                logging.info(highest_string)

                lowest_string = 'Lowest level animals: \n'
                for animal in lowest_level_animals:
                    lowest_string += animal.animal_information() + '\n'
                print(lowest_string)
                logging.info(lowest_string)

            # Counting number of species
            species_counts = {}
            for animal in self.instances:
                if animal.kind in species_counts:
                    species_counts[animal.kind] += 1
                else:
                    species_counts[animal.kind] = 1
            print('Species count:')
            logging.info('Species count:')
            for species, count in species_counts.items():
                if count == 1:
                    print(f"{species}: {count} animal")
                    logging.info(f"{species}: {count} animal")
                else:
                    print(f"{species}: {count} animals")
                    logging.info(f"{species}: {count} animals")

        except ValueError:
            print('No animals on the board! ')
            logging.info('No animals on the board! ')

    def __str__(self):
        final_str = '   '
        for j in range(1, self.size + 1):
            distance = 28 - len(str(j))
            left_distance = ' ' * (distance // 2)
            right_distance = ' ' * (distance - (distance // 2))
            final_str += f'{left_distance}{str(j)}.{right_distance}'
        final_str += '\n'

        for i, row in enumerate(self.board, start=1):
            final_str += f'{i}.|'
            for k, col in enumerate(row, start=1):
                distance = 28 - len(str(col))
                left_distance = ' ' * (distance // 2)
                right_distance = ' ' * (distance - (distance // 2))
                final_str += f'{left_distance}{str(col)}{right_distance}|'
            final_str += '\n'
        return final_str


if __name__ == "__main__":
    animals_list = [Wolf, Hare, Bear, Cow, Bull, Sheep, Eagle, Owl, Vulture]
    round_counter = 1
    size = int(input('Enter the size of board: '))
    board_01 = Board(animals_list, size)
    numbers_of_animals = int(
        input(f'Enter the number of animals on the board cannot be more or equal than {size * size}: '))
    if numbers_of_animals >= size * size:
        print('Wrong numbers of animals')
    else:
        board_01.init_simulation(numbers_of_animals)

        choice = None
        print('\nArrangement of animals on the board:\n', board_01)
        while choice != 4:

            print('What do you want to do?')
            print('1. Next round')
            print('2. View animal information')
            print('3. Simulate several rounds')
            print('4. End game')
            try:
                choice = int(input('Choose number:'))
            except ValueError:
                print('You must enter a number.')
            if choice == 1:
                logging.info(f"\nRound {round_counter}: Starting new round")
                board_01.next_round()
                print(f'\nRound: {round_counter}\n', board_01)
                logging.info(f'Round {round_counter}: End of the round')
                logging.info(f'-' * 100)
                round_counter += 1
            elif choice == 2:
                x = int(input('Specify the row-coordinate: '))
                y = int(input('Specify the column-coordinate: '))
                animal_sought = Board.find_animal_by_position(board_01, x - 1, y - 1)
                if animal_sought is not None:
                    print('-' * 120)
                    print(animal_sought.animal_information())
                    print('-' * 120)
                else:
                    print('Wrong coordinates, try again !')
            elif choice == 3:
                num_of_rounds = int(input('How many rounds you want to simulate? :'))
                for _ in range(num_of_rounds):
                    logging.info(f"\nRound {round_counter}: Starting new round")
                    board_01.next_round()
                    print(f'\nRound: {round_counter}\n', board_01)
                    logging.info(f'Round {round_counter}: End of the round')
                    logging.info(f'-' * 100)
                    round_counter += 1

            elif choice == 4:
                board_01.sum_up()
                break
