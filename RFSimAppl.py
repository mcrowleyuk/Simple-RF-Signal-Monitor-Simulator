from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rf')
def rf_data():
    signal_strength = random.randint(-100, -50)  # dBm
    frequency = random.choice([2400, 2450, 2500])  # MHz
    return jsonify(signal_strength=signal_strength, frequency=frequency)

if __name__ == '__main__':
    app.run(debug=True)
