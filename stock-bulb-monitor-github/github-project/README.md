# 📊💡 Stock Bulb Monitor

> Real-time stock portfolio monitoring with smart bulb visualization

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production-success.svg)]()

A fully automated system that monitors your Zerodha stock portfolio and controls a WiZ smart bulb based on your daily P&L. Get instant visual feedback without checking your phone!

<div align="center">
  <h3>🟢 Green = Profit | 🔴 Red = Loss | 🔵 Blue = Break-even</h3>
</div>

---

## ✨ Features

- 🔄 **Real-time Monitoring** - Checks portfolio every 5 minutes during market hours
- 💡 **Visual Feedback** - Color-coded bulb instantly shows profit/loss status
- 🎨 **Brightness Scaling** - Brightness adjusts based on profit/loss magnitude
- ⏰ **Smart Scheduling** - Only runs during market hours (9:15 AM - 3:30 PM IST)
- 🛡️ **Error Handling** - Graceful recovery from network failures
- 📝 **Comprehensive Logging** - Track all activity and debug issues
- 🎯 **Market Detection** - Automatically detects weekends and holidays

## 📸 Demo

```
Market Opens → Check Portfolio → Calculate P&L → Update Bulb Color
     ↓              ↓                 ↓              ↓
  9:15 AM      Every 5 mins       Real-time      🟢/🔴/🔵
```

**Your trading day at a glance:**
- Sit at your desk
- Bulb changes color automatically
- Know your P&L status without breaking focus
- No more constant phone checking!

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Zerodha account with [Kite Connect API](https://kite.trade/) (₹2,000/month)
- WiZ smart bulb (any color bulb)
- Computer on same WiFi as bulb

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/stock-bulb-monitor.git
   cd stock-bulb-monitor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your credentials**
   
   Edit `config.json`:
   ```json
   {
     "zerodha": {
       "api_key": "YOUR_API_KEY",
       "api_secret": "YOUR_SECRET",
       "user_id": "YOUR_USER_ID",
       "password": "YOUR_PASSWORD"
     },
     "wiz": {
       "bulb_ip": "192.168.1.XXX"
     }
   }
   ```

4. **Setup WiZ bulb**
   ```bash
   python setup_wiz.py
   ```

5. **Authenticate with Zerodha**
   ```bash
   python authenticate_zerodha.py
   ```

6. **Run the monitor**
   ```bash
   python main.py
   ```

## 📖 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - 15-minute setup
- **[Configuration Guide](docs/CONFIGURATION.md)** - Detailed configuration options
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[API Documentation](docs/API.md)** - Zerodha and WiZ API details

## 🛠️ Architecture

```
┌─────────────────┐
│  Zerodha Kite   │
│   Connect API   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Python Monitor  │
│   (main.py)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   WiZ Bulb      │
│  (UDP/WiFi)     │
└─────────────────┘
```

### Components

- **`main.py`** - Main monitoring service with scheduling
- **`zerodha_api.py`** - Zerodha Kite Connect API wrapper
- **`wiz_api.py`** - WiZ smart bulb controller (UDP protocol)
- **`authenticate_zerodha.py`** - Daily authentication helper
- **`setup_wiz.py`** - One-time bulb configuration
- **`test_bulb.py`** - Interactive bulb testing tool

## ⚙️ Configuration

### Market Hours
```json
"settings": {
  "check_interval_seconds": 300,
  "market_open_time": "09:15",
  "market_close_time": "15:30",
  "timezone": "Asia/Kolkata"
}
```

### Color Thresholds
```json
"color_thresholds": {
  "huge_profit": 10000,    // ₹10k+ = Max brightness
  "profit": 0,             // Any profit = Green
  "loss": 0,               // Any loss = Red
  "huge_loss": -10000      // ₹-10k = Max brightness
}
```

## 🧪 Testing

**Test WiZ bulb connection:**
```bash
python test_bulb.py
```

**Test Zerodha API:**
```bash
python zerodha_api.py
```

## 📊 Daily Usage

1. **Morning (before 9:15 AM)**
   ```bash
   python authenticate_zerodha.py  # Takes 30 seconds
   python main.py                   # Start monitoring
   ```

2. **During trading hours**
   - Monitor runs automatically
   - Bulb updates every 5 minutes
   - Logs saved to `stock_monitor.log`

3. **After market close**
   - Bulb turns off automatically
   - Press `Ctrl+C` to stop

## 🔍 Troubleshooting

### Common Issues

**"Cannot connect to WiZ bulb"**
- Check bulb is powered on
- Verify IP address in config
- Ensure same WiFi network
- Run `python setup_wiz.py`

**"Authentication failed"**
- Verify API credentials
- Check Kite subscription is active
- Run `python authenticate_zerodha.py` again

**"No positions found"**
- Ensure you have open positions
- Check market is open (9:15 AM - 3:30 PM, weekdays)

For more solutions, see [Troubleshooting Guide](docs/TROUBLESHOOTING.md).

## 💰 Costs

- **Zerodha Kite Connect API**: ₹2,000/month
- **WiZ Smart Bulb**: ₹500-2,000 (one-time)
- **Everything else**: Free

### Free Alternative
Consider [Angel One SmartAPI](https://smartapi.angelbroking.com/) - completely FREE alternative to Zerodha.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Ideas for Contributions
- [ ] Support for Angel One API (FREE)
- [ ] Web dashboard
- [ ] Telegram notifications
- [ ] Multiple bulb support
- [ ] Historical P&L tracking
- [ ] Docker containerization

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is for personal portfolio monitoring only. It does not:
- Provide financial advice
- Execute trades
- Guarantee accuracy
- Come with any warranty

Use at your own risk. Always verify information independently.

## 🙏 Acknowledgments

- Built with [Claude](https://claude.ai) (Anthropic)
- [Zerodha Kite Connect](https://kite.trade/) for API access
- [WiZ Connected](https://www.wizconnected.com/) for smart bulb
- Python community for excellent libraries

## 📬 Contact

Have questions or suggestions? Open an issue on GitHub!

---

<div align="center">
  <strong>⭐ If this project helps you, consider giving it a star! ⭐</strong>
</div>

---

**Built with ❤️ by a PM who codes with AI**
