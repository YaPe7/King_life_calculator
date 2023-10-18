import sys
import os
import time
from colorama import Fore, Back, Style
from random import randint
import csv


class King:
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.age = kwargs["age"]
        self.age_when_dying = kwargs["age_when_dying"]
        self.death_chance = kwargs["death_chance"]
        self.increasing_chance = kwargs["increasing_chance"]

    def __str__(self):
        return f"name = {self.name}, age = {self.age} years, when_dying = {self.age_when_dying} years, death_chance = {self.death_chance}%"


class Menu:
    is_king_chosen = False
    @classmethod
    def main_menu(cls):
        print("Menu. 1 - Create a King, 2 - Choose the King, 3 - Clear kings, 4 - Exit")
        decision = input("Option: ")
        if decision == "1":
            return cls.create_king()
        elif decision == "2":
            return cls.find_king()
        elif decision == "3":
            print("Are you sure? There is no way to backup data in this version.")
            confirm = True if input("y/n: ") == "y" else False
            if confirm:
                KingCSVManager.clear_file()
        elif decision == "4":
            raise KeyboardInterrupt
        else:
            print("Invalid command.")
        return cls.main_menu()

    @classmethod
    def create_king(cls) -> King:
        while True:
            name = input("A King's name: ")
            try:
                age = int(input("A King's age: "))
            except ValueError:
                print("Invalid age. Cancel command?")
                cancel = input("y/n: ")
                if cancel == 'y':
                    return Menu.main_menu()
                else:
                    continue
            try:
                age_when_dying = int(input("When the King is starting to die? Skip if nothing (Default: 50 years): "))
            except ValueError:
                age_when_dying = 50

            try:
                death_chance = int(input("Death chance? Skip if nothing (Default: 10%)"))
            except ValueError:
                death_chance = 10

            try:
                increasing_chance = int(input("How much will increase chance to die for a king? Skip if nothing. (Def: 5%)"))
            except ValueError:
                increasing_chance = 5
            return King(name=name, age_when_dying=age_when_dying, age=age, death_chance=death_chance, increasing_chance=increasing_chance)

    @classmethod
    def find_king(cls):
        while True:
            print("Please, write the name of a king or a part of it.")
            name = input("Name or part: ")
            list_kings = KingCSVManager.find_king(name)
            print(f"were found {len(list_kings)} kings:")

            for i in range(len(list_kings)):
                str_king = f"id {i} || {list_kings[i]}"
                print(str_king)
                print(len(str_king) * "=")

            choose_king = input("Choose a number of a king or skip to return back: ")
            try:
                choose_king = int(choose_king)
                result = list_kings[choose_king]

            except [ValueError, IndexError]:
                print("Invalid request.")
                return cls.main_menu()
            return result


class KingCSVManager:
    file = "kings.csv"
    if not os.path.exists(file):
        with open(file, "w") as king_csv:
            print("File created.")

    @classmethod
    def find_king(cls, name) -> list:
        king_list = []
        with open(cls.file, "r", newline='') as king_csv:
            king_reader = csv.reader(king_csv, delimiter=';')
            for l in king_reader:
                print(l)
                if name in l[0]:
                    king_list.append(King(name=l[0], age=l[1], age_when_dying=l[2], death_chance=l[3], increasing_chance=l[4]))
        return king_list




    @classmethod
    def save_king(cls, king: King):
        with open(cls.file, "a", newline='') as king_csv:
            king_writer = csv.writer(king_csv, delimiter=';')
            king_writer.writerow([king.name, king.age, king.age_when_dying, king.death_chance, king.increasing_chance])

    @classmethod
    def clear_file(cls):
        file = open(cls.file, "w")
        file.close()
        print("File cleared.")




def main():
    while True:
        king = Menu.main_menu()
        print(king)
        KingCSVManager.save_king(king)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Data saved")
        sys.exit()