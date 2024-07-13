# monty_hall.py

from random import choice, shuffle

class Monty_Hall:
    def __init__(self):
        self.doors = ['goat', 'goat', 'car']
        shuffle(self.doors)
        self.player_choice = None
        self.shown_goat = None

    def play(self, switch_choice=True):
        self.player_choice = choice([0, 1, 2])
        self.show_goat()
        if switch_choice:
            self.switch_door()
        return self.check_win()

    def show_goat(self):
        remaining_choices = [i for i in range(3) if i != self.player_choice and self.doors[i] == 'goat']
        self.shown_goat = choice(remaining_choices)

    def switch_door(self):
        self.player_choice = next(i for i in range(3) if i != self.player_choice and i != self.shown_goat)

    def check_win(self):
        return self.doors[self.player_choice] == 'car'
