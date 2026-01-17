# VLC HTTP Interface Setup Guide

This guide provides detailed instructions for enabling VLC's HTTP interface, which is required for the Discord Rich Presence integration to work.

## Why is this needed?

The HTTP interface allows external applications (like our Discord integration) to:
- Query what media is currently playing
- Check playback state (playing, paused, stopped)
- Get current playback position
- Retrieve media metadata (title, artist, album)

## Method 1: Enable via VLC Preferences (Recommended)

### Step-by-Step Instructions with Screenshots

1. **Open VLC Media Player**

2. **Access Preferences**
   - Click on **Tools** in the menu bar
   - Select **Preferences** (or press `Ctrl + P`)

3. **Switch to Advanced View**
   - At the bottom left corner, you'll see "Show settings"
   - Select **"All"** to show all settings (not "Simple")
   - This reveals the complete configuration tree

4. **Enable Web Interface**
   - In the left sidebar, navigate to: **Interface** → **Main interfaces**
   - Find the checkbox labeled **"Web"**
   - **Check this box** to enable the web interface

5. **Set HTTP Password**
   - In the left sidebar, expand **Interface** → **Main interfaces**
   - Click on **Lua**
   - Find the field labeled **"Lua HTTP Password"**
   - Enter: `vlcremote` (or any password you prefer)
   - **Important**: Remember this password - you'll need it in `config.json`

6. **Optional: Change HTTP Port**
   - In the same **Lua** section
   - Find **"Lua HTTP Port"**
   - Default is `8080` - change if this port is already in use
   - If you change it, update `vlc_port` in `config.json` to match

7. **Save Settings**
   - Click **"Save"** button at the bottom
   - A message may appear saying you need to restart VLC

8. **Restart VLC**
   - Close VLC completely
   - Reopen VLC Media Player

### Verify It's Working

1. Open VLC and play any media file
2. Open your web browser
3. Navigate to: `http://localhost:8080`
4. You should see a login prompt:
   - **Username**: Leave blank (or enter any text)
   - **Password**: `vlcremote` (or whatever you set)
5. If successful, you'll see the VLC web interface

## Method 2: Enable via Command Line Arguments

If you prefer not to change VLC's settings permanently, you can launch VLC with command-line arguments.

### Creating a Custom VLC Shortcut

1. **Locate VLC executable**
   - Default location: `C:\Program Files\VideoLAN\VLC\vlc.exe`
   - Or: `C:\Program Files (x86)\VideoLAN\VLC\vlc.exe`

2. **Create a shortcut**
   - Right-click on your desktop
   - Select **New** → **Shortcut**
   - Browse to `vlc.exe` location
   - Click **Next**, name it "VLC with HTTP", click **Finish**

3. **Modify shortcut properties**
   - Right-click the new shortcut → **Properties**
   - In the **Target** field, you'll see something like:
     ```
     "C:\Program Files\VideoLAN\VLC\vlc.exe"
     ```
   - Add this at the end (after the closing quote):
     ```
     --extraintf=http --http-password=vlcremote
     ```
   - Final result should look like:
     ```
     "C:\Program Files\VideoLAN\VLC\vlc.exe" --extraintf=http --http-password=vlcremote
     ```

4. **Optional: Change port**
   - If port 8080 is in use, add:
     ```
     --http-port=8090
     ```
   - Full example:
     ```
     "C:\Program Files\VideoLAN\VLC\vlc.exe" --extraintf=http --http-password=vlcremote --http-port=8090
     ```

5. **Use this shortcut**
   - Always launch VLC using this shortcut
   - The HTTP interface will be active while VLC is running
   - When VLC closes, the interface shuts down automatically

### Creating a Batch File Launcher

Alternatively, create a batch file `launch_vlc.bat`:

```batch
@echo off
"C:\Program Files\VideoLAN\VLC\vlc.exe" --extraintf=http --http-password=vlcremote
```

Double-click this file to launch VLC with HTTP interface enabled.

## Method 3: Create VLC Configuration File

For advanced users who want persistent settings without using the GUI:

1. **Locate VLC config directory**
   - Press `Win + R`
   - Type: `%APPDATA%\vlc` and press Enter

2. **Edit vlcrc file**
   - Open `vlcrc` in a text editor (create if it doesn't exist)
   - Add these lines:
     ```ini
     [http]
     http-password=vlcremote
     http-port=8080
     
     [core]
     extraintf=http
     ```

3. **Save and restart VLC**

## Troubleshooting

### "Cannot access http://localhost:8080"

**Possible causes:**

1. **HTTP interface not enabled**
   - Go back through Method 1 steps carefully
   - Make sure you clicked "Save" and restarted VLC

2. **Wrong port number**
   - Check if VLC is actually using port 8080
   - Try different ports: 8081, 8090, 9090
   - Update `config.json` to match

3. **Firewall blocking**
   - Windows Firewall might block the connection
   - Add VLC to Windows Firewall exceptions:
     - Open Windows Defender Firewall
     - Click "Allow an app through firewall"
     - Find VLC or click "Allow another app"
     - Select VLC and check both Private and Public

4. **VLC not running**
   - Make sure VLC is actually open
   - Try playing a media file

### "Wrong username or password"

- The username field can be blank or any text
- Make sure the password matches exactly:
  - What you set in VLC settings
  - What's in your `config.json`
- Password is case-sensitive

### "Connection refused" or "Cannot connect"

1. **Check if VLC HTTP is listening**
   - Open Command Prompt
   - Type: `netstat -an | findstr :8080`
   - You should see a line with `0.0.0.0:8080` or `127.0.0.1:8080`
   - If nothing appears, HTTP interface isn't running

2. **Try restarting VLC**
   - Close VLC completely (check Task Manager)
   - Reopen VLC
   - Wait a few seconds for HTTP interface to start

3. **Check for port conflicts**
   - Another application might be using port 8080
   - Try changing to a different port (e.g., 8090)

## Testing the HTTP Interface

### Quick Browser Test

1. Open VLC and play something
2. Open browser to: `http://localhost:8080/requests/status.json`
3. Login with your password
4. You should see JSON data like:
   ```json
   {
     "state": "playing",
     "information": {
       "category": {
         "meta": {
           "title": "Your Media Title"
         }
       }
     }
   }
   ```

### Test with PowerShell

Open PowerShell and run:

```powershell
$password = "vlcremote"
$bytes = [System.Text.Encoding]::UTF8.GetBytes(":$password")
$base64 = [Convert]::ToBase64String($bytes)
$headers = @{"Authorization" = "Basic $base64"}
Invoke-RestMethod -Uri "http://localhost:8080/requests/status.json" -Headers $headers
```

This should return VLC's current status.

### Test with Python

```python
import requests
from requests.auth import HTTPBasicAuth

response = requests.get(
    "http://localhost:8080/requests/status.json",
    auth=HTTPBasicAuth('', 'vlcremote')
)
print(response.json())
```

## Security Considerations

### Is this safe?

- The HTTP interface only binds to `localhost` (127.0.0.1)
- It's **not accessible** from other computers on your network
- Only applications on your computer can connect to it
- The password protects against unauthorized local access

### Changing the default password

The default password `vlcremote` is fine for local use, but you can change it:

1. In VLC settings, set a different **Lua HTTP Password**
2. Update `config.json` with the new password:
   ```json
   {
     "vlc_password": "your_new_password"
   }
   ```

### Network exposure

By default, VLC HTTP interface only listens on localhost. To make it accessible over your network (not recommended):

1. In VLC settings → Interface → Main interfaces → Lua
2. Find **"Lua HTTP Host"**
3. Change from `localhost` to `0.0.0.0`
4. **Warning**: This exposes VLC control to your entire network

## API Endpoints Reference

Once HTTP interface is enabled, these endpoints are available:

- `http://localhost:8080/requests/status.json` - Current playback status
- `http://localhost:8080/requests/playlist.json` - Playlist information
- `http://localhost:8080/requests/browse.json` - Browse media library

Our application primarily uses `status.json` to get:
- Current media title
- Playback state (playing/paused/stopped)
- Current time position
- Total media length

## Additional Resources

- [VLC HTTP Interface Documentation](https://wiki.videolan.org/VLC_HTTP_requests/)
- [VLC Command Line Help](https://wiki.videolan.org/VLC_command-line_help/)
- [VLC Documentation Index](https://wiki.videolan.org/Documentation:Documentation/)

---

## Still having issues?

If you've followed all steps and still can't connect:

1. **Restart everything**:
   - Close VLC completely
   - Restart the Discord Presence script
   - Reopen VLC and play media

2. **Check VLC version**:
   - Very old VLC versions might have different settings
   - Update to the latest VLC version

3. **Try alternative ports**:
   - Common alternatives: 8081, 8090, 9090
   - Update both VLC settings and `config.json`

4. **Disable antivirus temporarily**:
   - Some antivirus software blocks localhost connections
   - Try disabling temporarily to test

---

**Once HTTP interface is working, the Discord Rich Presence integration will automatically detect VLC and update your status!**
