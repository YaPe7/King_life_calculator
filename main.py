import sys
import os
import time
from colorama import Fore, Back, Style
from random import randint
import csv
import shutil
from tempfile import NamedTemporaryFile


class King:
    def __init__(self, died=False, **kwargs):
        self.name = kwargs["name"]
        self._died = died
        self.age = int(kwargs["age"])
        self.age_when_dying = int(kwargs["age_when_dying"])
        self.death_chance = int(kwargs["death_chance"])
        self.increasing_chance = int(kwargs["increasing_chance"])

    def grew_up(self):
        if not self._died:
            self.age += 1

    def king_to_dict(self):
        return  {
            "name": self.name,
            "age": self.age,
            "age_when_dying": self.age_when_dying,
            "death_chance": self.death_chance,
            "increasing_chance": self.increasing_chance
        }

    def __str__(self):
        return f"name = {self.name}, age = {self.age} years, when_dying = {self.age_when_dying} years, death_chance = {self.death_chance}%, {'DIED' if self._died else 'Alive'}"


class Menu:
    is_king_chosen = False

    @classmethod
    def main_menu(cls):
        print("Menu. 1 - Create a King, 2 - Choose the King, 3 - Clear kings, 4 - Exit")
        decision = input("Option: ")
        if decision == "1":
            return cls.create_king()
        elif decision == "2":
            king = cls.find_king()

            return king
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
                death_chance = int(input("Death chance? Skip if nothing (Default: 10%): "))
            except ValueError:
                death_chance = 10

            try:
                increasing_chance = int(input("How much will increase chance to die for a king? Skip if nothing. (Def: 5%): "))
            except ValueError:
                increasing_chance = 5
            return King(name=name, age_when_dying=age_when_dying, age=age, death_chance=death_chance, increasing_chance=increasing_chance)

    @classmethod
    def find_king(cls):
        while True:
            print("Please, write the name of a king or a part of it.")
            name = input("Name or part: ")
            list_kings = KingCSVManager.find_king(name) or False
            if not list_kings:
                print("The King who you're looking for doesn't exist...")
                return cls.main_menu()
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


    def edit_king(self, king: King):
        king_dict = king.king_to_dict()
        for key, value in king_dict.items():
            print(f"Change {key}?")
            decision = input("y/n: ")
            if decision == 'y':
                new_value = input("Input new value: ")
                king_dict[key] = new_value





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
                if name in l[0]:
                    king_list.append(King(name=l[0], age=l[1], age_when_dying=l[2], death_chance=l[3], increasing_chance=l[4]))
        return king_list

    @classmethod
    def save_king(cls, king: King):
        info_to_write = (king.name, king.age, king.age_when_dying, king.death_chance, king.increasing_chance, king._died)
        king = cls.find_king(king.name) or False

        if not king:
            with open(cls.file, "a", newline='') as king_csv:
                king_writer = csv.writer(king_csv, delimiter=';')
                king_writer.writerow(info_to_write)
                print("King was written. It will be saved after exiting program")
        else:
            temp_csv = NamedTemporaryFile(mode="w", delete=False)
            with open(cls.file) as king_csv, temp_csv:
                reader = csv.reader(king_csv, delimiter=";")
                writer = csv.writer(temp_csv, delimiter=";")
                for line in reader:
                    print(line[0], king[0])
                    if line[0] == king[0].name:
                        writer.writerow(info_to_write)
                        print("Information about king was updated")
            shutil.move(temp_csv.name, cls.file)

    @classmethod
    def clear_file(cls):
        file = open(cls.file, "w").close()
        print("File cleared.")


def main():
    while True:
        try:
            king = Menu.main_menu()
        except ValueError:
            print("Error when creating object of a King")
            continue
        print(king)
        KingCSVManager.save_king(king)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Goodbye!")
        sys.exit()