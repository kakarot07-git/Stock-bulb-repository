"""
Zerodha Authentication Setup
Run this once daily to authenticate with Kite Connect
"""

import json
import webbrowser
import logging
from zerodha_api import ZerodhaAPI
from colorama import Fore, Style, init

init(autoreset=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def authenticate():
    """Run Zerodha authentication flow"""
    
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"🔐 Zerodha Kite Connect Authentication")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    # Load config
    try:
        with open('config.json') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"{Fore.RED}❌ config.json not found!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please create config.json first{Style.RESET_ALL}")
        return
    
    # Initialize API
    api = ZerodhaAPI(config['zerodha'])
    
    # Get login URL
    login_url = api.get_login_url()
    
    print(f"{Fore.YELLOW}📋 INSTRUCTIONS:{Style.RESET_ALL}")
    print(f"1. Your browser will open with Kite login page")
    print(f"2. Login with your Zerodha credentials")
    print(f"3. After login, you'll be redirected to a URL")
    print(f"4. Copy the FULL URL from your browser")
    print(f"5. Paste it here\n")
    
    input(f"{Fore.GREEN}Press ENTER to open login page...{Style.RESET_ALL}")
    
    # Open browser
    webbrowser.open(login_url)
    
    print(f"\n{Fore.CYAN}⏳ Waiting for you to complete login...{Style.RESET_ALL}\n")
    
    # Get redirect URL from user
    redirect_url = input(f"{Fore.YELLOW}Paste the full redirect URL here: {Style.RESET_ALL}").strip()
    
    # Extract request token
    try:
        # URL format: http://127.0.0.1:5000/?request_token=XXX&action=login&status=success
        request_token = redirect_url.split('request_token=')[1].split('&')[0]
        print(f"\n{Fore.GREEN}✅ Request token extracted: {request_token[:10]}...{Style.RESET_ALL}")
    except IndexError:
        print(f"\n{Fore.RED}❌ Invalid URL format!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}The URL should contain 'request_token='{Style.RESET_ALL}")
        return
    
    # Authenticate
    print(f"\n{Fore.CYAN}🔄 Generating access token...{Style.RESET_ALL}")
    
    if api.authenticate(request_token=request_token):
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"✅ AUTHENTICATION SUCCESSFUL!")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Access token saved to access_token.txt")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Valid for today's trading session")
        print(f"{Fore.YELLOW}⚠️{Style.RESET_ALL}  You'll need to re-authenticate tomorrow morning\n")
        
        # Test the connection
        print(f"{Fore.CYAN}🧪 Testing connection...{Style.RESET_ALL}\n")
        
        positions = api.get_positions()
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Found {len(positions)} positions")
        
        total_pnl = api.get_total_pnl()
        
        if total_pnl > 0:
            print(f"{Fore.GREEN}✓ Total P&L: ₹{total_pnl:,.2f} 📈{Style.RESET_ALL}")
        elif total_pnl < 0:
            print(f"{Fore.RED}✓ Total P&L: ₹{total_pnl:,.2f} 📉{Style.RESET_ALL}")
        else:
            print(f"{Fore.BLUE}✓ Total P&L: ₹{total_pnl:,.2f} ⚖️{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}🚀 You're ready to run: python main.py{Style.RESET_ALL}\n")
        
    else:
        print(f"\n{Fore.RED}❌ Authentication failed!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please check your API credentials in config.json{Style.RESET_ALL}\n")


if __name__ == "__main__":
    authenticate()
