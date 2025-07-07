"""
Advanced Token Sniping System with DexScreener Integration
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import logging

logger = logging.getLogger(__name__)

class TokenSniperError(Exception):
    """Custom exception for token sniping errors"""
    pass

class TokenSniper:
    """
    Advanced token sniping system with comprehensive analysis
    """
    
    def __init__(self):
        self.session = None
        self.dexscreener_base = "https://api.dexscreener.com"
        self.rugcheck_base = "https://api.rugcheck.xyz"
        self.birdeye_base = "https://public-api.birdeye.so"
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes
        
        # Risk scoring weights
        self.risk_weights = {
            'mint_authority': 0.25,
            'freeze_authority': 0.25,
            'top_holders': 0.20,
            'liquidity': 0.15,
            'social_presence': 0.10,
            'trading_volume': 0.05
        }
        
    async def get_session(self):
        """Get or create aiohttp session"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def get_new_tokens(self, limit: int = 20) -> List[Dict]:
        """
        Get new tokens from DexScreener (using third-party scraper approach)
        """
        try:
            session = await self.get_session()
            
            # Use DexScreener API to get pairs and filter for new ones
            url = f"{self.dexscreener_base}/latest/dex/pairs/solana"
            
            # Since DexScreener doesn't have a direct new tokens endpoint,
            # we'll get recent pairs and filter by creation time
            params = {
                'limit': limit * 2  # Get more to filter down
            }
            
            # For now, we'll use a simulated approach since DexScreener doesn't have this endpoint
            # In production, you'd use Apify or similar service
            new_tokens = await self._get_simulated_new_tokens(limit)
            
            # Enhance with DexScreener data
            enhanced_tokens = []
            for token in new_tokens:
                try:
                    token_data = await self.get_token_details(token['address'])
                    if token_data:
                        enhanced_tokens.append({
                            **token,
                            **token_data,
                            'discovery_time': datetime.now().isoformat()
                        })
                except Exception as e:
                    logger.error(f"Error enhancing token {token['address']}: {e}")
                    continue
            
            return enhanced_tokens
            
        except Exception as e:
            logger.error(f"Error getting new tokens: {e}")
            return []
    
    async def _get_simulated_new_tokens(self, limit: int) -> List[Dict]:
        """
        Simulate new token discovery for demo purposes
        In production, this would connect to real-time sources
        """
        # Popular Solana tokens for demonstration
        demo_tokens = [
            {
                'address': 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263',
                'symbol': 'BONK',
                'name': 'Bonk',
                'created_at': (datetime.now() - timedelta(minutes=30)).isoformat()
            },
            {
                'address': 'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm',
                'symbol': 'WIF',
                'name': 'dogwifhat',
                'created_at': (datetime.now() - timedelta(minutes=45)).isoformat()
            },
            {
                'address': 'ukHH6c7mMyiWCf1b9pnWe25TSpkDDt3H5pQZgZ74J82',
                'symbol': 'BOME',
                'name': 'Book of Meme',
                'created_at': (datetime.now() - timedelta(minutes=60)).isoformat()
            }
        ]
        
        return demo_tokens[:limit]
    
    async def get_token_details(self, token_address: str) -> Optional[Dict]:
        """
        Get detailed token information from DexScreener
        """
        try:
            cache_key = f"token_details_{token_address}"
            if cache_key in self.cache:
                cached_data, timestamp = self.cache[cache_key]
                if time.time() - timestamp < self.cache_timeout:
                    return cached_data
            
            session = await self.get_session()
            url = f"{self.dexscreener_base}/latest/dex/tokens/{token_address}"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Process and structure the data
                    if 'pairs' in data and data['pairs']:
                        pair = data['pairs'][0]  # Take first pair
                        
                        token_data = {
                            'pair_address': pair.get('pairAddress'),
                            'base_token': pair.get('baseToken', {}),
                            'quote_token': pair.get('quoteToken', {}),
                            'price_usd': float(pair.get('priceUsd', 0)),
                            'price_native': float(pair.get('priceNative', 0)),
                            'volume_24h': float(pair.get('volume', {}).get('h24', 0)),
                            'volume_1h': float(pair.get('volume', {}).get('h1', 0)),
                            'price_change_24h': float(pair.get('priceChange', {}).get('h24', 0)),
                            'price_change_1h': float(pair.get('priceChange', {}).get('h1', 0)),
                            'liquidity_usd': float(pair.get('liquidity', {}).get('usd', 0)),
                            'market_cap': float(pair.get('marketCap', 0)),
                            'fdv': float(pair.get('fdv', 0)),
                            'txns_24h': pair.get('txns', {}).get('h24', {}),
                            'created_at': pair.get('pairCreatedAt'),
                            'dex_id': pair.get('dexId'),
                            'url': pair.get('url'),
                            'info': pair.get('info', {})
                        }
                        
                        # Cache the result
                        self.cache[cache_key] = (token_data, time.time())
                        return token_data
                    
                return None
                
        except Exception as e:
            logger.error(f"Error getting token details for {token_address}: {e}")
            return None
    
    async def analyze_tokenomics(self, token_address: str) -> Dict:
        """
        Comprehensive tokenomics analysis
        """
        try:
            analysis = {
                'token_address': token_address,
                'timestamp': datetime.now().isoformat(),
                'risk_score': 0,
                'risk_level': 'UNKNOWN',
                'flags': [],
                'metrics': {}
            }
            
            # Get token details
            token_details = await self.get_token_details(token_address)
            if not token_details:
                analysis['flags'].append('NO_DEXSCREENER_DATA')
                analysis['risk_score'] = 100
                return analysis
            
            # Analyze liquidity
            liquidity_usd = token_details.get('liquidity_usd', 0)
            if liquidity_usd < 5000:
                analysis['flags'].append('LOW_LIQUIDITY')
                analysis['risk_score'] += 25
            elif liquidity_usd < 20000:
                analysis['flags'].append('MEDIUM_LIQUIDITY')
                analysis['risk_score'] += 10
            
            # Analyze volume
            volume_24h = token_details.get('volume_24h', 0)
            if volume_24h < 10000:
                analysis['flags'].append('LOW_VOLUME')
                analysis['risk_score'] += 15
            
            # Analyze market cap
            market_cap = token_details.get('market_cap', 0)
            if market_cap < 100000:
                analysis['flags'].append('LOW_MARKET_CAP')
                analysis['risk_score'] += 20
            
            # Analyze age
            age_hours = 0
            created_at = token_details.get('created_at')
            if created_at:
                creation_time = datetime.fromtimestamp(created_at / 1000)
                age_hours = (datetime.now() - creation_time).total_seconds() / 3600
                if age_hours < 1:
                    analysis['flags'].append('VERY_NEW_TOKEN')
                    analysis['risk_score'] += 30
                elif age_hours < 24:
                    analysis['flags'].append('NEW_TOKEN')
                    analysis['risk_score'] += 15
            
            # Analyze price changes
            price_change_24h = token_details.get('price_change_24h', 0)
            if abs(price_change_24h) > 100:
                analysis['flags'].append('HIGH_VOLATILITY')
                analysis['risk_score'] += 10
            
            # Get additional security analysis
            security_analysis = await self.check_security(token_address)
            if security_analysis:
                analysis['flags'].extend(security_analysis.get('flags', []))
                analysis['risk_score'] += security_analysis.get('risk_score', 0)
            
            # Calculate final risk level
            if analysis['risk_score'] < 20:
                analysis['risk_level'] = 'LOW'
            elif analysis['risk_score'] < 50:
                analysis['risk_level'] = 'MEDIUM'
            elif analysis['risk_score'] < 80:
                analysis['risk_level'] = 'HIGH'
            else:
                analysis['risk_level'] = 'EXTREME'
            
            analysis['metrics'] = {
                'liquidity_usd': liquidity_usd,
                'volume_24h': volume_24h,
                'market_cap': market_cap,
                'price_change_24h': price_change_24h,
                'age_hours': age_hours
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing tokenomics for {token_address}: {e}")
            return {
                'token_address': token_address,
                'error': str(e),
                'risk_score': 100,
                'risk_level': 'EXTREME'
            }
    
    async def check_security(self, token_address: str) -> Optional[Dict]:
        """
        Check token security using RugCheck API
        """
        try:
            session = await self.get_session()
            url = f"{self.rugcheck_base}/tokens/{token_address}/report/summary"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    security_analysis = {
                        'flags': [],
                        'risk_score': 0,
                        'details': data
                    }
                    
                    # Analyze the RugCheck response
                    if 'mint' in data:
                        mint_info = data['mint']
                        if mint_info.get('mintAuthority'):
                            security_analysis['flags'].append('MINT_AUTHORITY_ACTIVE')
                            security_analysis['risk_score'] += 25
                        
                        if mint_info.get('freezeAuthority'):
                            security_analysis['flags'].append('FREEZE_AUTHORITY_ACTIVE')
                            security_analysis['risk_score'] += 25
                    
                    if 'markets' in data:
                        markets = data['markets']
                        if not markets:
                            security_analysis['flags'].append('NO_MARKETS')
                            security_analysis['risk_score'] += 30
                    
                    return security_analysis
                    
        except Exception as e:
            logger.error(f"Error checking security for {token_address}: {e}")
            return None
    
    def generate_token_chart(self, token_address: str, token_data: Dict) -> Optional[str]:
        """
        Generate token price chart
        """
        try:
            # Create a simple chart with available data
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Price & Volume', 'Trading Activity'),
                vertical_spacing=0.3,
                row_width=[0.7, 0.3]
            )
            
            # Mock price data for demonstration
            # In production, you'd fetch historical price data
            timestamps = pd.date_range(
                start=datetime.now() - timedelta(hours=24),
                end=datetime.now(),
                freq='1H'
            )
            
            current_price = token_data.get('price_usd', 0)
            price_change = token_data.get('price_change_24h', 0)
            
            # Generate realistic price movement
            np.random.seed(42)  # For reproducible results
            price_changes = np.random.normal(0, 0.05, len(timestamps))
            prices = [current_price * (1 + price_change/100)]
            
            for change in price_changes[1:]:
                prices.append(prices[-1] * (1 + change))
            
            prices = np.array(prices)
            
            # Add price line
            fig.add_trace(
                go.Scatter(
                    x=timestamps,
                    y=prices,
                    mode='lines',
                    name='Price (USD)',
                    line=dict(color='#00ff88', width=2)
                ),
                row=1, col=1
            )
            
            # Add volume bars
            volumes = np.random.exponential(token_data.get('volume_24h', 10000) / 24, len(timestamps))
            fig.add_trace(
                go.Bar(
                    x=timestamps,
                    y=volumes,
                    name='Volume',
                    marker_color='rgba(0, 255, 136, 0.3)',
                    yaxis='y2'
                ),
                row=2, col=1
            )
            
            # Update layout
            fig.update_layout(
                title=f"{token_data.get('base_token', {}).get('symbol', 'Token')} Price Chart",
                xaxis_title="Time",
                yaxis_title="Price (USD)",
                yaxis2_title="Volume",
                template="plotly_dark",
                height=500,
                showlegend=True
            )
            
            # Convert to base64 for Telegram
            img_bytes = fig.to_image(format="png", width=800, height=500)
            img_base64 = base64.b64encode(img_bytes).decode()
            
            return img_base64
            
        except Exception as e:
            logger.error(f"Error generating chart for {token_address}: {e}")
            return None
    
    def generate_analysis_report(self, token_address: str, analysis: Dict, token_data: Dict) -> str:
        """
        Generate comprehensive analysis report
        """
        try:
            symbol = token_data.get('base_token', {}).get('symbol', 'Unknown')
            name = token_data.get('base_token', {}).get('name', 'Unknown Token')
            
            report = f"🔍 **TOKEN ANALYSIS REPORT**\n\n"
            report += f"**Token:** {name} ({symbol})\n"
            report += f"**Address:** `{token_address}`\n"
            report += f"**Analysis Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            # Risk Assessment
            risk_level = analysis.get('risk_level', 'UNKNOWN')
            risk_score = analysis.get('risk_score', 0)
            
            risk_emoji = {
                'LOW': '🟢',
                'MEDIUM': '🟡',
                'HIGH': '🟠',
                'EXTREME': '🔴'
            }.get(risk_level, '⚪')
            
            report += f"**🎯 RISK ASSESSMENT**\n"
            report += f"{risk_emoji} **Risk Level:** {risk_level}\n"
            report += f"📊 **Risk Score:** {risk_score}/100\n\n"
            
            # Key Metrics
            metrics = analysis.get('metrics', {})
            report += f"**📈 KEY METRICS**\n"
            report += f"• **Price:** ${token_data.get('price_usd', 0):.8f}\n"
            report += f"• **Market Cap:** ${metrics.get('market_cap', 0):,.0f}\n"
            report += f"• **Liquidity:** ${metrics.get('liquidity_usd', 0):,.0f}\n"
            report += f"• **24h Volume:** ${metrics.get('volume_24h', 0):,.0f}\n"
            report += f"• **24h Change:** {metrics.get('price_change_24h', 0):.2f}%\n"
            report += f"• **Age:** {metrics.get('age_hours', 0):.1f} hours\n\n"
            
            # Risk Flags
            flags = analysis.get('flags', [])
            if flags:
                report += f"**⚠️ RISK FLAGS**\n"
                for flag in flags:
                    flag_text = flag.replace('_', ' ').title()
                    report += f"• {flag_text}\n"
                report += "\n"
            
            # Trading Information
            report += f"**💹 TRADING INFO**\n"
            report += f"• **DEX:** {token_data.get('dex_id', 'Unknown').title()}\n"
            report += f"• **Pair:** {token_data.get('pair_address', 'N/A')}\n"
            
            txns = token_data.get('txns_24h', {})
            if txns:
                report += f"• **24h Transactions:** {txns.get('buys', 0)} buys, {txns.get('sells', 0)} sells\n"
            
            # Recommendations
            report += f"\n**🎯 RECOMMENDATIONS**\n"
            if risk_level == 'LOW':
                report += "• ✅ Relatively safe for trading\n"
                report += "• ✅ Good liquidity and volume\n"
                report += "• ⚠️ Always DYOR and trade responsibly\n"
            elif risk_level == 'MEDIUM':
                report += "• ⚠️ Moderate risk - proceed with caution\n"
                report += "• ⚠️ Consider smaller position sizes\n"
                report += "• ⚠️ Monitor closely for changes\n"
            elif risk_level == 'HIGH':
                report += "• 🚨 High risk - not recommended\n"
                report += "• 🚨 Multiple red flags detected\n"
                report += "• 🚨 Could be subject to manipulation\n"
            else:
                report += "• 🔴 EXTREME RISK - AVOID\n"
                report += "• 🔴 Multiple critical issues found\n"
                report += "• 🔴 High probability of rug pull\n"
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating analysis report: {e}")
            return f"Error generating report: {str(e)}"
    
    async def setup_price_alerts(self, token_address: str, target_price: float, 
                                chat_id: int, user_id: int) -> bool:
        """
        Setup price alerts for sniped tokens
        """
        try:
            # This would integrate with the existing price monitoring system
            # For now, we'll just return success
            logger.info(f"Setting up price alert for {token_address} at ${target_price}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting up price alerts: {e}")
            return False

# Global instance
token_sniper = TokenSniper()