from abc import ABC, abstractmethod
from Point import Point
from enum import Enum
import random
import logging

logging.basicConfig(filename='board_logs.txt', level=logging.INFO, format='%(message)s', filemode='w')


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

class Type_of_Animal(Enum):
    LAND = 0
    FLYING = 1
    WATER = 2


NUMBER_OF_TRIES = 15


class Animal(ABC):

    def __init__(self, kind_arg: str, hp_max_arg: int, hp_arg: int, speed_arg: int, attack_arg: int, defense_arg: int,
                 is_aggressive_arg: bool, level_arg: int, init_x: int, init_y: int, type_of_animal: Type_of_Animal,
                 rounds_without_fight: int = 2):
        self.kind = kind_arg
        self.hp_max = hp_max_arg
        self.hp = hp_arg
        self.speed = speed_arg
        self.attack = attack_arg
        self.defense = defense_arg
        self.IsAggressive = is_aggressive_arg
        self.level = level_arg
        self.position = Point(init_x, init_y)
        self.type_of_animal = type_of_animal
        self.rounds_without_fight = rounds_without_fight

    def change_position(self, new_x: int, new_y: int) -> bool:
        logging.info(f'{self.kind} moved from position {self.position.x + 1}, {self.position.y + 1} '
                     f'to {new_x + 1}, {new_y + 1}')
        self.position.x = new_x
        self.position.y = new_y
        return True

    def heal(self, percentage_of_heal: int = 10):
        if self.hp < self.hp_max and self.rounds_without_fight >= 2:
            heal = self.hp_max // percentage_of_heal
            self.hp += heal
            logging.info(f'{self.kind} has healed by {heal} HP, and now has {self.hp} HP')

    def chance_to_escape(self, attacker) -> bool:
        if self.speed > attacker.speed:
            chance_to_escape = (self.speed - attacker.speed) / 100
            if random.random() < chance_to_escape:
                logging.info(f'{self} escaped successfully from {attacker}')
                return True
            else:
                logging.info(f"{self} didn't escape from {attacker}")
                return False
        else:
            logging.info(f'{self} speed is lower than {attacker} speed, escape unsuccessful')
            return False

    def chance_for_attack(self) -> bool:
        if self.IsAggressive:
            chance_to_attack = random.randint(0, 1)
            if chance_to_attack == 1:
                return True
            else:
                logging.info(f"{self} attack unsuccessful ")
                return False
        else:
            logging.info(f"{self} didn't attack any animal because it is not aggressive")

    def attack_target(self, other) -> bool:
        if self.attack > other.defense:
            damage = self.attack - other.defense
        else:
            damage = 0

        self.rounds_without_fight = 0
        # Taking damage
        other.hp -= damage
        logging.info(f'{self} attacked {other} and dealt damage equal to {damage}')
        return True

    def hunt(self) -> bool:
        print(f"{self.kind} is hunting ")
        return True

    @abstractmethod
    def level_up(self):
        logging.info(f'{self.kind} has leveled up')

    @abstractmethod
    def make_sound(self):
        pass

    def __str__(self):
        # final_string = f'Kind: {self.kind}, HP: {self.hp}, Speed: {self.speed}, Attack: {self.attack}, ' \
        #                f'Defense: {self.defense}, Is Aggressive: {self.IsAggressive}, Level: {self.level}'
        final_string = f"{self.kind}, Lvl: {self.level} Hp: {self.hp}"
        return final_string

    def animal_information(self):
        final_string = f'Kind: {self.kind}, Max HP: {self.hp_max}, Current HP: {self.hp}, Speed: {self.speed},' \
                       f' Attack: {self.attack}, Defense: {self.defense}, Is Aggressive: {self.IsAggressive}, ' \
                       f'Level: {self.level}'
        return final_string


class Wolf(Animal):
    def __init__(self, hp_arg: int = 100, hp_max_arg: int = 100, speed_arg: int = 10, attack_arg: int = 30,
                 defense_arg: int = 20, level_arg: int = 1, is_aggressive_arg: bool = True, init_x: int = 0,
                 init_y: int = 0, type_of_animal: Type_of_Animal = Type_of_Animal.LAND):
        super().__init__("Wolf", hp_arg, hp_max_arg, speed_arg, attack_arg, defense_arg, is_aggressive_arg, level_arg,
                         init_x, init_y, type_of_animal)

    def make_sound(self) -> bool:
        print('Howl')
        return True

    def level_up(self) -> bool:
        self.level += 1
        self.hp_max += 5
        self.speed += 1
        self.attack += 5
        self.defense += 2
        return True


class Hare(Animal):
    def __init__(self, hp_arg: int = 30, hp_max_arg: int = 30, speed_arg: int = 30, attack_arg: int = 3,
                 defense_arg: int = 3, level_arg: int = 1, is_aggressive_arg: bool = False, init_x: int = 0,
                 init_y: int = 0, type_of_animal: Type_of_Animal = Type_of_Animal.LAND):
        super().__init__("Hare ", hp_arg, hp_max_arg, speed_arg, attack_arg, defense_arg, is_aggressive_arg, level_arg,
                         init_x, init_y, type_of_animal)

    def make_sound(self) -> bool:
        print('chirp-chirp')
        return True

    def level_up(self) -> bool:
        self.level += 1
        self.hp_max += 1
        self.speed += 3
        self.attack += 1
        self.defense += 1
        return True


class Bear(Animal):
    def __init__(self, hp_arg: int = 150, hp_max_arg: int = 150, speed_arg: int = 12, attack_arg: int = 40,
                 defense_arg: int = 30, level_arg: int = 1, is_aggressive_arg: bool = True, init_x: int = 0,
                 init_y: int = 0, type_of_animal: Type_of_Animal = Type_of_Animal.LAND):
        super().__init__("Bear", hp_arg, hp_max_arg, speed_arg, attack_arg, defense_arg, is_aggressive_arg, level_arg,
                         init_x, init_y, type_of_animal)

    def make_sound(self) -> bool:
        print('Roar')
        return True

    def level_up(self) -> bool:
        self.level += 1
        self.hp_max += 20
        self.speed += 1
        self.attack += 10
        self.defense += 10
        return True


class Cow(Animal):
    def __init__(self, hp_arg: int = 100, hp_max_arg: int = 100, speed_arg: int = 8, attack_arg: int = 6,
                 defense_arg: int = 10, level_arg: int = 1, is_aggressive_arg: bool = False, init_x: int = 0,
                 init_y: int = 0, type_of_animal: Type_of_Animal = Type_of_Animal.LAND):
        super().__init__("Cow", hp_arg, hp_max_arg, speed_arg, attack_arg, defense_arg, is_aggressive_arg, level_arg,
                         init_x, init_y, type_of_animal)

    def make_sound(self) -> bool:
        print('moo, moo')
        return True

    def level_up(self) -> bool:
        self.level += 1
        self.hp_max += 10
        self.speed += 1
        self.attack += 1
        self.defense += 1
        return True


class Bull(Animal):
    def __init__(self, hp_arg: int = 120, hp_max_arg: int = 120, speed_arg: int = 10, attack_arg: int = 20,
                 defense_arg: int = 20, level_arg: int = 1, is_aggressive_arg: bool = True, init_x: int = 0,
                 init_y: int = 0, type_of_animal: Type_of_Animal = Type_of_Animal.LAND):
        super().__init__("Bull", hp_arg, hp_max_arg, speed_arg, attack_arg, defense_arg, is_aggressive_arg, level_arg,
                         init_x, init_y, type_of_animal)

    def make_sound(self) -> bool:
        print('bellow')
        return True

    def level_up(self) -> bool:
        self.level += 1
        self.hp_max += 15
        self.speed += 1
        self.attack += 7
        self.defense += 5
        return True


class Sheep(Animal):
    def __init__(self, hp_arg: int = 70, hp_max_arg: int = 70, speed_arg: int = 8, attack_arg: int = 7,
                 defense_arg: int = 10, level_arg: int = 1, is_aggressive_arg: bool = False, init_x: int = 0,
                 init_y: int = 0, type_of_animal: Type_of_Animal = Type_of_Animal.LAND):
        super().__init__("Sheep", hp_arg, hp_max_arg, speed_arg, attack_arg, defense_arg, is_aggressive_arg, level_arg,
                         init_x, init_y, type_of_animal)

    def make_sound(self) -> bool:
        print('baa, baa')
        return True

    def level_up(self) -> bool:
        self.level += 1
        self.hp_max += 5
        self.speed += 2
        self.attack += 1
        self.defense += 1
        return True


class Bird(Animal, ABC):
    def __init__(self, kind_arg: str, hp_max: int, hp_arg: int, speed_arg: int, attack_arg: int, defense_arg: int,
                 level_arg: int, is_aggressive_arg: bool, init_x: int = 0, init_y: int = 0,
                 type_of_animal: Type_of_Animal = Type_of_Animal.FLYING):
        super().__init__(kind_arg, hp_max, hp_arg, speed_arg, attack_arg, defense_arg, is_aggressive_arg, level_arg,
                         init_x, init_y, type_of_animal)

    def fly_away(self, new_x, new_y) -> bool:
        print(f'{self.kind} flew away to the field {new_x}, {new_y}')
        return True

    def land(self, spot):
        print(f'{self.kind}, has landed on the {spot}')
        return True


class Eagle(Bird):
    def __init__(self, hp_arg: int = 70, hp_max: int = 70, speed_arg: int = 50, attack_arg: int = 15,
                 defense_arg: int = 15, level_arg: int = 1, is_aggressive_arg: bool = True, init_x: int = 0,
                 init_y: int = 0, type_of_animal: Type_of_Animal = Type_of_Animal.FLYING):
        super().__init__('Eagle', hp_arg, hp_max, speed_arg, attack_arg, defense_arg, level_arg, is_aggressive_arg,
                         init_x, init_y, type_of_animal)

    def level_up(self) -> bool:
        self.level += 1
        self.hp_max += 5
        self.speed += 10
        self.attack += 5
        self.defense += 2
        return True

    def make_sound(self) -> bool:
        print('Piercing screech')
        return True

    def powerful_strike(self, target):
        print(f"{self.kind} strong grasp {target} with the powerful talons")


class Owl(Bird):
    def __init__(self, hp_arg: int = 30, hp_max: int = 30, speed_arg: int = 25, attack_arg: int = 8,
                 defense_arg: int = 10, level_arg: int = 1, is_aggressive_arg: bool = True, init_x: int = 0,
                 init_y: int = 0, type_of_animal: Type_of_Animal = Type_of_Animal.FLYING):
        super().__init__('Owl', hp_arg, hp_max, speed_arg, attack_arg, defense_arg, level_arg, is_aggressive_arg,
                         init_x, init_y, type_of_animal)

    def level_up(self) -> bool:
        self.level += 1
        self.hp_max += 3
        self.speed += 6
        self.attack += 2
        self.defense += 2
        return True

    def make_sound(self) -> bool:
        print('hoot')
        return True

    def night_vision(self) -> bool:
        print(f'{self.kind} turns on vision in the dark')
        return True


class Vulture(Bird):
    def __init__(self, hp_arg: int = 50, hp_max: int = 50, speed_arg: int = 30, attack_arg: int = 12,
                 defense_arg: int = 12, level_arg: int = 1, is_aggressive_arg: bool = True, init_x: int = 0,
                 init_y: int = 0, type_of_animal: Type_of_Animal = Type_of_Animal.FLYING):
        super().__init__('Vulture', hp_arg, hp_max, speed_arg, attack_arg, defense_arg, level_arg,
                         is_aggressive_arg, init_x, init_y, type_of_animal)

    def level_up(self) -> bool:
        self.level += 1
        self.hp_max += 4
        self.speed += 8
        self.attack += 4
        self.defense += 3
        return True

    def make_sound(self) -> bool:
        return False


class Fish(Animal, ABC):
    def __init__(self, kind_arg: str, hp_max: int, hp_arg: int, speed_arg: int, attack_arg: int, defense_arg: int,
                 level_arg: int, is_aggressive_arg: bool, init_x: int = 0, init_y: int = 0,
                 type_of_animal: Type_of_Animal = Type_of_Animal.WATER):
        super().__init__(kind_arg, hp_max, hp_arg, speed_arg, attack_arg, defense_arg, is_aggressive_arg, level_arg,
                         init_x, init_y, type_of_animal)


class Shark(Fish):
    def __init__(self, hp_arg: int = 150, hp_max: int = 150, speed_arg: int = 35, attack_arg: int = 30,
                 defense_arg: int = 20, level_arg: int = 1, is_aggressive_arg: bool = True, init_x: int = 0,
                 init_y: int = 0, type_of_animal: Type_of_Animal = Type_of_Animal.WATER):
        super().__init__('Shark', hp_arg, hp_max, speed_arg, attack_arg, defense_arg, level_arg,
                         is_aggressive_arg, init_x, init_y, type_of_animal)

    def level_up(self) -> bool:
        self.level += 1
        self.hp_max += 10
        self.speed += 5
        self.attack += 8
        self.defense += 4
        return True

    def make_sound(self) -> bool:
        return False


class Dolphin(Fish):
    def __init__(self, hp_arg: int = 100, hp_max: int = 100, speed_arg: int = 35, attack_arg: int = 10,
                 defense_arg: int = 10, level_arg: int = 1, is_aggressive_arg: bool = False, init_x: int = 0,
                 init_y: int = 0, type_of_animal: Type_of_Animal = Type_of_Animal.WATER):
        super().__init__('Dolphin', hp_arg, hp_max, speed_arg, attack_arg, defense_arg, level_arg,
                         is_aggressive_arg, init_x, init_y, type_of_animal)

    def level_up(self) -> bool:
        self.level += 1
        self.hp_max += 10
        self.speed += 5
        self.attack += 3
        self.defense += 4
        return True

    def make_sound(self) -> bool:
        print('Ee-ee-ee-ee-ek! ')
        return True


class Sea_Turtle(Fish):
    def __init__(self, hp_arg: int = 200, hp_max: int = 200, speed_arg: int = 5, attack_arg: int = 5,
                 defense_arg: int = 40, level_arg: int = 1, is_aggressive_arg: bool = False, init_x: int = 0,
                 init_y: int = 0, type_of_animal: Type_of_Animal = Type_of_Animal.WATER):
        super().__init__('Sea Turtle', hp_arg, hp_max, speed_arg, attack_arg, defense_arg, level_arg,
                         is_aggressive_arg, init_x, init_y, type_of_animal)

    def level_up(self) -> bool:
        self.level += 1
        self.hp_max += 15
        self.speed += 2
        self.attack += 2
        self.defense += 5
        return True

    def make_sound(self) -> bool:
        print('Ee-ee-ee-ee-ek! ')
        return True


if __name__ == "__main__":
    wolf_01 = Wolf(100, 30, 30, 25, 10)
    wolf_02 = Wolf(120, 30, 35, 30, 15)
    print(wolf_01)
    wolf_01.level_up()
    print(wolf_01)
    wolf_01.position.x = 1

    shark_01 = Shark()
    print(shark_01)

    wolf_01.position.y = 1
    wolf_01.change_position(2, 3)
    owl_01 = Owl()
    print(type(wolf_01.type_of_animal.name))
    print(owl_01.type_of_animal)
