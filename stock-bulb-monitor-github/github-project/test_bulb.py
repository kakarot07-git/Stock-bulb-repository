"""
Quick WiZ Bulb Test Script
Test your WiZ bulb controls
"""

import json
import time
from wiz_api import WiZController
from colorama import Fore, Style, init

init(autoreset=True)


def test_bulb():
    """Test bulb with various colors and effects"""
    
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"🧪 WiZ Bulb Test")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    # Load config
    try:
        with open('config.json') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"{Fore.RED}❌ config.json not found!{Style.RESET_ALL}")
        return
    
    # Initialize WiZ
    wiz = WiZController(config['wiz'])
    
    # Test connection
    if not wiz.test_connection():
        print(f"{Fore.RED}❌ Cannot connect to bulb{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Run: python setup_wiz.py{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.GREEN}✅ Connected to bulb!{Style.RESET_ALL}\n")
    
    # Menu
    while True:
        print(f"{Fore.CYAN}Choose a test:{Style.RESET_ALL}")
        print(f"1. Test all colors")
        print(f"2. Test P&L colors (profit/loss simulation)")
        print(f"3. Test pulse effect")
        print(f"4. Manual color picker")
        print(f"5. Turn off and exit")
        
        choice = input(f"\n{Fore.YELLOW}Enter choice (1-5): {Style.RESET_ALL}").strip()
        
        if choice == '1':
            print(f"\n{Fore.CYAN}Testing all colors...{Style.RESET_ALL}\n")
            colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'white']
            for color in colors:
                print(f"  → {color.upper()}")
                wiz.set_color(color, brightness=80)
                time.sleep(2)
        
        elif choice == '2':
            print(f"\n{Fore.CYAN}Simulating P&L scenarios...{Style.RESET_ALL}\n")
            
            scenarios = [
                (5000, f"{Fore.GREEN}Profit: ₹5,000{Style.RESET_ALL}"),
                (-3000, f"{Fore.RED}Loss: ₹-3,000{Style.RESET_ALL}"),
                (0, f"{Fore.BLUE}Break-even: ₹0{Style.RESET_ALL}"),
                (15000, f"{Fore.GREEN}Huge Profit: ₹15,000{Style.RESET_ALL}"),
                (-12000, f"{Fore.RED}Huge Loss: ₹-12,000{Style.RESET_ALL}"),
            ]
            
            thresholds = config.get('color_thresholds', {})
            
            for pnl, description in scenarios:
                print(f"  → {description}")
                wiz.set_color_for_pnl(pnl, thresholds)
                time.sleep(3)
        
        elif choice == '3':
            print(f"\n{Fore.CYAN}Testing pulse effect...{Style.RESET_ALL}\n")
            color = input(f"Color to pulse (red/green/blue): ").strip() or 'green'
            times = int(input(f"Number of pulses (1-5): ").strip() or '3')
            
            print(f"Pulsing {color} {times} times...")
            wiz.pulse(color, times=times)
        
        elif choice == '4':
            print(f"\n{Fore.CYAN}Manual color picker{Style.RESET_ALL}\n")
            print(f"Available colors: red, green, blue, yellow, orange, purple, white")
            color = input(f"Enter color: ").strip()
            brightness = int(input(f"Brightness (10-100, default 80): ").strip() or '80')
            
            wiz.set_color(color, brightness=brightness)
            print(f"{Fore.GREEN}✓ Color set!{Style.RESET_ALL}")
        
        elif choice == '5':
            wiz.turn_off()
            print(f"\n{Fore.GREEN}✓ Bulb turned off. Goodbye! 👋{Style.RESET_ALL}\n")
            break
        
        else:
            print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")
        
        print()


if __name__ == "__main__":
    test_bulb()
