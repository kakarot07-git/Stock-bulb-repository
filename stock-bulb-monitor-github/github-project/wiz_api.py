"""
WiZ Smart Bulb Controller
Handles WiZ bulb connection and color control
"""

import logging
import requests
import json
import time
from typing import Optional

logger = logging.getLogger(__name__)


class WiZController:
    """Controller for WiZ smart bulbs"""
    
    # Color definitions in WiZ RGB format
    COLORS = {
        'red': {'r': 255, 'g': 0, 'b': 0},
        'green': {'r': 0, 'g': 255, 'b': 0},
        'blue': {'r': 0, 'g': 0, 'b': 255},
        'yellow': {'r': 255, 'g': 255, 'b': 0},
        'orange': {'r': 255, 'g': 165, 'b': 0},
        'purple': {'r': 128, 'g': 0, 'b': 128},
        'white': {'r': 255, 'g': 255, 'b': 255},
    }
    
    def __init__(self, config):
        """
        Initialize WiZ controller
        
        Args:
            config (dict): Configuration with bulb_ip
        """
        self.bulb_ip = config.get('bulb_ip')
        self.port = 38899  # WiZ UDP port
        
        if not self.bulb_ip:
            logger.error("❌ No bulb IP address configured!")
            raise ValueError("bulb_ip is required in config")
        
        logger.info(f"💡 WiZ Controller initialized (Bulb: {self.bulb_ip})")
    
    def _send_command(self, params: dict) -> Optional[dict]:
        """
        Send command to WiZ bulb via UDP
        
        Args:
            params (dict): Command parameters
            
        Returns:
            dict: Response from bulb or None if failed
        """
        try:
            import socket
            
            # Create UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(3)
            
            # Prepare message
            message = {
                "method": "setPilot",
                "params": params
            }
            
            # Send to bulb
            sock.sendto(
                json.dumps(message).encode(),
                (self.bulb_ip, self.port)
            )
            
            # Wait for response
            try:
                data, _ = sock.recvfrom(1024)
                response = json.loads(data.decode())
                sock.close()
                return response
            except socket.timeout:
                logger.warning("⚠️ Bulb response timeout (command may have worked)")
                sock.close()
                return {"success": True}  # Assume success
                
        except Exception as e:
            logger.error(f"❌ Error sending command: {e}")
            return None
    
    def _get_state(self) -> Optional[dict]:
        """
        Get current bulb state
        
        Returns:
            dict: Bulb state or None if failed
        """
        try:
            import socket
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(3)
            
            message = {"method": "getPilot", "params": {}}
            
            sock.sendto(
                json.dumps(message).encode(),
                (self.bulb_ip, self.port)
            )
            
            data, _ = sock.recvfrom(1024)
            response = json.loads(data.decode())
            sock.close()
            
            return response.get('result', {})
            
        except Exception as e:
            logger.error(f"❌ Error getting state: {e}")
            return None
    
    def test_connection(self) -> bool:
        """
        Test connection to WiZ bulb
        
        Returns:
            bool: True if connection successful
        """
        try:
            state = self._get_state()
            
            if state:
                status = "ON" if state.get('state', False) else "OFF"
                logger.info(f"✅ Connected to WiZ bulb (currently {status})")
                return True
            else:
                logger.error(f"❌ Failed to connect to bulb at {self.bulb_ip}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Connection test failed: {e}")
            return False
    
    def set_color(self, color_name: str, brightness: int = 100, transition_time: int = 2000):
        """
        Set bulb to a specific color
        
        Args:
            color_name (str): Color name ('red', 'green', 'blue', etc.)
            brightness (int): Brightness 0-100 (default: 100)
            transition_time (int): Transition time in milliseconds (default: 2000 = 2 seconds)
        
        Returns:
            bool: True if successful
        """
        try:
            color_name = color_name.lower()
            
            if color_name not in self.COLORS:
                logger.warning(f"⚠️ Unknown color '{color_name}', using white")
                color_name = 'white'
            
            color = self.COLORS[color_name]
            
            # WiZ brightness is 10-100
            brightness = min(100, max(10, brightness))
            
            # Prepare command
            params = {
                'r': color['r'],
                'g': color['g'],
                'b': color['b'],
                'dimming': brightness,
                'state': True
            }
            
            # Send command
            response = self._send_command(params)
            
            if response:
                logger.info(f"💡 Bulb set to {color_name.upper()} (brightness: {brightness})")
                return True
            else:
                logger.error(f"❌ Failed to set color")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error setting color: {e}")
            return False
    
    def set_brightness(self, brightness: int):
        """
        Set bulb brightness only
        
        Args:
            brightness (int): Brightness 0-100
        """
        try:
            brightness = min(100, max(10, brightness))
            
            params = {
                'dimming': brightness,
                'state': True
            }
            
            response = self._send_command(params)
            
            if response:
                logger.info(f"💡 Brightness set to {brightness}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"❌ Error setting brightness: {e}")
            return False
    
    def turn_on(self):
        """Turn bulb on"""
        try:
            params = {'state': True}
            response = self._send_command(params)
            
            if response:
                logger.info("💡 Bulb turned ON")
                return True
            return False
            
        except Exception as e:
            logger.error(f"❌ Error turning on: {e}")
            return False
    
    def turn_off(self):
        """Turn bulb off"""
        try:
            params = {'state': False}
            response = self._send_command(params)
            
            if response:
                logger.info("💡 Bulb turned OFF")
                return True
            return False
            
        except Exception as e:
            logger.error(f"❌ Error turning off: {e}")
            return False
    
    def get_state(self) -> Optional[dict]:
        """
        Get current bulb state
        
        Returns:
            dict: Bulb state information
        """
        return self._get_state()
    
    def pulse(self, color: str = 'green', times: int = 3):
        """
        Pulse the bulb (flash effect)
        
        Args:
            color (str): Color to pulse
            times (int): Number of pulses
        """
        try:
            original_state = self._get_state()
            
            for _ in range(times):
                self.set_color(color, brightness=100, transition_time=500)
                time.sleep(0.5)
                self.set_brightness(30)
                time.sleep(0.5)
            
            # Restore original state
            if original_state and original_state.get('state', False):
                orig_brightness = original_state.get('dimming', 100)
                self.set_color(color, brightness=orig_brightness)
            
            logger.info(f"✨ Pulsed {color} {times} times")
            
        except Exception as e:
            logger.error(f"❌ Error pulsing: {e}")
    
    def set_color_for_pnl(self, pnl: float, thresholds: dict):
        """
        Set color based on P&L amount
        
        Args:
            pnl (float): Profit/Loss amount
            thresholds (dict): Color thresholds configuration
        """
        try:
            huge_profit = thresholds.get('huge_profit', 10000)
            huge_loss = thresholds.get('huge_loss', -10000)
            
            if pnl > 0:
                # Profit = Green
                # Brightness based on profit magnitude
                if pnl >= huge_profit:
                    brightness = 100  # Max brightness
                else:
                    # Scale brightness: ₹0-10k → 40-100
                    brightness = int(40 + (pnl / huge_profit) * 60)
                
                self.set_color('green', brightness=brightness)
                logger.info(f"✅ PROFIT: ₹{pnl:,.2f} → GREEN (brightness: {brightness})")
                
            elif pnl < 0:
                # Loss = Red
                # Brightness based on loss magnitude
                if pnl <= huge_loss:
                    brightness = 100  # Max brightness
                else:
                    # Scale brightness: ₹0 to -10k → 40-100
                    brightness = int(40 + (abs(pnl) / abs(huge_loss)) * 60)
                
                self.set_color('red', brightness=brightness)
                logger.info(f"❌ LOSS: ₹{pnl:,.2f} → RED (brightness: {brightness})")
                
            else:
                # Break-even = Blue
                self.set_color('blue', brightness=50)
                logger.info(f"➖ BREAK-EVEN: ₹0 → BLUE")
                
        except Exception as e:
            logger.error(f"❌ Error setting color for P&L: {e}")


if __name__ == "__main__":
    # Test the WiZ controller
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    import json
    with open('config.json') as f:
        config = json.load(f)
    
    wiz = WiZController(config['wiz'])
    
    if wiz.test_connection():
        print("\n✅ Connection successful!")
        print("\n🎨 Testing colors...")
        
        for color in ['green', 'red', 'blue', 'yellow']:
            print(f"  → {color.upper()}")
            wiz.set_color(color, brightness=80)
            time.sleep(2)
        
        print("\n✨ Testing pulse effect...")
        wiz.pulse('green', times=2)
        
        print("\n💡 Test complete!")
    else:
        print("\n❌ Connection failed. Check your config.")
