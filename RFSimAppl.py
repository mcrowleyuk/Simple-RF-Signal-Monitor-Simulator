
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import random



app = Flask(__name__)
app.secret_key = 'hello+!'  # Replace with a secure random key


@app.route('/')
def home():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/rf')
def rf_data():
    signal_strength = random.randint(-100, -50)  # dBm
    frequency = random.choice([2400, 2450, 2500])  # MHz
    return jsonify(signal_strength=signal_strength, frequency=frequency)


@app.route('/ew')
def ew():
    signal_strength = -50  # dBm
    frequency = 2400; # MHz
    return jsonify(signal_strength=signal_strength, frequency=frequency)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == app.secret_key:  # Replace with your desired password
            session['authenticated'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

 
    
