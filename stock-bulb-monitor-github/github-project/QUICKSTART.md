# Quick Start Guide 🚀
## WiZ Smart Bulb Version

Get your stock bulb monitor running in 10 minutes with your existing WiZ bulb!

## TL;DR - Super Quick Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Test WiZ bulb (IP already configured!)
python setup_wiz.py

# 3. Edit config.json with your Zerodha credentials

# 4. Authenticate
python authenticate_zerodha.py

# 5. Run!
python main.py
```

---

## What Makes This Different?

✅ **Your bulb IP is already configured**: 192.168.29.111  
✅ **No bridge needed** - WiZ connects via WiFi directly  
✅ **Works with your Philips A60 WiZ bulb**  

---

## 5-Minute Setup

### 1️⃣ Install Python Packages (1 min)

Open terminal in the `stock-bulb-monitor-wiz` folder:

```bash
pip install -r requirements.txt
```

### 2️⃣ Test WiZ Connection (1 min)

```bash
python setup_wiz.py
```

Your bulb IP (192.168.29.111) is already saved!

**You'll see:**
- Connection test
- Bulb cycling through GREEN → RED → BLUE
- If successful: ✅ Setup complete!

**If connection fails:**
- Make sure bulb is on
- Check computer is on same WiFi (192.168.29.x network)
- Verify bulb IP hasn't changed in WiZ app

### 3️⃣ Add Zerodha Credentials (2 mins)

Edit `config.json`:

```json
{
  "zerodha": {
    "api_key": "YOUR_API_KEY_HERE",      ← From kite.trade
    "api_secret": "YOUR_SECRET_HERE",    ← From kite.trade  
    "user_id": "AB1234",                  ← Your Zerodha ID
    "password": "your_password",          ← Kite password
    "totp_secret": ""                     ← Leave empty
  }
}
```

Don't change the `wiz` section - it's already configured!

### 4️⃣ Authenticate (1 min)

```bash
python authenticate_zerodha.py
```

- Browser opens → Login to Kite
- Copy redirect URL
- Paste in terminal
- Done! ✅

### 5️⃣ Start Monitoring!

```bash
python main.py
```

**You should see:**
```
🚀 Stock Bulb Monitor Starting (WiZ Version)...
💡 WiZ Controller initialized (Bulb: 192.168.29.111)
📊 Checking portfolio...
💰 Total P&L: ₹1,234.50
✅ PROFIT → GREEN bulb
```

---

## What Happens Now?

🔄 **Every 5 minutes**:
- Checks your Zerodha portfolio
- Calculates total P&L
- Updates WiZ bulb color

🟢 **GREEN** = Making money  
🔴 **RED** = Losing money  
🔵 **BLUE** = Break-even  

---

## Daily Routine

**Every morning before 9:15 AM:**

```bash
python authenticate_zerodha.py
python main.py
```

That's it! Let it run all day.

---

## Testing Your Bulb

Want to test the bulb manually?

```bash
python test_bulb.py
```

Interactive menu to:
- Test all colors
- Simulate profit/loss scenarios
- Pulse effects
- Manual control

---

## Troubleshooting

### Bulb not responding?

**Check IP address:**
1. Open WiZ app
2. Tap your bulb
3. Go to Settings → Device Info
4. Find IP address
5. If different from 192.168.29.111, update config.json:

```json
"wiz": {
  "bulb_ip": "NEW_IP_HERE"
}
```

**Quick fixes:**
- Power cycle the bulb (turn off/on)
- Restart your router
- Make sure WiZ app can control it
- Check you're on 2.4GHz WiFi (WiZ doesn't work on 5GHz)

### Zerodha authentication failed?

```bash
python authenticate_zerodha.py
```

- Copy the FULL URL (from http:// to end)
- Check API key/secret are correct

---

## WiZ Bulb Tips

💡 **Static IP recommended**: Set a static IP for your bulb in router settings so it doesn't change

📶 **WiFi band**: WiZ bulbs only work on 2.4GHz WiFi, not 5GHz

🔌 **Keep powered**: Don't use physical switch - bulb needs constant power

⚡ **Response time**: WiZ responds almost instantly (UDP, not cloud)

---

## File Overview

| File | What it does |
|------|-------------|
| `wiz_api.py` | Controls your WiZ bulb |
| `zerodha_api.py` | Gets portfolio from Zerodha |
| `main.py` | Main monitoring loop |
| `setup_wiz.py` | Test WiZ connection |
| `test_bulb.py` | Manual bulb control |
| `config.json` | Your settings (IP pre-filled!) |

---

## Your Setup Summary

✅ **Bulb Model**: Philips A60 WiZ  
✅ **Bulb IP**: 192.168.29.111 (already configured)  
✅ **Connection**: Direct WiFi (no bridge needed)  
✅ **Cost**: ₹0 hardware (using existing bulb!)  

---

## Next Steps

1. **Today**: Get it running following steps above
2. **Tomorrow**: Re-authenticate before market (daily requirement)
3. **Ongoing**: Let it run automatically during market hours

---

**That's it! You're trading with visual feedback! 🎉**

May your bulb glow green all day! 🟢📈
