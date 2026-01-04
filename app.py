import time
import hashlib
import json
import random
import numpy as np
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from sklearn.ensemble import IsolationForest

app = Flask(__name__)
app.secret_key = 'DELHI_GOVT_SECURE_KEY_2026' # Required for Login Session

# --- 1. BLOCKCHAIN CORE ---
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.data, sort_keys=True) + str(self.index) + str(self.timestamp) + str(self.previous_hash)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), {"info": "GNCTD SECURE LEDGER v4.0"}, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_data):
        prev_block = self.get_latest_block()
        new_block = Block(len(self.chain), time.time(), new_data, prev_block.hash)
        self.chain.append(new_block)
        return new_block

ledger = Blockchain()

# --- 2. AI ENGINE ---
print("⚙️ [SYSTEM] Loading Neural Networks for PWD/Jal Board...")
rng = np.random.RandomState(42)
X_train = 0.3 * rng.randn(100, 1) + 2500000 
X_train = np.r_[X_train, np.random.uniform(low=9000000, high=20000000, size=(20, 1))]
clf = IsolationForest(random_state=42, contamination=0.1)
clf.fit(X_train)

# --- 3. ROUTES ---

@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # DEMO CREDENTIALS
        if username == 'admin' and password == 'delhi2026':
            session['user'] = 'Chief Auditor (GNCTD)'
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="ACCESS DENIED: Invalid Credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    amount = float(data.get('amount'))
    
    # AI Logic
    prediction = clf.predict([[amount]])[0]
    is_anomaly = prediction == -1
    
    risk_score = random.randint(88, 99) if is_anomaly else random.randint(1, 15)
    status = "CRITICAL THREAT" if is_anomaly else "VERIFIED SAFE"
    
    # Generate random Chart Data for the frontend visualization
    chart_data = [random.randint(20, 100) for _ in range(6)]
    
    result = {
        "vendor": data.get('vendor'),
        "department": data.get('department'),
        "amount": "₹{:,.2f}".format(amount),
        "status": status,
        "risk_score": risk_score,
        "chart_trend": chart_data,
        "timestamp": time.strftime("%d-%b-%Y %H:%M:%S")
    }

    tx_hash = "N/A"
    if is_anomaly:
        new_block = ledger.add_block(result)
        tx_hash = new_block.hash
    
    return jsonify({"result": result, "blockchain_hash": tx_hash})

@app.route('/ledger', methods=['GET'])
def get_ledger():
    data = []
    for block in ledger.chain:
        data.append({
            "index": block.index,
            "hash": block.hash,
            "data": block.data,
            "timestamp": time.strftime("%H:%M:%S", time.localtime(block.timestamp))
        })
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
