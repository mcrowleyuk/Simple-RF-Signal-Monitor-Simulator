from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import socket
import threading
import struct
import os


data_lock = threading.Lock()

app = Flask(__name__)
app.secret_key = 'hello+!'  # Replace with a secure random key

# Shared data store for latest UDP message
latest_data = {'signal_strength': -100, 'frequency': 2400}

def udp_listener():
    global latest_data
    HOST = '127.0.0.1'
    PORT = 8082
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    print(f"[UDP] Listening on port {PORT}...")

    while True:
        data, addr = s.recvfrom(1024)
        try:
            decoded = data.decode('utf-8').strip()
            parts = decoded.split()

            if len(parts) == 2:
                signal_strength = int(parts[0])
                frequency = int(parts[1])
                
                with data_lock:
                    latest_data.update({
                        'signal_strength': signal_strength,
                        'frequency': frequency
                    })

                print(f"Received: dBm={signal_strength}, freq={frequency}")
            else:
                print("Unexpected format:", decoded)
        except Exception as e:
            print("Error decoding UDP data:", e)

# --- Flask Routes ---
@app.route('/')
def home():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/rf')
def rf_data():
    print("RF route accessed")
    print("Flask sees:", latest_data)
    with data_lock:
        return jsonify(latest_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == app.secret_key:
            session['authenticated'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))




# --- Start UDP Listener in Background ---

if __name__ == '__main__':
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        threading.Thread(target=udp_listener, daemon=True).start()
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
