# VLC Discord Rich Presence

A Windows application that displays what you're currently reading/listening to in VLC Media Player on your Discord profile - similar to how Discord shows what game you're playing.

## Features

✨ **Real-time Status Updates** - Shows current media title on your Discord profile  
⏯️ **Playback State Sync** - Automatically shows "Playing" or "Paused" status  
⏱️ **Accurate Timestamps** - Displays actual VLC playback position, not just app runtime  
🔄 **Auto-cleanup** - Clears Discord status when VLC is closed  
🎯 **Lightweight** - Minimal resource usage, runs quietly in the background  

## Requirements

- **Windows** (tested on Windows 10/11)
- **Python 3.7+**
- **VLC Media Player** (latest version recommended)
- **Discord Desktop** app running

## Setup Instructions

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, **check "Add Python to PATH"**
3. Verify installation by opening Command Prompt and typing:
   ```bash
   python --version
   ```

### Step 2: Install Dependencies

1. Open Command Prompt
2. Navigate to the project folder:
   ```bash
   cd d:\GULP
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Create Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**
3. Give it a name (e.g., "VLC Rich Presence")
4. Go to **"General Information"** tab
5. Copy your **Application ID** (this is your Client ID)
6. *(Optional)* Go to **"Rich Presence"** → **"Art Assets"**:
   - Upload a VLC logo image as `vlc_logo`
   - Upload a play icon as `playing`
   - Upload a pause icon as `paused`
   - Click "Save Changes"

### Step 4: Configure the Application

1. Open `config.json` in a text editor
2. Replace `YOUR_DISCORD_CLIENT_ID_HERE` with your Application ID from Step 3
3. (Optional) Change the VLC password if you've set a custom one
4. Save the file

Example `config.json`:
```json
{
  "discord_client_id": "1234567890123456789",
  "vlc_host": "localhost",
  "vlc_port": 8080,
  "vlc_password": "vlcremote",
  "update_interval": 5
}
```

### Step 5: Enable VLC HTTP Interface

#### Method 1: Via VLC GUI (Recommended)

1. Open VLC Media Player
2. Go to **Tools** → **Preferences**
3. At bottom left, select **"All"** (Show settings: All)
4. Navigate to **Interface** → **Main interfaces**
5. Check the box: **"Web"**
6. Navigate to **Interface** → **Main interfaces** → **Lua**
7. Set **Lua HTTP Password** to: `vlcremote` (or match your config.json)
8. Click **Save**
9. **Restart VLC** for changes to take effect

#### Method 2: Via Command Line

1. Create a shortcut to VLC
2. Right-click the shortcut → Properties
3. In the **Target** field, add at the end:
   ```
   --extraintf=http --http-password=vlcremote
   ```
   Full example:
   ```
   "C:\Program Files\VideoLAN\VLC\vlc.exe" --extraintf=http --http-password=vlcremote
   ```
4. Click **OK**
5. Use this shortcut to launch VLC

#### Verify VLC HTTP Interface

1. Open VLC and play any media
2. Open a web browser
3. Go to: `http://localhost:8080`
4. When prompted, username is blank, password is `vlcremote`
5. You should see the VLC web interface

### Step 6: Run the Application

1. Open Command Prompt
2. Navigate to project folder:
   ```bash
   cd d:\GULP
   ```
3. Run the script:
   ```bash
   python vlc_discord_presence.py
   ```
4. You should see:
   ```
   VLC Discord Rich Presence - Starting...
   ✓ Connected to Discord Rich Presence
   Monitoring VLC Media Player...
   ```
5. Open VLC and play something - your Discord profile should update!

## Auto-Start on Windows Startup

### Method 1: Using Startup Folder (Recommended)

1. Press `Win + R`
2. Type: `shell:startup` and press Enter
3. Create a shortcut to `start_vlc_presence.bat` in this folder
4. The application will start automatically when Windows boots

### Method 2: Using Task Scheduler

1. Open Task Scheduler (`taskschd.msc`)
2. Click **"Create Basic Task"**
3. Name it "VLC Discord Presence"
4. Trigger: **"When I log on"**
5. Action: **"Start a program"**
6. Program: `C:\Windows\System32\cmd.exe`
7. Arguments: `/c start /min python d:\GULP\vlc_discord_presence.py`
8. Finish the wizard

## Usage

1. **Start the script** (it will run in the background)
2. **Open VLC** and play your audiobook/music
3. **Check your Discord profile** - it should show:
   - **Details**: "Reading in VLC" or "Paused"
   - **State**: The media title
   - **Timestamp**: Current playback position

### Discord Profile Display

When playing:
```
🎵 Reading in VLC
📖 [Your Media Title]
⏱️ [Elapsed Time] elapsed
```

When paused:
```
⏸️ Paused
⏸️ [Your Media Title]
```

## Troubleshooting

### "Cannot connect to VLC HTTP interface"

**Solution**: Make sure VLC's HTTP interface is enabled:
- Follow Step 5 above carefully
- Verify you can access `http://localhost:8080` in your browser
- Check that the password in `config.json` matches VLC's Lua HTTP password

### "Failed to connect to Discord"

**Solution**:
- Make sure Discord Desktop app is running (not web version)
- Verify your Client ID is correct in `config.json`
- Try restarting Discord

### "VLC detected but no status updates"

**Solution**:
- Verify VLC HTTP interface is working (check browser)
- Make sure port 8080 isn't blocked by firewall
- Try changing the port in both VLC settings and `config.json`

### Discord shows old status

**Solution**:
- Restart the Python script
- Restart Discord
- Wait a few seconds for Discord to refresh

### Script crashes on startup

**Solution**:
- Make sure `config.json` exists and is valid JSON
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (needs 3.7+)

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `discord_client_id` | Your Discord Application ID | Required |
| `vlc_host` | VLC HTTP interface host | `localhost` |
| `vlc_port` | VLC HTTP interface port | `8080` |
| `vlc_password` | VLC HTTP interface password | `vlcremote` |
| `update_interval` | Seconds between status updates | `5` |

## Advanced Features

### Custom VLC Port

If port 8080 is already in use:

1. In VLC, go to **Tools** → **Preferences** → **All** → **Interface** → **Main interfaces** → **Lua**
2. Set **Lua HTTP Port** to a different port (e.g., `8090`)
3. Update `vlc_port` in `config.json` to match

### Multiple Instances

To run multiple copies (not recommended):
- Create separate folders with different `config.json` files
- Use different Discord Client IDs for each instance

## Stopping the Application

- If running in Command Prompt: Press `Ctrl + C`
- If running in background: Use Task Manager to end `python.exe` process
- The script automatically cleans up Discord status when stopped

## Project Structure

```
d:\GULP\
├── vlc_discord_presence.py   # Main application script
├── config.json                # Configuration file
├── requirements.txt           # Python dependencies
├── start_vlc_presence.bat    # Windows startup script
├── setup_vlc_http.md         # VLC HTTP setup guide
└── README.md                  # This file
```

## Privacy & Security

- This application runs **locally on your computer**
- No data is sent to external servers (except Discord's official API)
- VLC HTTP interface is only accessible on your local machine
- Your media library information stays on your device

## Credits

Built with:
- [pypresence](https://github.com/qwertyquerty/pypresence) - Discord Rich Presence library
- [requests](https://docs.python-requests.org/) - HTTP library
- [psutil](https://github.com/giampaolo/psutil) - Process monitoring

---

## Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Verify all setup steps were completed
3. Check that VLC and Discord are both running
4. Try restarting the script

## License

This project is provided as-is for customer use.

---

**Enjoy showing off what you're reading/listening to on Discord! 📚🎧**
