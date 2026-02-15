"""
WiZ Smart Bulb Setup
Run this once to configure your WiZ bulb connection
"""

import json
import time
from wiz_api import WiZController
from colorama import Fore, Style, init

init(autoreset=True)


def setup_wiz():
    """Interactive WiZ bulb setup"""
    
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"💡 WiZ Smart Bulb Setup")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    # Load config
    try:
        with open('config.json') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"{Fore.RED}❌ config.json not found!{Style.RESET_ALL}")
        return
    
    wiz_config = config.get('wiz', {})
    
    # Get bulb IP
    print(f"{Fore.YELLOW}Step 1: Find Your WiZ Bulb IP Address{Style.RESET_ALL}\n")
    
    print("To find your bulb's IP address:")
    print("1. Open the WiZ app on your phone")
    print("2. Tap on your bulb")
    print("3. Tap the settings/gear icon")
    print("4. Look for 'IP Address' or 'Device Info'\n")
    
    current_ip = wiz_config.get('bulb_ip', '')
    if current_ip:
        print(f"Current IP in config: {Fore.CYAN}{current_ip}{Style.RESET_ALL}")
        use_current = input(f"Use this IP? (y/n, default: y): ").strip().lower()
        if use_current != 'n':
            bulb_ip = current_ip
        else:
            bulb_ip = input(f"Enter your WiZ bulb IP address: ").strip()
    else:
        bulb_ip = input(f"Enter your WiZ bulb IP address (e.g., 192.168.1.50): ").strip()
    
    if not bulb_ip:
        print(f"{Fore.RED}❌ IP address is required{Style.RESET_ALL}")
        return
    
    wiz_config['bulb_ip'] = bulb_ip
    print(f"{Fore.GREEN}✓ Bulb IP: {bulb_ip}{Style.RESET_ALL}\n")
    
    # Test connection
    print(f"{Fore.YELLOW}Step 2: Testing Connection{Style.RESET_ALL}\n")
    
    wiz = WiZController(wiz_config)
    
    if not wiz.test_connection():
        print(f"\n{Fore.RED}❌ Failed to connect to bulb{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Troubleshooting:{Style.RESET_ALL}")
        print("• Make sure bulb is powered on")
        print("• Check IP address is correct")
        print("• Ensure computer and bulb are on same WiFi")
        print("• Try turning bulb off/on in WiZ app")
        return
    
    # Save configuration
    config['wiz'] = wiz_config
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n{Fore.GREEN}✓ Configuration saved to config.json{Style.RESET_ALL}\n")
    
    # Test colors
    print(f"{Fore.YELLOW}Step 3: Testing Bulb Control{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}Testing colors...{Style.RESET_ALL}\n")
    
    colors = [
        ('GREEN', 'green', 'Profit! 📈'),
        ('RED', 'red', 'Loss! 📉'),
        ('BLUE', 'blue', 'Break-even ⚖️')
    ]
    
    for color_name, color_code, description in colors:
        print(f"{Fore.CYAN}→ {color_name}: {description}{Style.RESET_ALL}")
        wiz.set_color(color_code, brightness=80)
        time.sleep(2)
    
    print(f"\n{Fore.GREEN}{'='*60}")
    print(f"✅ SETUP COMPLETE!")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    print(f"{Fore.GREEN}✓{Style.RESET_ALL} WiZ bulb configured")
    print(f"{Fore.GREEN}✓{Style.RESET_ALL} Connection tested successfully")
    print(f"\n{Fore.YELLOW}Next steps:{Style.RESET_ALL}")
    print(f"1. Run: {Fore.CYAN}python authenticate_zerodha.py{Style.RESET_ALL}")
    print(f"2. Then: {Fore.CYAN}python main.py{Style.RESET_ALL}\n")


if __name__ == "__main__":
    setup_wiz()
