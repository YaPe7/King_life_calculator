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

    def live_one_year(self):
        self.year += 1
        passed = 0
        failed = 0
        for king in self.kings:
            result = king.grew_up()
            if result:
                passed += 1
            else:
                failed += 1
        print(f"One year has passed. {passed} {'kings are' if passed > 1 else 'king is'} alive, {failed} {'are' if failed > 1 else 'is'} dead.")

    def info_to_write(self):
        return self.name, self.year
