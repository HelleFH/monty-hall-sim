from flask import Flask, render_template, request, jsonify, Response
import random
import threading
import time

app = Flask(__name__)

# Global variables
running = False
games_counter = 0
results = {
    'typewriter_text': '',
    'games_won_not_switching': 0,
    'games_won_switching': 0,
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_simulation', methods=['POST'])
def start_simulation():
    global running, games_counter

    if not running:
        games_counter = 0
        reset_results()
        running = True
        threading.Thread(target=run_simulations).start()

    return jsonify({'status': 'started'})

@app.route('/stop_simulation', methods=['POST'])
def stop_simulation():
    global running

    if running:
        running = False

    return jsonify({
        'status': 'stopped',
        'results': {
            'games_won_not_switching': results['games_won_not_switching'],
            'games_won_switching': results['games_won_switching']
        }
    })

@app.route('/status', methods=['GET'])
def status():
    global games_counter, running, results

    return jsonify({
        'running': running,
        'games_counter': games_counter,
        'results': {
            'games_won_not_switching': results['games_won_not_switching'],
            'games_won_switching': results['games_won_switching']
        }
    })

@app.route('/stream')
def stream():
    def generate():
        global running, results

        while running:
            time.sleep(1)
            yield f"data: {results['typewriter_text']}\n\n"
            results['typewriter_text'] = ''

    return Response(generate(), mimetype='text/event-stream')

def reset_results():
    global results
    results['typewriter_text'] = ''
    results['games_won_not_switching'] = 0
    results['games_won_switching'] = 0

def run_simulations():
    global running, games_counter, results

    while running:
        simulate_game(games_counter % 2 == 0)  # Alternate between switching and not switching
        games_counter += 1

        time.sleep(0.5)  # Delay of 0.5 seconds between each simulation

def simulate_game(switch):
    global results
    doors = ['car', 'goat', 'goat']
    random.shuffle(doors)
    choose = random.choice([0, 1, 2])
    show = random.choice([x for x in [0, 1, 2] if x != choose and doors[x] == 'goat'])

    if switch:
        choose = [x for x in [0, 1, 2] if x not in [choose, show]][0]

    win = doors[choose] == 'car'

    if win:
        if switch:
            results['games_won_switching'] += 1
        else:
            results['games_won_not_switching'] += 1

    # Prepare game output for typewriter effect
    game_output = f'player chooses door {choose}; host shows door {show} has goat; '
    if switch:
        game_output += f'player switches to door {choose}; '
    else:
        game_output += f'player sticks with door {choose}; '
    game_output += f'door {choose} has {doors[choose]}; player {"wins" if win else "loses"}!\n'

    results['typewriter_text'] += game_output

if __name__ == '__main__':
    app.run(debug=True)
