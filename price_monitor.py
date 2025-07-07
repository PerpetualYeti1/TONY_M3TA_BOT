"""
Price monitoring service using CoinGecko API
"""

import asyncio
import aiohttp
import logging
from typing import Optional, Dict, List
from bot.storage import WatchStorage
from telegram import Bot
from config import BOT_TOKEN
from utils.logger import setup_logger

logger = setup_logger()

class PriceMonitor:
    def __init__(self):
        self.storage = WatchStorage()
        self.bot = Bot(BOT_TOKEN)
        self.session = None
        self.base_url = "https://api.coingecko.com/api/v3"
        self.price_cache = {}
        self.cache_timeout = 120  # 2 minutes cache
        self.last_cache_update = 0
        self.monitoring = False
        
    async def get_session(self):
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def get_token_price(self, token_id: str) -> Optional[float]:
        """Get current price for a token from CoinGecko"""
        try:
            session = await self.get_session()
            url = f"{self.base_url}/simple/price"
            params = {
                'ids': token_id,
                'vs_currencies': 'usd'
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if token_id in data and 'usd' in data[token_id]:
                        price = float(data[token_id]['usd'])
                        logger.debug(f"Got price for {token_id}: ${price}")
                        return price
                    else:
                        logger.warning(f"Token {token_id} not found in CoinGecko response")
                        return None
                elif response.status == 429:
                    logger.warning("CoinGecko API rate limit hit")
                    return None
                else:
                    logger.error(f"CoinGecko API error: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error fetching price for {token_id}: {e}")
            return None
    
    async def get_multiple_prices(self, token_ids: List[str]) -> Dict[str, float]:
        """Get prices for multiple tokens at once"""
        if not token_ids:
            return {}
            
        try:
            session = await self.get_session()
            url = f"{self.base_url}/simple/price"
            params = {
                'ids': ','.join(token_ids),
                'vs_currencies': 'usd'
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    prices = {}
                    for token_id in token_ids:
                        if token_id in data and 'usd' in data[token_id]:
                            prices[token_id] = float(data[token_id]['usd'])
                    return prices
                else:
                    logger.error(f"Error fetching multiple prices: {response.status}")
                    return {}
                    
        except Exception as e:
            logger.error(f"Error fetching multiple prices: {e}")
            return {}
    
    async def check_price_alerts(self):
        """Check all active watches for price alerts"""
        try:
            all_watches = self.storage.get_all_watches()
            if not all_watches:
                return
            
            # Get unique tokens to minimize API calls
            unique_tokens = list(set(watch['token'] for watch in all_watches))
            current_prices = await self.get_multiple_prices(unique_tokens)
            
            if not current_prices:
                logger.warning("No prices received from API")
                return
            
            # Check each watch
            for watch in all_watches:
                token = watch['token']
                target_price = watch['target_price']
                user_id = watch['user_id']
                chat_id = watch['chat_id']
                
                if token not in current_prices:
                    continue
                
                current_price = current_prices[token]
                
                # Check if target price is reached
                if self.is_target_reached(current_price, target_price):
                    await self.send_alert(chat_id, token, current_price, target_price)
                    # Remove the watch after alert is sent
                    self.storage.remove_watch(user_id, token)
                    logger.info(f"Alert sent and watch removed for {token} at ${current_price}")
                    
        except Exception as e:
            logger.error(f"Error checking price alerts: {e}")
    
    def is_target_reached(self, current_price: float, target_price: float) -> bool:
        """Check if target price is reached"""
        # Simple logic: alert when price crosses the target
        # This could be enhanced with more sophisticated logic
        return abs(current_price - target_price) / target_price <= 0.01  # 1% tolerance
    
    async def send_alert(self, chat_id: int, token: str, current_price: float, target_price: float):
        """Send price alert to user"""
        try:
            direction = "📈 above" if current_price > target_price else "📉 below"
            percentage_change = ((current_price - target_price) / target_price) * 100
            
            message = (
                f"🎯 **PRICE ALERT!**\n\n"
                f"**{token.upper()}** has reached your target!\n\n"
                f"**Current Price:** ${current_price:,.2f}\n"
                f"**Target Price:** ${target_price:,.2f}\n"
                f"**Change:** {direction} by {abs(percentage_change):.1f}%\n\n"
                f"🚀 **Time to take action!**"
            )
            
            await self.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
            logger.info(f"Alert sent for {token} to chat {chat_id}")
            
        except Exception as e:
            logger.error(f"Error sending alert: {e}")
    
    async def start_monitoring(self):
        """Start the price monitoring loop"""
        if self.monitoring:
            return
            
        self.monitoring = True
        logger.info("🔍 Price monitoring started")
        
        while self.monitoring:
            try:
                await self.check_price_alerts()
                # Wait 2 minutes before next check
                await asyncio.sleep(120)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error
    
    async def stop_monitoring(self):
        """Stop the price monitoring"""
        self.monitoring = False
        if self.session and not self.session.closed:
            await self.session.close()
        logger.info("🛑 Price monitoring stopped")
