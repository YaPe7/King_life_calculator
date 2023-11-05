import shutil
import os
import csv
from king import King
from group import Group
from tempfile import NamedTemporaryFile


class GroupCSVManager:
    # Format is "group_name;year"
    groups = "groups.csv"

    if not os.path.exists(groups):
        with open(groups, "w") as groups_file:
            groups_file.write("default;0\n")
            print("Group file created.")

    @classmethod
    def _check_default_file(cls):
        groups = cls.return_group_names()
        if "default" not in groups:
            with open(cls.groups, "w") as groups_file:
                groups_file.write("default;0\n")

    @classmethod
    def return_all_groups(cls):
        group_list = []
        with open(cls.groups, "r") as groups_file:
            groups_file = csv.reader(groups_file, delimiter=";")
            for line in groups_file:
                group_list.append((line[0], line[1]))
        return group_list

    @classmethod
    def return_group_names(cls):
        group_list = cls.return_all_groups()
        return [group[0] for group in group_list]


    @classmethod
    def find_groups(cls, group_name: str):
        group_name = group_name.lower()
        groups = cls.return_all_groups()
        groups_found = []
        for group in groups:
            if group_name in (group[0], 'any'):
                groups_found.append(group)
        return groups_found

    @classmethod
    def save_group(cls, group: Group):
        info_to_write = group.info_to_write
        group = cls.find_groups(group.name) or False

        if not group:
            with open(cls.groups, "a", newline='', encoding="utf-8") as groups_file:
                king_writer = csv.writer(groups_file, delimiter=';')
                king_writer.writerow(info_to_write)
                print("King was written. It will be saved after exiting program")
        else:
            group = group[0]
            group = Group(group[0], group[1])
            cls._manipulate_group_info(group, info_to_write)

    @classmethod
    def _manipulate_group_info(cls, group: Group, info_to_write, delete=False):
        temp_csv = NamedTemporaryFile(mode="w", delete=False, encoding="utf-8")
        with open(cls.groups, "r", newline='') as group_csv, temp_csv:
            reader = csv.reader(group_csv, delimiter=";")
            writer = csv.writer(temp_csv, delimiter=";")
            for line in reader:
                if not (line and line[0] == group.name):
                    # print("Line is written")
                    writer.writerow(line)
                    continue
                if not delete:
                    writer.writerow(info_to_write)
                    # print("Information about group was updated")
                    continue
                if group.name == 'default':
                    writer.writerow(("default", 0))
                # print("Group was deleted.")
        shutil.move(temp_csv.name, cls.groups)

    def delete_group(cls, group: Group):
        cls._manipulate_group_info(group, delete=True)


class KingCSVManager:
    file = "kings.csv"

    if not os.path.exists(file):
        with open(file, "w") as king_csv:
            print("File created.")

    @classmethod
    def find_king(cls, name='any') -> list:
        king_list = []
        with open(cls.file, "r", newline='') as king_csv:
            king_reader = csv.reader(king_csv, delimiter=';')
            for l in king_reader:
                if not l:
                    continue
                if l and name.lower().strip() in l[0].strip().lower() or name == "any":
                    l[5] = False if l[5] == "False" else True
                    king_list.append(King(name=l[0], age=l[1], age_when_dying=l[2], death_chance=l[3], increasing_chance=l[4], died=l[5], group=l[6]))
        return king_list

    @classmethod
    def _manipulate_king_info(cls, king: King, info_to_write=False, delete=False):
        temp_csv = NamedTemporaryFile(mode="w", delete=False, encoding="utf-8")
        with open(cls.file, "r", newline='') as king_csv, temp_csv:
            reader = csv.reader(king_csv, delimiter=";")
            writer = csv.writer(temp_csv, delimiter=";")
            for line in reader:
                if not (line and line[0] == king.name):
                    # print("Line is written")
                    writer.writerow(line)
                    continue
                if not delete:
                    writer.writerow(info_to_write)
                    # print("Information about king was updated")
                    continue
                # print("King was deleted.")
        shutil.move(temp_csv.name, cls.file)

    @classmethod
    def save_king(cls, kings: list | King):
        if type(kings) == King:
            kings = [kings]
        for king in kings:
            info_to_write = king.info_to_write
            king = cls.find_king(king.name) or False

            if not king:
                with open(cls.file, "a", newline='', encoding="utf-8") as king_csv:
                    king_writer = csv.writer(king_csv, delimiter=';')
                    king_writer.writerow(info_to_write)
                    # print("King was written. It will be saved after exiting program")
            else:
                cls._manipulate_king_info(king[0], info_to_write)

    @classmethod
    def return_kings_by_groups(cls, group: Group):
        kings = cls.find_king()
        sorted_kings = []
        # print(kings)
        for king in kings:
            if group.name == king.group:
                sorted_kings.append(king)
        return sorted_kings


    @classmethod
    def delete_king(cls, king: King):
        cls._manipulate_king_info(king, delete=True)

    @classmethod
    def clear_file(cls):
        open(cls.file, "w").close()
        print("File cleared.")
