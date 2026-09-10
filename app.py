from flask import Flask, jsonify
import os
from metaapi_cloud_sdk import MetaApi

app = Flask(__name__)

# YOUR TRADING SETTINGS
SYMBOLS = ["XAUUSD", "BTCUSD", "SFX60", "SFX40", "PAINX400", "GAIN400"]
LOT_SIZE = 0.01

TOKEN = os.getenv("METAAPI_TOKEN")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

@app.route('/')
def home():
    return "🔥 MZK Blaze is LIVE - Trading: Gold, BTC, SFX60, SFX40, PAINX400, GAIN400 | Lot: 0.01"

@app.route('/start')
async def start():
    try:
        if not TOKEN or not ACCOUNT_ID:
            return jsonify({"error": "Add METAAPI_TOKEN and ACCOUNT_ID in Render Environment"})

        api = MetaApi(TOKEN)
        account = await api.metatrader_account_api.get_account(ACCOUNT_ID)
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()

        results = []
        for symbol in SYMBOLS:
            try:
                price = await connection.get_symbol_price(symbol)
                # Simple Blaze Logic: Buy Gold & SFX, Sell BTC check
                order_type = "buy" if symbol in ["XAUUSD", "SFX60", "SFX40", "PAINX400", "GAIN400"] else "buy"
                await connection.create_market_buy_order(symbol, LOT_SIZE)
                results.append(f"{symbol}: BUY {LOT_SIZE} @ {price['bid']}")
            except Exception as e:
                results.append(f"{symbol}: {str(e)}")

        return jsonify({"status": "BLAZE EXECUTED", "trades": results})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
