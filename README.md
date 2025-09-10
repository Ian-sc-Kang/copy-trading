# Discord Trading Bot with TD Ameritrade Integration

A Python-based automated trading bot that monitors Discord channels for trading signals and executes trades via the TD Ameritrade API. The bot reads trading callouts (options trades) from a designated Discord channel and automatically places corresponding orders in your TD Ameritrade account.

## ⚠️ Important Disclaimers

- **Risk Warning**: Automated trading involves significant financial risk. Use this bot at your own risk.
- **Paper Trading**: Consider testing with a paper trading account first.
- **Educational Purpose**: This project is for educational and research purposes.
- **Not Financial Advice**: This bot does not provide financial advice.

## Features

- **Real-time Discord Monitoring**: Monitors Discord channels for trading signals using web scraping
- **Options Trading**: Automatically parses and executes options trading callouts (BTO/STC)
- **TD Ameritrade Integration**: Places orders through TD Ameritrade's official API
- **Position Sizing**: Calculates position sizes based on account balance and risk parameters
- **Error Handling**: Comprehensive error handling and status reporting
- **Notification System**: Discord bot notifications for trade confirmations and errors

## How It Works

1. **Monitor**: Bot monitors a specified Discord channel for trading messages
2. **Parse**: Parses trading callouts in format: `BTO/STC TICKER STRIKE_PRICE[P/C] MM/DD PRICE`
3. **Execute**: Places corresponding orders via TD Ameritrade API
4. **Notify**: Sends confirmation messages to a Discord notification channel

### Example Trading Callout
```
BTO AAPL 150C 12/15 $2.50 (small position)
```
This would:
- Buy to Open (BTO)
- AAPL call option 
- $150 strike price
- Expiring 12/15
- At $2.50 limit price
- With small position sizing

## Prerequisites

- Python 3.8+
- TD Ameritrade brokerage account with API access
- Discord bot token and server access
- Chrome browser installed (ChromeDriver is automatically managed)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/copy-trading.git
   cd copy-trading
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   **Note**: ChromeDriver is automatically downloaded and managed by Selenium Manager. No manual setup required!

## Configuration

1. **Copy environment template**:
   ```bash
   cp .env.example .env
   ```

2. **Configure environment variables** (edit `.env`):

   **Discord Configuration**:
   - `DISCORD_BOT_TOKEN`: Your Discord bot token
   - `DISCORD_NOTIFICATION_CHANNEL_ID`: Channel ID for notifications
   - `DISCORD_SERVER_ID`: Server ID containing the trading channel
   - `DISCORD_CHANNEL_ID`: Channel ID to monitor for trading signals
   - `EMAIL`: Your Discord account email (for web scraping)
   - `PASSWORD`: Your Discord account password (for web scraping)

   **TD Ameritrade Configuration**:
   - `TD_ACCESS_TOKEN`: Your TD Ameritrade access token
   - `TD_ACCOUNT_ID`: Your TD Ameritrade account ID
   - `TD_CONSUMER_KEY`: Your TD Ameritrade consumer key
   - `TD_REFRESH_TOKEN`: Your TD Ameritrade refresh token

### Setting up TD Ameritrade API Access

1. Create a TD Ameritrade developer account at [developer.tdameritrade.com](https://developer.tdameritrade.com/)
2. Register a new app to get your consumer key
3. Follow TD Ameritrade's OAuth2 flow to get access and refresh tokens
4. Ensure your account has options trading enabled

### Setting up Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application and bot
3. Get your bot token and add the bot to your server
4. Grant necessary permissions (read messages, send messages)

## Usage

1. **Start the bot**:
   ```bash
   python main.py
   ```

2. **The bot will**:
   - Connect to Discord and start monitoring the specified channel
   - Display status messages in the console
   - Send notifications to the Discord notification channel
   - Automatically execute trades when valid callouts are detected

3. **Stop the bot**:
   - Use `Ctrl+C` to stop the bot gracefully
   - The bot will automatically shut down after 6.5 hours (market hours)

## Testing

1. **Test Discord connection**:
   - Ensure the bot comes online in your Discord server
   - Check that it can read messages from the monitored channel

2. **Test API connections**:
   - Verify TD Ameritrade API credentials work
   - Test with small position sizes initially

3. **Test trading logic**:
   - Use paper trading account if available
   - Start with very small position sizes
   - Monitor logs for any errors

## Supported Trading Callout Formats

The bot recognizes these patterns:
- `BTO TICKER STRIKEP/C MM/DD PRICE` - Buy to Open
- `STC TICKER STRIKEP/C MM/DD PRICE` - Sell to Close

**Position Sizing Modifiers** (in parentheses):
- `(small)` - 1% of account value
- `(half)` or `(50%)` - 1% of account value  
- `(risky)`, `(slow)`, `(lotto)` - 1% of account value
- Default - 1% of account value

**Example Valid Callouts**:
```
BTO TSLA 800C 1/20 $15.00 (small position)
STC AAPL 145P 12/31 $3.25
BTO SPY 420C 12/17 $2.50 (half position)
```

## File Structure

```
copy-trading/
├── main.py              # Main bot entry point
├── Kindred.py           # Core trading logic and Discord monitoring
├── TD_Client.py         # TD Ameritrade API client
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not committed)
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore patterns
└── README.md           # This file
```

## Error Handling

The bot includes comprehensive error handling for:
- Invalid trading callout formats
- TD Ameritrade API errors (401, 403, 500, etc.)
- Network connectivity issues
- Position not found errors
- Discord connection issues

All errors are logged to console and Discord notifications.

## Security Considerations

- Never commit `.env` file or real credentials
- Use secure environment variable storage in production
- Consider using a dedicated trading account
- Regularly rotate API tokens
- Monitor account activity regularly

## Contributing

This is an educational project. If you'd like to contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. Use at your own risk.

## Support

⚠️ **Important**: This bot handles real money transactions. Please:
- Test thoroughly before using with real money
- Start with small position sizes
- Monitor the bot actively during operation
- Have a plan to manually intervene if needed
