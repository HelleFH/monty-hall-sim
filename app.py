#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, request, jsonify
from random import randint
import matplotlib.pyplot as plt

app = Flask(__name__)

# Function to generate random games
def generate_game(n: int):
    game = []
    for _ in range(n):
        doors = [False] * 3
        winner = randint(0, 2)  # Choose winning door randomly
        doors[winner] = True
        game.append(doors)
    return game

# Function to reveal a goat behind one of the doors
def reveal_goat(doors):
    for i in range(1, 3):
        if not doors[i]:
            return i

# Simulate random choice
def simulate_random_choice(game: list):
    wins = 0
    attempts = 0
    history = []

    for doors in game:
        attempts += 1
        goat = reveal_goat(doors)
        new_choice = randint(0, 1)
        final_choice = 0 if new_choice == 0 else 2 if goat == 1 else 1
        if doors[final_choice]:
            wins += 1
        history.append(wins / attempts)

    return wins, history

# Simulate keep choice
def simulate_keep_choice(game: list):
    wins = 0
    attempts = 0
    history = []

    for doors in game:
        attempts += 1
        if doors[0]:
            wins += 1
        history.append(wins / attempts)

    return wins, history

# Simulate switch choice
def simulate_switch_choice(game: list):
    wins = 0
    attempts = 0
    history = []

    for doors in game:
        attempts += 1
        goat = reveal_goat(doors)
        new_choice = 1 if goat == 2 else 2
        if doors[new_choice]:
            wins += 1
        history.append(wins / attempts)

    return wins, history

# Route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to start simulations
@app.route('/start_simulations', methods=['POST'])
def start_simulations():
    num_simulations = int(request.form['num_simulations'])
    game = generate_game(num_simulations)

    # Run the three simulations
    wins_random, history_random = simulate_random_choice(game)
    wins_keep, history_keep = simulate_keep_choice(game)
    wins_switch, history_switch = simulate_switch_choice(game)

    # Prepare data to send back as JSON
    data = {
        'simulation_count': num_simulations,
        'history_random': history_random,
        'history_keep': history_keep,
        'history_switch': history_switch,
        'total_wins_random': wins_random,
        'total_wins_keep': wins_keep,
        'total_wins_switch': wins_switch
    }

    return jsonify(data)

# Example usage
if __name__ == '__main__':
    app.run(debug=True)
