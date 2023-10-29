import sys
from king import King
from csv_managers import GroupCSVManager, KingCSVManager


class Menu:
    is_king_chosen = False

    @classmethod
    def main_menu(cls):
        print("Menu. 1 - Create a King, 2 - Choose the King, 3 - Clear kings, 4 - Delete the King, 5 - King groups 6 - Exit")
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
            pass


        elif decision == "6":
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

            group = input("In which group will be a king? Default group: \"default\"")
            if group not in GroupCSVManager.return_group_names():
                group = "default"
            king = King(name=name, age_when_dying=age_when_dying, age=age, death_chance=death_chance, increasing_chance=increasing_chance, group=group)
            print(f"Do you want to save? {king}")
            decision = input("y/n: ")
            if decision == "y":
                KingCSVManager.save_king(king)
            return Menu.main_menu()

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


def main():
    Menu.main_menu()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Goodbye!")
        sys.exit()