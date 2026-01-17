"""
VLC Discord Rich Presence
A Python script that shows what you're currently reading/listening to in VLC on Discord.
Author: Built for a customer
Date: January 2026
"""

import time
import requests
import psutil
import json
from pypresence import Presence
from datetime import datetime
import sys
import os
from requests.auth import HTTPBasicAuth

class VLCDiscordPresence:
    def __init__(self, config_path="config.json"):
        """Initialize the VLC Discord Presence integration."""
        self.config = self.load_config(config_path)
        self.client_id = self.config.get("discord_client_id")
        self.vlc_host = self.config.get("vlc_host", "localhost")
        self.vlc_port = self.config.get("vlc_port", 8080)
        self.vlc_password = self.config.get("vlc_password", "vlcremote")
        self.update_interval = self.config.get("update_interval", 5)
        
        self.rpc = None
        self.connected_to_discord = False
        self.last_state = None
        self.start_time = None
        self.last_position = 0
        
        print("VLC Discord Rich Presence - Starting...")
        print(f"VLC HTTP Interface: http://{self.vlc_host}:{self.vlc_port}")
        
    def load_config(self, config_path):
        """Load configuration from JSON file."""
        if not os.path.exists(config_path):
            print(f"Error: Configuration file '{config_path}' not found!")
            print("Please create a config.json file with your Discord Client ID.")
            sys.exit(1)
        
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def connect_discord(self):
        """Connect to Discord Rich Presence."""
        try:
            if not self.connected_to_discord:
                self.rpc = Presence(self.client_id)
                self.rpc.connect()
                self.connected_to_discord = True
                print("✓ Connected to Discord Rich Presence")
                return True
        except Exception as e:
            print(f"✗ Failed to connect to Discord: {e}")
            self.connected_to_discord = False
            return False
    
    def disconnect_discord(self):
        """Disconnect from Discord Rich Presence."""
        try:
            if self.connected_to_discord and self.rpc:
                self.rpc.close()
                self.connected_to_discord = False
                print("✓ Disconnected from Discord Rich Presence")
        except Exception as e:
            print(f"Warning: Error disconnecting from Discord: {e}")
    
    def is_vlc_running(self):
        """Check if VLC is currently running."""
        for process in psutil.process_iter(['name']):
            try:
                if process.info['name'].lower() == 'vlc.exe':
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return False
    
    def get_vlc_status(self):
        """Get current VLC playback status via HTTP interface."""
        try:
            url = f"http://{self.vlc_host}:{self.vlc_port}/requests/status.json"
            response = requests.get(
                url, 
                auth=HTTPBasicAuth('', self.vlc_password),
                timeout=2
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.exceptions.RequestException:
            return None
    
    def extract_media_info(self, status):
        """Extract media information from VLC status."""
        if not status:
            return None
        
        info = status.get('information', {})
        meta = info.get('category', {}).get('meta', {})
        
        # Try to get title from metadata
        title = meta.get('title', meta.get('filename', 'Unknown Media'))
        
        # Clean up title (remove file extensions)
        if title.endswith(('.mp3', '.mp4', '.avi', '.mkv', '.flac', '.m4a', '.m4b')):
            title = os.path.splitext(title)[0]
        
        # Get additional metadata
        artist = meta.get('artist', '')
        album = meta.get('album', '')
        
        # Create full display title
        if artist and album:
            full_title = f"{artist} - {title}"
        elif artist:
            full_title = f"{artist} - {title}"
        else:
            full_title = title
        
        # Get playback information
        state = status.get('state', 'stopped')
        length = status.get('length', 0)  # Total duration in seconds
        time_pos = status.get('time', 0)  # Current position in seconds
        
        return {
            'title': full_title[:128],  # Discord has character limits
            'state': state,
            'length': length,
            'position': time_pos,
            'raw_title': title
        }
    
    def update_presence(self, media_info):
        """Update Discord Rich Presence with media information."""
        if not self.connected_to_discord:
            return
        
        try:
            if not media_info or media_info['state'] == 'stopped':
                # Clear presence when stopped
                self.rpc.clear()
                self.last_state = None
                self.start_time = None
                self.last_position = 0
                print("✓ Cleared Discord presence (VLC stopped)")
                return
            
            state = media_info['state']
            title = media_info['title']
            position = media_info['position']
            length = media_info['length']
            
            # Calculate start time based on current position
            # This makes the timestamp show actual playback position
            current_time = int(time.time())
            
            if state == 'playing':
                # Detect position changes (seeking or initial play)
                position_changed = abs(position - self.last_position) > self.update_interval + 2
                
                # Always recalculate start_time based on current position to keep it accurate
                # Recalculate if: resuming from pause, seeking, or initial play
                if self.last_state != 'playing' or self.start_time is None or position_changed:
                    self.start_time = current_time - position
                    self.last_position = position
                
                details = "Reading in VLC"
                state_text = f"📖 {title}"
                
                # Only use start time to show elapsed time (not total duration)
                self.rpc.update(
                    details=details,
                    state=state_text,
                    large_image="book_cover",
                    large_text="VLC Media Player",
                    small_image="playing",
                    small_text="Playing",
                    start=self.start_time
                )
                
                # Update last position for next iteration
                self.last_position = position
                
                if self.last_state != 'playing':
                    print(f"✓ Updated Discord: Playing - {title}")
                
            elif state == 'paused':
                details = "Paused"
                state_text = f"⏸️ {title}"
                
                self.rpc.update(
                    details=details,
                    state=state_text,
                    large_image="book_cover",
                    large_text="VLC Media Player",
                    small_image="paused",
                    small_text="Paused"
                )
                
                if self.last_state != 'paused':
                    print(f"✓ Updated Discord: Paused - {title}")
            
            self.last_state = state
            
        except Exception as e:
            print(f"✗ Error updating Discord presence: {e}")
            self.connected_to_discord = False
    
    def run(self):
        """Main loop to monitor VLC and update Discord."""
        print("\n" + "="*60)
        print("VLC Discord Rich Presence is running!")
        print("="*60)
        print("\nMonitoring VLC Media Player...")
        print("Press Ctrl+C to stop.\n")
        
        vlc_was_running = False
        
        try:
            while True:
                vlc_running = self.is_vlc_running()
                
                if vlc_running:
                    if not vlc_was_running:
                        print("✓ VLC detected!")
                        vlc_was_running = True
                    
                    # Connect to Discord if not already connected
                    if not self.connected_to_discord:
                        self.connect_discord()
                    
                    # Get VLC status
                    status = self.get_vlc_status()
                    
                    if status:
                        media_info = self.extract_media_info(status)
                        self.update_presence(media_info)
                    else:
                        if self.connected_to_discord:
                            print("⚠ Cannot connect to VLC HTTP interface. Is it enabled?")
                else:
                    if vlc_was_running:
                        print("✓ VLC closed - clearing Discord presence")
                        if self.connected_to_discord:
                            self.rpc.clear()
                        vlc_was_running = False
                        self.last_state = None
                        self.start_time = None
                        self.last_position = 0
                
                time.sleep(self.update_interval)
                
        except KeyboardInterrupt:
            print("\n\nShutting down gracefully...")
            self.disconnect_discord()
            print("✓ VLC Discord Rich Presence stopped.")
            sys.exit(0)
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
            self.disconnect_discord()
            sys.exit(1)

def main():
    """Entry point for the application."""
    presence = VLCDiscordPresence("config.json")
    presence.run()

if __name__ == "__main__":
    main()
