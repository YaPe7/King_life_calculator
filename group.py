from king import King

class Group:
    def __init__(self, name: str, year: int):
        self.name = name
        self.kings = []
        try:
            self.year = int(year)
        except ValueError:
            self.year = 0

    def add_kings(self, kings: list):
        if type(kings) == King:
            self.kings.append(kings)
            return True
        elif type(kings) not in (list, tuple):
            return False
        for king in kings:
            if type(king) == King:
                self.kings.append(king)

    def change_year(self, new_value):
        try:
            new_value = int(new_value)
        except ValueError:
            return False
        self.year = new_value
        return True

    def live_one_year(self):
        self.year += 1
        passed = 0
        failed = 0
        for king in self.kings:
            result = king.grew_up()
            if not king._died:
                print(f"- {king}")
            if result:
                passed += 1
            else:
                failed += 1
        print(f"One year has passed. Now is {self.year}")
        print(f"{passed} {'kings are' if passed > 1 else 'king is'} alive, {failed} {'are' if failed > 1 else 'is'} dead.")

    @property
    def info_to_write(self):
        return self.name, self.year

    def __str__(self):
        return f'Group name = {self.name}, year = {self.year}'
