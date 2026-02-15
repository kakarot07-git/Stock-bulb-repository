"""
Zerodha Kite Connect API Wrapper
Handles authentication and portfolio data retrieval
"""

import logging
import json
import pyotp
from kiteconnect import KiteConnect
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ZerodhaAPI:
    """Wrapper for Zerodha Kite Connect API"""
    
    def __init__(self, config):
        """
        Initialize Zerodha API client
        
        Args:
            config (dict): Configuration containing api_key, api_secret, etc.
        """
        self.api_key = config['api_key']
        self.api_secret = config['api_secret']
        self.user_id = config['user_id']
        self.password = config['password']
        self.totp_secret = config.get('totp_secret', '')
        
        # Initialize KiteConnect
        self.kite = KiteConnect(api_key=self.api_key)
        self.access_token = None
        
        logger.info("Zerodha API initialized")
    
    def authenticate(self, request_token=None):
        """
        Authenticate with Zerodha and generate access token
        
        Args:
            request_token (str): Request token from Kite login redirect
            
        Returns:
            bool: True if authentication successful
        """
        try:
            if request_token:
                # Generate session using request token
                data = self.kite.generate_session(
                    request_token=request_token,
                    api_secret=self.api_secret
                )
                self.access_token = data["access_token"]
                self.kite.set_access_token(self.access_token)
                
                # Save token to file for persistence
                self._save_access_token(self.access_token)
                
                logger.info("✅ Authentication successful")
                return True
            else:
                # Try to load existing token
                token = self._load_access_token()
                if token:
                    self.access_token = token
                    self.kite.set_access_token(token)
                    logger.info("✅ Loaded existing access token")
                    return True
                else:
                    logger.warning("⚠️ No access token found. Run authenticate_zerodha.py first")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Authentication failed: {e}")
            return False
    
    def get_positions(self):
        """
        Get all current positions
        
        Returns:
            list: List of position dictionaries with P&L data
        """
        try:
            positions = self.kite.positions()
            
            # Extract net positions (combined day + overnight)
            net_positions = positions.get('net', [])
            
            if not net_positions:
                logger.info("📊 No open positions found")
                return []
            
            # Format position data
            formatted_positions = []
            for pos in net_positions:
                if pos['quantity'] != 0:  # Only include non-zero positions
                    formatted_positions.append({
                        'symbol': pos['tradingsymbol'],
                        'quantity': pos['quantity'],
                        'average_price': pos['average_price'],
                        'last_price': pos['last_price'],
                        'pnl': pos['pnl'],
                        'day_change': pos['pnl'],
                        'value': pos['value']
                    })
            
            logger.info(f"📊 Found {len(formatted_positions)} positions")
            return formatted_positions
            
        except Exception as e:
            logger.error(f"❌ Error fetching positions: {e}")
            return []
    
    def get_total_pnl(self):
        """
        Calculate total P&L across all positions
        
        Returns:
            float: Total unrealized P&L for the day
        """
        try:
            positions = self.get_positions()
            
            if not positions:
                return 0.0
            
            total_pnl = sum(pos['pnl'] for pos in positions)
            
            logger.info(f"💰 Total P&L: ₹{total_pnl:,.2f}")
            return total_pnl
            
        except Exception as e:
            logger.error(f"❌ Error calculating P&L: {e}")
            return 0.0
    
    def get_portfolio_summary(self):
        """
        Get detailed portfolio summary
        
        Returns:
            dict: Portfolio statistics
        """
        try:
            positions = self.get_positions()
            
            if not positions:
                return {
                    'total_pnl': 0.0,
                    'total_value': 0.0,
                    'position_count': 0,
                    'profitable_positions': 0,
                    'losing_positions': 0
                }
            
            total_pnl = sum(pos['pnl'] for pos in positions)
            total_value = sum(abs(pos['value']) for pos in positions)
            profitable = len([p for p in positions if p['pnl'] > 0])
            losing = len([p for p in positions if p['pnl'] < 0])
            
            summary = {
                'total_pnl': total_pnl,
                'total_value': total_value,
                'position_count': len(positions),
                'profitable_positions': profitable,
                'losing_positions': losing,
                'pnl_percentage': (total_pnl / total_value * 100) if total_value > 0 else 0
            }
            
            logger.info(f"📈 Portfolio: {profitable} winning, {losing} losing")
            return summary
            
        except Exception as e:
            logger.error(f"❌ Error getting portfolio summary: {e}")
            return None
    
    def get_login_url(self):
        """
        Get Kite Connect login URL
        
        Returns:
            str: Login URL for browser authentication
        """
        login_url = self.kite.login_url()
        logger.info(f"🔗 Login URL generated: {login_url}")
        return login_url
    
    def _save_access_token(self, token):
        """Save access token to file"""
        try:
            with open('access_token.txt', 'w') as f:
                f.write(token)
            logger.info("💾 Access token saved")
        except Exception as e:
            logger.error(f"❌ Error saving token: {e}")
    
    def _load_access_token(self):
        """Load access token from file"""
        try:
            with open('access_token.txt', 'r') as f:
                token = f.read().strip()
            logger.info("📂 Access token loaded from file")
            return token
        except FileNotFoundError:
            logger.warning("⚠️ No saved access token found")
            return None
        except Exception as e:
            logger.error(f"❌ Error loading token: {e}")
            return None
    
    def is_authenticated(self):
        """
        Check if currently authenticated
        
        Returns:
            bool: True if access token is set
        """
        return self.access_token is not None


if __name__ == "__main__":
    # Test the API
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    with open('config.json') as f:
        config = json.load(f)
    
    api = ZerodhaAPI(config['zerodha'])
    
    if api.authenticate():
        print("\n✅ Authentication successful!")
        
        # Get positions
        positions = api.get_positions()
        print(f"\n📊 Positions: {len(positions)}")
        for pos in positions:
            pnl_symbol = "📈" if pos['pnl'] > 0 else "📉"
            print(f"{pnl_symbol} {pos['symbol']}: ₹{pos['pnl']:,.2f}")
        
        # Get total P&L
        total_pnl = api.get_total_pnl()
        print(f"\n💰 Total P&L: ₹{total_pnl:,.2f}")
        
        # Get summary
        summary = api.get_portfolio_summary()
        if summary:
            print(f"\n📈 Summary:")
            print(f"   Positions: {summary['position_count']}")
            print(f"   Winning: {summary['profitable_positions']}")
            print(f"   Losing: {summary['losing_positions']}")
            print(f"   P&L %: {summary['pnl_percentage']:.2f}%")
    else:
        print("\n❌ Authentication failed. Run authenticate_zerodha.py first")
