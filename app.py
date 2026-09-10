from flask import Flask, jsonify
import os
app = Flask(__name__)

SYMBOLS = ["XAUUSD", "BTCUSD", "SFX60", "SFX40", "PAINX400", "GAIN400"]

@app.route('/')
def home():
    return "MZK Blaze is running 🔥 Ready to trade Gold, BTC, SFX60, SFX40, PAINX400, GAIN400"

@app.route('/start')
def start():
    return jsonify({"status": "BLAZE STARTED", "trading": SYMBOLS, "lot": 0.01, "message": "Connect MetaApi token next"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
