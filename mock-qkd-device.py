from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/api/v1/keys/<slave_SAE_ID>/status', methods=['GET'])
def get_status(slave_SAE_ID):

    # Simulate a status response
    status = {
        "status": "active",
        "slave_SAE_ID": slave_SAE_ID
    }
    return jsonify(status)

@app.route('/api/v1/keys/<slave_SAE_ID>/enc_keys', methods=['POST', 'GET'])
def get_enc_keys(slave_SAE_ID):

    key_length = 256
    key = os.urandom(key_length // 8)  # Generate 256-bit key
    key_hex = key.hex()  # Convert to hex for easy transport

    return jsonify({"enc_key": key_hex})

@app.route('/api/v1/keys/<master_SAE_ID>/dec_keys', methods=['POST', 'GET'])
def get_dec_keys(master_SAE_ID):
    
    key_ids = request.json.get("key_ids", [])
    keys = {key_id: os.urandom(32).hex() for key_id in key_ids}  # Simulate key retrieval

    return jsonify({"dec_keys": keys})

if __name__ == '__main__':
    app.run(port=5000)
