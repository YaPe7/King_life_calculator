import sys
import time
from colorama import Fore, Back, Style
from random import randint
import csv


class King:
    def __init__(self, age, age_when_dying=50, death_chance=10, increasing_chance=10):
        self.age = age
        self.age_when_dying = age_when_dying
        self.death_chance = death_chance
        self.increasing_chance = increasing_chance


class Menu:
    is_king_chosen = False
    @classmethod
    def main_menu(cls):
        while True:
            print("Menu. 1 - Create a King, 2 - Choose the King, 3 - Exit")
            decision = input("Option: ")
            if decision == "1":
                cls.create_king()
            elif decision == "2":
                cls.find_king()
            elif decision == "3":
                raise KeyboardInterrupt
            else:
                print("Invalid command.")
                time.sleep(1)

    @classmethod
    def create_king(cls):
        pass


    @classmethod
    def find_king(cls):
        pass

def main():
    pass



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Data saved")
        sys.exit()