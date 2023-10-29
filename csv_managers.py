import shutil
import os
import csv
from king import King
from tempfile import NamedTemporaryFile


class GroupCSVManager:
    # Format is "group_name;year"
    groups = "groups.csv"

    if not os.path.exists(groups):
        with open(groups, "w") as groups_file:
            groups_file.write("default;0\n")
            print("Group file created.")

    @classmethod
    def return_all_groups(cls):
        group_list = []
        with open(cls.groups, "r") as groups_file:
            for line in groups_file:
                line = line.strip().split(";")
                group_list.append((line[0], line[1]))
        return group_list

    @classmethod
    def return_group_names(cls):
        group_list = cls.return_all_groups()
        return [group[0] for group in group_list]


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
