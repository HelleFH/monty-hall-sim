#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, request, jsonify
from random import randint

app = Flask(__name__, static_folder='static')

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
    events = []

    for round_num, doors in enumerate(game):
        attempts += 1
        goat = reveal_goat(doors)
        new_choice = randint(0, 1)
        final_choice = 0 if new_choice == 0 else 2 if goat == 1 else 1
        win = doors[final_choice]
        if win:
            wins += 1
        history.append(wins / attempts)

        event_log = [
            f"Round {round_num + 1}: Player chooses door 1;",
            f"Host shows door {goat + 1} has goat;",
            f"Player {'switches to door ' + str(final_choice + 1) if new_choice == 1 else 'sticks with door 1'};",
            f"Door {final_choice + 1} has {'car' if win else 'goat'};",
            f"Player {'wins!' if win else 'loses.'}"
        ]
        events.append(' '.join(event_log))

    return wins, history, events

# Simulate keep choice
def simulate_keep_choice(game: list):
    wins = 0
    attempts = 0
    history = []
    events = []

    for round_num, doors in enumerate(game):
        attempts += 1
        win = doors[0]
        if win:
            wins += 1
        history.append(wins / attempts)

        event_log = [
            f"Round {round_num + 1}: Player chooses door 1;",
            f"Host shows door {reveal_goat(doors) + 1} has goat;",
            "Player sticks with door 1;",
            f"Door 1 has {'car' if win else 'goat'};",
            f"Player {'wins!' if win else 'loses.'}"
        ]
        events.append(' '.join(event_log))

    return wins, history, events

# Simulate switch choice
def simulate_switch_choice(game: list):
    wins = 0
    attempts = 0
    history = []
    events = []

    for round_num, doors in enumerate(game):
        attempts += 1
        goat = reveal_goat(doors)
        final_choice = 1 if goat == 2 else 2
        win = doors[final_choice]
        if win:
            wins += 1
        history.append(wins / attempts)

        event_log = [
            f"Round {round_num + 1}: Player chooses door 1;",
            f"Host shows door {goat + 1} has goat;",
            f"Player switches to door {final_choice + 1};",
            f"Door {final_choice + 1} has {'car' if win else 'goat'};",
            f"Player {'wins!' if win else 'loses.'}"
        ]
        events.append(' '.join(event_log))

    return wins, history, events

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
    wins_random, history_random, events_random = simulate_random_choice(game)
    wins_keep, history_keep, events_keep = simulate_keep_choice(game)
    wins_switch, history_switch, events_switch = simulate_switch_choice(game)

    # Prepare data to send back as JSON
    data = {
        'simulation_count': num_simulations,
        'history_random': history_random,
        'history_keep': history_keep,
        'history_switch': history_switch,
        'total_wins_random': wins_random,
        'total_wins_keep': wins_keep,
        'total_wins_switch': wins_switch,
        'events_random': events_random,
        'events_keep': events_keep,
        'events_switch': events_switch
    }

    return jsonify(data)

# Example usage
if __name__ == '__main__':
    app.run(debug=True)
