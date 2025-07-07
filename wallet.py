import requests

def get_all_tokens(address):
    try:
        url = f"https://public-api.solscan.io/account/tokens?account={address}"
        headers = {
            "accept": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        tokens = response.json()

        return [{
            "symbol": token.get("tokenSymbol", "Unknown"),
            "mint": token.get("tokenAddress"),
            "amount": float(token.get("tokenAmount", {}).get("uiAmount", 0)),
        } for token in tokens if token.get("tokenAmount", {}).get("uiAmount", 0) > 0]
    except Exception as e:
        return {"error": str(e)}

wallet_store = {}

def save_wallet(user_id, address):
    wallet_store[user_id] = address

def get_saved_wallet(user_id):
    return wallet_store.get(user_id)
