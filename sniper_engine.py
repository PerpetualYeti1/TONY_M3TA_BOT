import requests

def get_token_price(token_address):
    try:
        url = f"https://api.dexscreener.com/latest/dex/pairs/solana/{token_address}"
        response = requests.get(url)
        data = response.json()

        return float(data["pair"]["priceUsd"])
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

def execute_buy(token_address, amount=1.0):
    return f"Executed buy: {amount} {token_address}"

def sniper_engine(token_address, target_price):
    price = get_token_price(token_address)

    if price is None:
        return "⚠️ Error getting token price."

    if price <= target_price:
        tx_result = execute_buy(token_address)
        return f"✅ Sniped at ${price:.6f}\n{tx_result}"
    else:
        return f"🔍 Watching {token_address} | Current: ${price:.6f}, Target: ${target_price:.6f}"
