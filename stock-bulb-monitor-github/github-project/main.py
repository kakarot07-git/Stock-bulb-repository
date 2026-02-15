"""
Stock Bulb Monitor - Main Application (WiZ Version)
Monitors Zerodha portfolio and controls WiZ smart bulb based on P&L
"""

import logging
import json
import time
import signal
import sys
from datetime import datetime, time as dt_time
import pytz
from colorama import Fore, Style, init

from zerodha_api import ZerodhaAPI
from wiz_api import WiZController

# Initialize colorama for colored console output
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('stock_monitor.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class StockBulbMonitor:
    """Main monitoring service"""
    
    def __init__(self, config_path='config.json'):
        """
        Initialize the monitor
        
        Args:
            config_path (str): Path to configuration file
        """
        logger.info("=" * 60)
        logger.info("🚀 Stock Bulb Monitor Starting (WiZ Version)...")
        logger.info("=" * 60)
        
        # Load configuration
        with open(config_path) as f:
            self.config = json.load(f)
        
        # Initialize APIs
        self.zerodha = ZerodhaAPI(self.config['zerodha'])
        self.wiz = WiZController(self.config['wiz'])
        
        # Settings
        self.check_interval = self.config['settings']['check_interval_seconds']
        self.market_open = self._parse_time(self.config['settings']['market_open_time'])
        self.market_close = self._parse_time(self.config['settings']['market_close_time'])
        self.timezone = pytz.timezone(self.config['settings']['timezone'])
        
        # State tracking
        self.last_pnl = None
        self.running = True
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info(f"⏰ Market hours: {self.market_open.strftime('%H:%M')} - {self.market_close.strftime('%H:%M')} {self.timezone}")
        logger.info(f"🔄 Check interval: {self.check_interval} seconds")
    
    def _parse_time(self, time_str):
        """Parse time string (HH:MM) to time object"""
        hour, minute = map(int, time_str.split(':'))
        return dt_time(hour, minute)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info("\n⚠️ Shutdown signal received")
        self.running = False
    
    def is_market_open(self):
        """
        Check if market is currently open
        
        Returns:
            bool: True if market is open
        """
        now = datetime.now(self.timezone).time()
        is_open = self.market_open <= now <= self.market_close
        
        # Also check if it's a weekday (Monday=0, Sunday=6)
        weekday = datetime.now(self.timezone).weekday()
        is_weekday = weekday < 5  # Monday-Friday
        
        return is_open and is_weekday
    
    def time_until_market_open(self):
        """
        Calculate time until market opens
        
        Returns:
            str: Human-readable time until market opens
        """
        now = datetime.now(self.timezone)
        
        # Create market open datetime for today
        market_open_today = now.replace(
            hour=self.market_open.hour,
            minute=self.market_open.minute,
            second=0,
            microsecond=0
        )
        
        if now.time() > self.market_close:
            # Market closed for today, calculate for tomorrow
            market_open_today = market_open_today.replace(day=now.day + 1)
        
        time_diff = market_open_today - now
        hours = time_diff.seconds // 3600
        minutes = (time_diff.seconds % 3600) // 60
        
        return f"{hours}h {minutes}m"
    
    def update_bulb(self, pnl):
        """
        Update bulb color based on P&L
        
        Args:
            pnl (float): Profit/Loss amount
        """
        try:
            thresholds = self.config.get('color_thresholds', {})
            self.wiz.set_color_for_pnl(pnl, thresholds)
            
            # If P&L changed significantly, pulse the bulb
            if self.last_pnl is not None:
                pnl_change = abs(pnl - self.last_pnl)
                if pnl_change > 1000:  # ₹1000+ change
                    color = 'green' if pnl > self.last_pnl else 'red'
                    logger.info(f"📊 Significant P&L change: ₹{pnl_change:,.2f}")
                    # Don't pulse for now to avoid too much activity
                    # self.wiz.pulse(color, times=1)
            
            self.last_pnl = pnl
            
        except Exception as e:
            logger.error(f"❌ Error updating bulb: {e}")
    
    def check_portfolio(self):
        """Check portfolio and update bulb"""
        try:
            logger.info("📊 Checking portfolio...")
            
            # Get total P&L
            pnl = self.zerodha.get_total_pnl()
            
            # Get portfolio summary for detailed logging
            summary = self.zerodha.get_portfolio_summary()
            
            if summary:
                logger.info(f"💼 Positions: {summary['position_count']} | "
                          f"Winners: {summary['profitable_positions']} | "
                          f"Losers: {summary['losing_positions']}")
                logger.info(f"💰 Total P&L: ₹{pnl:,.2f} ({summary['pnl_percentage']:.2f}%)")
            else:
                logger.info(f"💰 Total P&L: ₹{pnl:,.2f}")
            
            # Update bulb
            self.update_bulb(pnl)
            
            # Print colored console output
            if pnl > 0:
                print(f"{Fore.GREEN}✅ PROFIT: ₹{pnl:,.2f}{Style.RESET_ALL}")
            elif pnl < 0:
                print(f"{Fore.RED}❌ LOSS: ₹{pnl:,.2f}{Style.RESET_ALL}")
            else:
                print(f"{Fore.BLUE}➖ BREAK-EVEN: ₹0{Style.RESET_ALL}")
            
        except Exception as e:
            logger.error(f"❌ Error checking portfolio: {e}")
    
    def run(self):
        """Main monitoring loop"""
        
        # Authenticate with Zerodha
        if not self.zerodha.authenticate():
            logger.error("❌ Failed to authenticate with Zerodha")
            logger.error("🔧 Please run: python authenticate_zerodha.py")
            return
        
        # Test WiZ connection
        if not self.wiz.test_connection():
            logger.error("❌ Failed to connect to WiZ bulb")
            logger.error("🔧 Please run: python setup_wiz.py")
            return
        
        logger.info("✅ All systems ready!")
        logger.info("🎯 Starting monitoring loop...\n")
        
        # Main loop
        while self.running:
            try:
                if self.is_market_open():
                    logger.info(f"\n{'='*60}")
                    logger.info(f"🕐 {datetime.now(self.timezone).strftime('%I:%M:%S %p')}")
                    
                    # Check portfolio and update bulb
                    self.check_portfolio()
                    
                    # Wait before next check
                    logger.info(f"⏰ Next check in {self.check_interval} seconds...")
                    logger.info(f"{'='*60}\n")
                    
                    time.sleep(self.check_interval)
                    
                else:
                    # Market is closed
                    now = datetime.now(self.timezone)
                    
                    if now.time() < self.market_open:
                        status = "not yet open"
                        time_msg = f"Opens in {self.time_until_market_open()}"
                    else:
                        status = "closed for the day"
                        time_msg = f"Opens tomorrow at {self.market_open.strftime('%I:%M %p')}"
                    
                    logger.info(f"🌙 Market is {status}. {time_msg}")
                    
                    # Turn off bulb when market closed
                    self.wiz.turn_off()
                    
                    # Check every 5 minutes during closed hours
                    time.sleep(300)
                    
            except KeyboardInterrupt:
                logger.info("\n⚠️ Keyboard interrupt received")
                break
            except Exception as e:
                logger.error(f"❌ Error in main loop: {e}")
                logger.info("⏳ Retrying in 60 seconds...")
                time.sleep(60)
        
        # Cleanup on shutdown
        self.shutdown()
    
    def shutdown(self):
        """Graceful shutdown"""
        logger.info("\n" + "="*60)
        logger.info("🛑 Shutting down Stock Bulb Monitor...")
        logger.info("="*60)
        
        # Turn off bulb
        try:
            self.wiz.turn_off()
            logger.info("💡 Bulb turned off")
        except:
            pass
        
        logger.info("✅ Shutdown complete. Goodbye! 👋")


def main():
    """Entry point"""
    try:
        monitor = StockBulbMonitor()
        monitor.run()
    except FileNotFoundError:
        print(f"{Fore.RED}❌ config.json not found!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📝 Please create config.json with your API credentials{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
