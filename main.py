import sys
from king import King
from group import Group
from csv_managers import GroupCSVManager, KingCSVManager


class Menu:
    is_king_chosen = False
    GroupCSVManager._check_default_file()

    @classmethod
    def main_menu(cls):
        print("Menu. 1 - Create a King, 2 - Choose the King, 3 - Clear kings, 4 - Delete the King, 5 - King groups, 6 - Exit")
        decision = input("Option: ")
        if decision == "1":
            cls.create_king()
        elif decision == "2":
            king = cls.find_king()
            result = cls.king_menu(king)
        elif decision == "3":
            print("Are you sure? There is no way to backup data in this version.")
            confirm = True if input("y/n: ") == "y" else False
            if confirm:
                KingCSVManager.clear_file()
        elif decision == "4":
            king = cls.find_king()
            KingCSVManager.delete_king(king)
        elif decision == "5":
            group = cls.find_king_groups()
            if not group:
                return cls.main_menu()
            group = Group(group[0], group[1])
            group.add_kings(KingCSVManager.return_kings_by_groups(group))
            cls.king_groups_info(group)
        elif decision == "6":
            raise KeyboardInterrupt
        else:
            print("Invalid command.")
        return cls.main_menu()

    @classmethod
    def king_groups_info(cls, group: Group):
        print("1 - manipulate group, 2 - delete group, 3 - Back to menu")
        sub_menu = input(": ")
        if sub_menu == '1':
            cls.manipulate_king_group(group)
        elif sub_menu == '2':
            GroupCSVManager.delete_group(group)
        else:
            return cls.main_menu()

    @classmethod
    def find_king_groups(cls):
        group_to_find = input("Enter a group name or a part of it: ")
        if not group_to_find:
            group_to_find = "any"
        groups = GroupCSVManager.find_groups(group_to_find)
        if groups:
            i = 0
            for group in groups:
                str_group = f"id {i} || name = {group[0]}, year = {group[1]}"
                print(str_group)
                print(len(str_group) * "=")
                i += 1
        else:
            print("Nothing.")
            return False
        try:
            group_id = int(input())
            if group_id >= len(groups) or group_id < 0:
                raise ValueError
        except ValueError:
            print("You didn't write a number. Aborting...")
            return False
        return groups[group_id]

    @classmethod
    def manipulate_king_group(cls, group: Group):
        while True:
            print("Group:", group)
            print("What to do next with a group? 1 - Live one year, 2 - Add a king, 3 - change year, 4 - Back")
            menu = input(": ")
            if menu == '1':
                group.live_one_year()
                KingCSVManager.save_king(group.kings)
            elif menu == '2':
                king = cls.find_king()
                group.add_kings(king)
            elif menu == '3':
                new_value = input("Write new year: ")
                result = group.change_year(new_value)
                if result:
                    print("Year was successfully changed. New value is:", group.year)
                else:
                    print("Error when changing a value.")
            else:
                break
            GroupCSVManager.save_group(group)

        return cls.king_groups_info(group)


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

            print("In which group will be a king? Default group: \"default\"")
            group = input(": ")
            if group not in GroupCSVManager.return_group_names():
                group = "default"
            king = King(name=name, age_when_dying=age_when_dying, age=age, death_chance=death_chance, increasing_chance=increasing_chance, group=group)
            print(f"Do you want to save? {king}")
            decision = input("y/n: ")
            if decision == "y":
                KingCSVManager.save_king(king)
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

    @classmethod
    def king_menu(cls, king: King):
        if king is None:
            print("Aborted.")
            return False
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
        return True


def main():
    Menu.main_menu()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Goodbye!")
        sys.exit()