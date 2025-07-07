"""
Telegram bot command handlers
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.storage import WatchStorage
from bot.price_monitor import PriceMonitor
from utils.logger import setup_logger

logger = setup_logger()
storage = WatchStorage()
price_monitor = PriceMonitor()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    welcome_message = """
🟢 **TONY_M3TA_BOT** is ready!

🎯 **Commands:**
• `/snipe TOKEN PRICE` - Set price alert for a token
• `/list` - Show all active watches
• `/remove TOKEN` - Remove a watch
• `/help` - Show detailed help

**Example:**
`/snipe bitcoin 50000` - Alert when Bitcoin reaches $50,000

Ready to snipe some crypto! 🚀
"""
    
    await update.message.reply_text(welcome_message, parse_mode='Markdown')
    logger.info(f"User {update.effective_user.id} started the bot")

async def snipe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /snipe command"""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    if not context.args or len(context.args) != 2:
        await update.message.reply_text(
            "❌ **Usage:** `/snipe TOKEN PRICE`\n\n"
            "**Examples:**\n"
            "• `/snipe bitcoin 50000`\n"
            "• `/snipe ethereum 3000`\n"
            "• `/snipe cardano 1.5`",
            parse_mode='Markdown'
        )
        return
    
    try:
        token = context.args[0].lower()
        target_price = float(context.args[1])
        
        if target_price <= 0:
            await update.message.reply_text("❌ Price must be greater than 0")
            return
        
        # Validate token exists on CoinGecko
        current_price = await price_monitor.get_token_price(token)
        if current_price is None:
            await update.message.reply_text(
                f"❌ Token '{token}' not found on CoinGecko.\n"
                f"Please use the exact CoinGecko ID (e.g., 'bitcoin', 'ethereum', 'cardano')"
            )
            return
        
        # Add watch
        success = storage.add_watch(user_id, chat_id, token, target_price)
        
        if success:
            price_direction = "📈 above" if target_price > current_price else "📉 below"
            await update.message.reply_text(
                f"🎯 **Watch Added!**\n\n"
                f"**Token:** {token.upper()}\n"
                f"**Current Price:** ${current_price:,.2f}\n"
                f"**Target Price:** ${target_price:,.2f}\n"
                f"**Alert when:** {price_direction} target\n\n"
                f"I'll notify you when {token.upper()} reaches ${target_price:,.2f}! 🚀",
                parse_mode='Markdown'
            )
            logger.info(f"Added watch for user {user_id}: {token} at ${target_price}")
        else:
            await update.message.reply_text(
                f"⚠️ You already have a watch for {token.upper()}.\n"
                f"Use `/remove {token}` to remove the existing watch first."
            )
            
    except ValueError:
        await update.message.reply_text("❌ Invalid price format. Please enter a valid number.")
    except Exception as e:
        logger.error(f"Error in snipe command: {e}")
        await update.message.reply_text("❌ An error occurred. Please try again.")

async def list_watches(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /list command"""
    user_id = update.effective_user.id
    watches = storage.get_user_watches(user_id)
    
    if not watches:
        await update.message.reply_text(
            "📭 **No Active Watches**\n\n"
            "Use `/snipe TOKEN PRICE` to set up your first price alert!"
        )
        return
    
    message = "📊 **Your Active Watches:**\n\n"
    
    for watch in watches:
        token = watch['token']
        target_price = watch['target_price']
        
        # Get current price
        current_price = await price_monitor.get_token_price(token)
        if current_price:
            price_diff = ((current_price - target_price) / target_price) * 100
            direction = "📈" if current_price > target_price else "📉"
            message += (
                f"**{token.upper()}**\n"
                f"Current: ${current_price:,.2f}\n"
                f"Target: ${target_price:,.2f}\n"
                f"Difference: {direction} {abs(price_diff):.1f}%\n\n"
            )
        else:
            message += (
                f"**{token.upper()}**\n"
                f"Target: ${target_price:,.2f}\n"
                f"Status: ⚠️ Price unavailable\n\n"
            )
    
    message += "Use `/remove TOKEN` to remove a watch."
    await update.message.reply_text(message, parse_mode='Markdown')

async def remove_watch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /remove command"""
    user_id = update.effective_user.id
    
    if not context.args or len(context.args) != 1:
        await update.message.reply_text(
            "❌ **Usage:** `/remove TOKEN`\n\n"
            "**Example:** `/remove bitcoin`"
        )
        return
    
    token = context.args[0].lower()
    success = storage.remove_watch(user_id, token)
    
    if success:
        await update.message.reply_text(
            f"✅ **Watch Removed**\n\n"
            f"No longer watching {token.upper()} for price alerts."
        )
        logger.info(f"Removed watch for user {user_id}: {token}")
    else:
        await update.message.reply_text(
            f"❌ No active watch found for {token.upper()}.\n"
            f"Use `/list` to see your active watches."
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    help_text = """
🤖 **TONY_M3TA_BOT Help**

**Commands:**
• `/start` - Welcome message and quick start
• `/snipe TOKEN PRICE` - Set price alert for a cryptocurrency
• `/list` - Show all your active price watches
• `/remove TOKEN` - Remove a specific watch
• `/help` - Show this help message

**How to use:**
1. Use `/snipe` with a CoinGecko token ID and target price
2. Bot will monitor the price and alert you when reached
3. Use `/list` to check your active watches
4. Use `/remove` to stop watching a token

**Token Examples:**
• `bitcoin` - Bitcoin (BTC)
• `ethereum` - Ethereum (ETH)
• `cardano` - Cardano (ADA)
• `solana` - Solana (SOL)
• `chainlink` - Chainlink (LINK)

**Example Commands:**
• `/snipe bitcoin 50000` - Alert when Bitcoin reaches $50,000
• `/snipe ethereum 3000` - Alert when Ethereum reaches $3,000
• `/list` - Show all active watches
• `/remove bitcoin` - Stop watching Bitcoin

**Notes:**
• Prices are checked every 2 minutes
• You can have multiple watches active
• Use exact CoinGecko token IDs for best results
• Bot works 24/7 to monitor your targets

Happy sniping! 🎯🚀
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')
