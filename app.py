import time
import hashlib
import json
import random
import locale
import numpy as np
from flask import Flask, render_template, jsonify, request
from sklearn.ensemble import IsolationForest

app = Flask(__name__)

# --- 1. BLOCKCHAIN SYSTEM (IMMUTABLE LEDGER) ---
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
        return Block(0, time.time(), {"info": "SAMADHAAN GENESIS BLOCK - GOVT OF NCT DELHI"}, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_data):
        prev_block = self.get_latest_block()
        new_block = Block(len(self.chain), time.time(), new_data, prev_block.hash)
        self.chain.append(new_block)
        return new_block

ledger = Blockchain()

# --- 2. AI MODEL (Adapted for Indian Economy) ---
print("\n[SAMADHAAN] Initializing Neural Kernels for Govt Spending...")
rng = np.random.RandomState(42)

# Training Data: Normal tenders around ₹25 Lakhs (25,00,000)
X_train = 0.3 * rng.randn(100, 1) + 2500000 
# Anomalies: Tenders > ₹1 Crore or extremely low
X_train = np.r_[X_train, np.random.uniform(low=8000000, high=15000000, size=(20, 1))]

clf = IsolationForest(random_state=42, contamination=0.1)
clf.fit(X_train)
print("[SAMADHAAN] AI Model Active. Monitoring PWD, NDMC, & Jal Board.\n")

# --- 3. HELPER: Format Currency to Indian Style (Lakhs/Crores) ---
def format_inr(amount):
    try:
        return "₹" + "{:,.2f}".format(float(amount))
    except:
        return amount

# --- 4. ROUTES ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    amount = float(data.get('amount'))
    vendor = data.get('vendor')
    dept = data.get('department')
    
    # AI Prediction
    prediction = clf.predict([[amount]])[0] 
    is_anomaly = prediction == -1
    
    # Risk Logic
    if is_anomaly:
        status = "FLAGGED FOR AUDIT"
        risk_score = random.randint(85, 99)
        risk_level = "CRITICAL"
    else:
        status = "CLEARED"
        risk_score = random.randint(2, 15)
        risk_level = "SAFE"

    # Simulate GST/PAN Checks
    checks = {
        "gst_valid": "TRUE" if risk_score < 90 else "MISMATCH",
        "pan_linked": "TRUE",
        "blacklist_check": "CLEAN" if risk_score < 80 else "MATCH FOUND"
    }

    result = {
        "vendor": vendor,
        "department": dept,
        "amount": format_inr(amount),
        "status": status,
        "risk_level": risk_level,
        "risk_score": risk_score,
        "checks": checks,
        "timestamp": time.strftime("%d-%m-%Y %H:%M:%S")
    }

    tx_hash = "N/A"
    # Store in Blockchain if High Risk
    if is_anomaly:
        new_block = ledger.add_block(result)
        tx_hash = new_block.hash
    
    return jsonify({
        "result": result,
        "blockchain_hash": tx_hash
    })

@app.route('/ledger', methods=['GET'])
def get_ledger():
    chain_data = []
    for block in ledger.chain:
        chain_data.append({
            "index": block.index,
            "hash": block.hash,
            "data": block.data,
            "timestamp": time.ctime(block.timestamp)
        })
    return jsonify(chain_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)