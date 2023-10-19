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
        try:
            self.age = int(kwargs["age"])
            self.age_when_dying = int(kwargs["age_when_dying"])
            self.death_chance = int(kwargs["death_chance"])
            self.increasing_chance = int(kwargs["increasing_chance"])
        except ValueError:
            raise ValueError("Error when creating a king.")

    @property
    def info_to_write(self):
        return self.name, self.age, self.age_when_dying, self.death_chance, self.increasing_chance, self._died

    def count_death(self):
        if not self.age >= self.age_when_dying:
            return True
        death_num = randint(1, 100)
        if death_num <= self.death_chance:
            self._died = True
            return False
        self.death_chance += self.increasing_chance
        return True

    def grew_up(self):
        if not self._died:
            self.age += 1
            is_live = self.count_death()
            if not is_live:
                print(f"{self.name} has died at the age of {self.age}...")
            else:
                return True
        else:
            print("King is dead. Game over.")
        return False

    def king_to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "age_when_dying": self.age_when_dying,
            "death_chance": self.death_chance,
            "increasing_chance": self.increasing_chance,
        }

    def __str__(self):
        return f"name = {self.name}, age = {self.age} years, when_dying = {self.age_when_dying} years, death_chance = {self.death_chance}%, {'DEAD' if self._died else 'ALIVE'}"


class Menu:
    is_king_chosen = False

    @classmethod
    def main_menu(cls):
        print("Menu. 1 - Create a King, 2 - Choose the King, 3 - Clear kings, 4 - Delete the King, 5 - Exit")
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
            king = cls.find_king()
            KingCSVManager.delete_king(king)

        elif decision == "5":
            raise KeyboardInterrupt
        else:
            print("Invalid command.")
        return cls.main_menu()

    @classmethod
    def create_king(cls) -> King | None:
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
            king = King(name=name, age_when_dying=age_when_dying, age=age, death_chance=death_chance, increasing_chance=increasing_chance)
            print(f"Do you want to save? {king}")
            decision = input("y/n: ")
            if decision == "y":
                return king

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

            except Exception:
                print("Invalid request.")
                return cls.main_menu()
            return result

    @classmethod
    def edit_king(cls, king: King):
        king_dict = king.king_to_dict()
        for key, value in king_dict.items():
            print(f"Change {key}?")
            decision = input("y/n: ")
            if decision == 'y':
                new_value = input("Input new value: ")
                king_dict[key] = new_value
        return King(**king_dict)


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
                if l and name.lower().strip() in l[0].strip().lower() or name == "any":
                    l[5] = False if l[5] == "False" else True
                    king_list.append(King(name=l[0], age=l[1], age_when_dying=l[2], death_chance=l[3], increasing_chance=l[4], died=l[5]))
        return king_list

    @classmethod
    def _manipulate_king_info(cls, king: King, info_to_write=False, delete=False):
        temp_csv = NamedTemporaryFile(mode="w", delete=False, encoding="utf-8")
        with open(cls.file, "r", newline='') as king_csv, temp_csv:
            reader = csv.reader(king_csv, delimiter=";")
            writer = csv.writer(temp_csv, delimiter=";")
            for line in reader:
                if not (line and line[0] == king.name):
                    print("Line is written")
                    writer.writerow(line)
                    continue
                if not delete:
                    print(king.info_to_write)
                    writer.writerow(info_to_write)
                    print("Information about king was updated")
                    continue
                print("King was deleted.")
        shutil.move(temp_csv.name, cls.file)

    @classmethod
    def save_king(cls, king: King):
        info_to_write = king.info_to_write
        king = cls.find_king(king.name) or False

        if not king:
            with open(cls.file, "a", newline='', encoding="utf-8") as king_csv:
                king_writer = csv.writer(king_csv, delimiter=';')
                king_writer.writerow(info_to_write)
                print("King was written. It will be saved after exiting program")
        else:
            cls._manipulate_king_info(king[0], info_to_write)

    @classmethod
    def delete_king(cls, king: King):
        cls._manipulate_king_info(king, delete=True)

    @classmethod
    def clear_file(cls):
        open(cls.file, "w").close()
        print("File cleared.")


def main():
    while True:
        king = Menu.main_menu()
        if king is None:
            print("Aborted.")
            continue
        while True:
            print(king)
            print("What to do next? 1 - Change king, 2 - Live 1 year, 3 - Abort")
            decision = input(": ")
            if decision == '1':
                king = Menu.edit_king(king)
            elif decision == '2':
                result = king.grew_up()
                KingCSVManager.save_king(king)
                if not result:
                    break
            else:
                KingCSVManager.save_king(king)
                break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Goodbye!")
        sys.exit()