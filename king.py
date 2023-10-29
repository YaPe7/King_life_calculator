from random import randint


class King:
    def __init__(self, died=False, group="default", **kwargs):
        self.name = kwargs["name"]
        self._died = died
        self.group = group
        try:
            self.age = int(kwargs["age"])
            self.age_when_dying = int(kwargs["age_when_dying"])
            self.death_chance = int(kwargs["death_chance"])
            self.increasing_chance = int(kwargs["increasing_chance"])
        except ValueError:
            raise ValueError("Error when creating a king.")

    @property
    def info_to_write(self):
        return self.name, self.age, self.age_when_dying, self.death_chance, self.increasing_chance, self._died, self.group

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
