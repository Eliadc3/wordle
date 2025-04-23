from flask import Flask, render_template, request, jsonify, session
import pandas as pd
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'wordle-secret-key'

# טוען את המילים מה-CSV
words = pd.read_csv('words.csv', header=None).iloc[:, 0].dropna().astype(str).tolist()

def get_daily_word():
    index = datetime.now().toordinal() % len(words)
    return words[index]

@app.route('/')
def index():
    if 'target' not in session:
        session['target'] = random.choice(words)
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    data = request.get_json()
    guess_word = data['word']
    target = session.get('target', random.choice(words))
    feedback = []

    for i in range(5):
        if guess_word[i] == target[i]:
            feedback.append('green')
        elif guess_word[i] in target:
            feedback.append('yellow')
        else:
            feedback.append('gray')

    won = guess_word == target
    if won:
        session.pop('target', None)

    return jsonify({'feedback': feedback, 'won': won})

if __name__ == '__main__':
    app.run(debug=True)
