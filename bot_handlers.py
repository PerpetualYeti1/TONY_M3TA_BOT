from telegram.ext import CommandHandler
from wallet import get_all_tokens, save_wallet, get_saved_wallet
from sniper_engine import sniper_engine

def start(update, context):
    update.message.reply_text("🟢 Welcome to TONY_M3TA_BOT.\nUse /wallet add <ADDRESS> to begin.")

def wallet_add(update, context):
    if len(context.args) != 1:
        update.message.reply_text("❌ Usage: /wallet add <WALLET_ADDRESS>")
        return
    address = context.args[0]
    save_wallet(update.effective_user.id, address)
    update.message.reply_text("✅ Wallet saved.")

def wallet_tokens(update, context):
    address = get_saved_wallet(update.effective_user.id)
    if not address:
        update.message.reply_text("❌ No wallet found. Use /wallet add <ADDRESS>")
        return

    tokens = get_all_tokens(address)
    if "error" in tokens:
        update.message.reply_text("⚠️ " + tokens["error"])
        return

    msg = "📜 Tokens in your wallet:\n"
    for t in tokens:
        msg += f"{t['symbol']} — {t['amount']:.4f}\n"
    update.message.reply_text(msg)

def snipe(update, context):
    if len(context.args) != 2:
        update.message.reply_text("❌ Usage: /snipe <TOKEN_ADDRESS> <TARGET_PRICE>")
        return
    token, price = context.args
    try:
        price = float(price)
        result = sniper_engine(token, price)
        update.message.reply_text(result)
    except:
        update.message.reply_text("❌ Invalid input. Use: /snipe <TOKEN_ADDRESS> <TARGET_PRICE>")

# To use these handlers in your main bot file:
# dp.add_handler(CommandHandler("start", start))
# dp.add_handler(CommandHandler("wallet", wallet_tokens))
# dp.add_handler(CommandHandler("wallet_add", wallet_add))
# dp.add_handler(CommandHandler("snipe", snipe))
