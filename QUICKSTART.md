# Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites Checklist

- [ ] Windows 10/11
- [ ] Python 3.7+ installed
- [ ] VLC Media Player installed
- [ ] Discord Desktop app installed and running

## Setup Steps

### 1. Install Dependencies (2 minutes)

Open Command Prompt in this folder and run:

```bash
pip install -r requirements.txt
```

### 2. Create Discord Application (2 minutes)

1. Go to https://discord.com/developers/applications
2. Click "New Application"
3. Name it "VLC Rich Presence"
4. Copy the **Application ID** from General Information tab

### 3. Configure (1 minute)

Edit `config.json` and replace `YOUR_DISCORD_CLIENT_ID_HERE` with your Application ID:

```json
{
  "discord_client_id": "1234567890123456789",
  "vlc_host": "localhost",
  "vlc_port": 8080,
  "vlc_password": "vlcremote",
  "update_interval": 5
}
```

### 4. Enable VLC HTTP Interface (2 minutes)

**In VLC Media Player:**

1. Tools → Preferences
2. Show settings: **All** (bottom left)
3. Interface → Main interfaces → Check **"Web"**
4. Interface → Main interfaces → Lua → Set password to: **vlcremote**
5. Click **Save** and restart VLC

**Verify it works:**
- Open browser to http://localhost:8080
- Login with password: `vlcremote`

### 5. Run! (30 seconds)

```bash
python vlc_discord_presence.py
```

That's it! Open VLC, play something, and check your Discord profile.

## Quick Test

1. Run the script
2. Open VLC
3. Play any audio/video file
4. Check Discord - you should see:
   - "Reading in VLC"
   - Your media title
   - Elapsed time

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Cannot connect to VLC HTTP interface" | Make sure you enabled Web interface in VLC and restarted VLC |
| "Failed to connect to Discord" | Make sure Discord app is running (not web version) |
| "Config file not found" | Make sure `config.json` exists in the same folder |

## Auto-Start on Windows Boot

1. Press `Win + R`
2. Type: `shell:startup`
3. Create a shortcut to `start_vlc_presence.bat` in that folder

Done! It will start automatically when you log in.

---

**Need more help?** Check [README.md](README.md) for detailed instructions.
