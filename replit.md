# TONY_M3TA_BOT - Cryptocurrency Price Monitoring Bot

## Overview

TONY_M3TA_BOT is a Telegram bot designed for cryptocurrency price monitoring and alert management. The bot allows users to set price alerts for various cryptocurrencies and receive notifications when target prices are reached. It integrates with the CoinGecko API for real-time price data and uses in-memory storage for managing user watch lists.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

- **main.py**: Entry point and application orchestration
- **bot/**: Core bot functionality including handlers, price monitoring, and storage
- **utils/**: Utility functions and logging configuration
- **config.py**: Centralized configuration management

The system uses an event-driven architecture with asynchronous operations for handling Telegram updates and price monitoring tasks concurrently.

## Key Components

### 1. Bot Handlers (`bot/handlers.py`)
- **Purpose**: Handle Telegram bot commands and user interactions
- **Key Commands**: `/start`, `/snipe`, `/list`, `/remove`, `/help`
- **Architecture Decision**: Command-based interface provides intuitive user experience
- **Rationale**: Simple command structure makes the bot easy to use for crypto enthusiasts

### 2. Price Monitor (`bot/price_monitor.py`)
- **Purpose**: Continuously monitor cryptocurrency prices and trigger alerts
- **Architecture Decision**: Asynchronous monitoring with configurable intervals
- **Features**: Price caching, rate limiting, and background task execution
- **Rationale**: Prevents API rate limiting while ensuring timely price updates

### 3. Storage System (`bot/storage.py`)
- **Purpose**: Manage user watch lists and alert configurations
- **Architecture Decision**: In-memory storage with thread-safe operations
- **Trade-offs**: 
  - Pros: Fast access, no database dependencies
  - Cons: Data lost on restart, not suitable for production scale
- **Rationale**: Simple solution for MVP and development phases

### 4. Configuration Management (`config.py`)
- **Purpose**: Centralize all configuration settings
- **Architecture Decision**: Environment variable-based configuration
- **Features**: Type conversion, validation, and feature flags
- **Rationale**: Enables easy deployment across different environments

### 5. Logging System (`utils/logger.py`)
- **Purpose**: Structured logging for monitoring and debugging
- **Architecture Decision**: Centralized logger configuration
- **Features**: Formatted output, multiple log levels, API call tracking
- **Rationale**: Essential for debugging and monitoring bot operations

## Data Flow

1. **User Command**: User sends command via Telegram
2. **Command Processing**: Bot handlers process and validate commands
3. **Storage Operations**: Watch data is stored/retrieved from in-memory storage
4. **Price Monitoring**: Background task continuously checks prices via CoinGecko API
5. **Alert Triggering**: When target prices are reached, notifications are sent
6. **Logging**: All operations are logged for monitoring and debugging

## External Dependencies

### CoinGecko API
- **Purpose**: Real-time cryptocurrency price data
- **Architecture Decision**: Free tier usage with optional API key support
- **Rate Limiting**: 50 requests per minute (configurable)
- **Rationale**: Reliable, comprehensive cryptocurrency data source

### Telegram Bot API
- **Purpose**: Bot communication interface
- **Architecture Decision**: Official python-telegram-bot library
- **Features**: Command handling, message sending, user management
- **Rationale**: Well-maintained library with excellent documentation

### AsyncIO & aiohttp
- **Purpose**: Asynchronous operations for API calls and concurrent tasks
- **Architecture Decision**: Full async implementation
- **Rationale**: Enables handling multiple users and price monitoring simultaneously

## Deployment Strategy

### Current Configuration
- **Environment**: Development/Testing phase
- **Storage**: In-memory (temporary)
- **Monitoring**: Basic logging to console
- **Scalability**: Single instance deployment

### Production Considerations
- **Database**: Would require persistent storage (SQLite, PostgreSQL)
- **Monitoring**: Enhanced logging and metrics collection
- **Scalability**: Container-based deployment with load balancing
- **Security**: Secure token management and API key rotation

## Changelog
- July 07, 2025. Initial setup with comprehensive bot architecture
- July 07, 2025. Simplified to basic bot with /start and /snipe commands using python-telegram-bot v13.15
- July 07, 2025. Added instant take profits button and comprehensive popup menu with live tokenomics
- July 07, 2025. Implemented currency amount support for sniping (£, $, €, SOL) and comprehensive snipe management system with live charts and P&L tracking

## User Preferences

Preferred communication style: Simple, everyday language.

## Current Implementation Status

The bot is now running with comprehensive crypto functionality:

### Core Features
- Uses python-telegram-bot v13.15 with Updater syntax
- Phantom wallet integration with real Solana blockchain connectivity
- Complete Solana DEX integration with Jupiter, Raydium, and Orca
- **NEW: Advanced Token Sniping System with DexScreener Integration**

### Commands Available
**Basic Commands:**
- /start - Initialize bot and add wallet
- /commands - Show complete command list

**Wallet Management:**
- /wallet, /wallet add, /wallet balance, /portfolio
- /wallet tokens - Show all crypto assets with real-time prices
- Real-time SOL balance and complete token portfolio tracking

**DEX Trading:**
- /dex, /dex quote, /dex price, /dex pairs, /dex pools, /dex markets
- Real-time swap quotes and token pricing from live DEX APIs

**Advanced Token Sniping & Analysis:**
- /snipe_new - Scan and analyze newest tokens with comprehensive risk assessment
- /snipe_trending - Find safe trending tokens with automated filtering
- /analyze TOKEN_ADDRESS - Deep tokenomics analysis with charts and risk scoring
- /rugcheck TOKEN_ADDRESS - Comprehensive rug pull protection analysis
- /snipe TOKEN PRICE - Set price alerts (existing functionality)

### Technical Architecture Additions

**New Module: bot/token_sniping.py**
- TokenSniper class with DexScreener API integration
- Comprehensive tokenomics analysis engine
- Rug pull detection using RugCheck API
- Interactive chart generation with Plotly
- Risk scoring algorithm with weighted factors
- Real-time security analysis

**Key Features:**
- DexScreener API integration for token discovery
- RugCheck API integration for security analysis
- Plotly chart generation for price visualization
- Comprehensive risk assessment with 6-factor scoring
- Real-time tokenomics analysis including liquidity, volume, market cap
- Automated rug pull detection with authority checks
- Support for major Solana tokens: SOL, USDC, USDT, RAY, ORCA, BONK, WIF, MEME

### Security & Risk Management
- Multi-layer rug pull detection
- Mint and freeze authority checking
- Liquidity and volume analysis
- Token age and volatility assessment
- Social presence verification
- Automated risk level classification (LOW/MEDIUM/HIGH/EXTREME)

Ready for testing comprehensive token sniping functionality on Telegram