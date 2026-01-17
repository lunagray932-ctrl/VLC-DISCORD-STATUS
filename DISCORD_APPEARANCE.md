# Discord Rich Presence Appearance Guide

This document shows you exactly what will appear on your Discord profile when using VLC Discord Rich Presence.

## What Your Discord Profile Will Show

### When Playing Media

```
┌─────────────────────────────────────┐
│  🎵  Reading in VLC                 │
│  📖  The Hobbit - Chapter 1.mp3     │
│  ⏱️  00:15:42 elapsed               │
│                                     │
│  [VLC Logo]                         │
└─────────────────────────────────────┘
```

**Details shown:**
- **Large Text**: "Reading in VLC"
- **State**: Current media title (e.g., "The Hobbit - Chapter 1.mp3")
- **Timestamp**: Shows actual playback position from VLC
- **Icon**: VLC logo (if you uploaded assets to Discord Developer Portal)

### When Paused

```
┌─────────────────────────────────────┐
│  ⏸️  Paused                         │
│  ⏸️  The Hobbit - Chapter 1.mp3     │
│                                     │
│  [VLC Logo]                         │
└─────────────────────────────────────┘
```

**Details shown:**
- **Large Text**: "Paused"
- **State**: Current media title
- **No timestamp** (paused state)
- **Icon**: VLC logo with pause indicator

### When VLC is Closed

```
No Rich Presence displayed
(Your normal Discord status)
```

The presence is automatically cleared when you close VLC.

## Customizing the Appearance

### Adding Custom Images

To add custom VLC logo and status icons to your Discord Rich Presence:

1. **Go to Discord Developer Portal**
   - https://discord.com/developers/applications
   - Select your application

2. **Navigate to Rich Presence → Art Assets**

3. **Upload these assets**:
   
   | Asset Name | Image Type | Purpose |
   |------------|-----------|---------|
   | `vlc_logo` | Large 512x512 PNG | Main VLC logo that shows in profile |
   | `playing` | Small 256x256 PNG | Small icon when playing |
   | `paused` | Small 256x256 PNG | Small icon when paused |

4. **Save Changes**

5. **Wait a few minutes** for Discord to process the images

**Where to find images:**
- VLC Logo: Download from [VLC website](https://www.videolan.org/)
- Playing Icon: Search for "play button icon transparent background"
- Paused Icon: Search for "pause button icon transparent background"

**Recommended image specifications:**
- Format: PNG with transparent background
- VLC Logo: 512x512 pixels
- Status Icons: 256x256 pixels
- File size: < 500KB each

### Modifying Text Display

You can customize the displayed text by editing `vlc_discord_presence.py`:

**Location 1 - Main status text (line ~137):**
```python
details = "Reading in VLC"
```
Change to:
```python
details = "Listening to Audiobook"  # or whatever you prefer
```

**Location 2 - Playing indicator (line ~138):**
```python
state_text = f"📖 {title}"
```
Change emoji:
```python
state_text = f"🎧 {title}"  # Headphones
state_text = f"📚 {title}"  # Books
state_text = f"🎵 {title}"  # Music note
```

**Location 3 - Paused text (line ~155):**
```python
details = "Paused"
```
Change to:
```python
details = "Taking a Break"
```

## Real-World Examples

### Example 1: Audiobook

**What you'll see on Discord:**
```
Reading in VLC
📖 Harry Potter and the Philosopher's Stone - Chapter 01
⏱️ 1:23:45 elapsed
```

### Example 2: Podcast

**What you'll see on Discord:**
```
Reading in VLC
📖 Joe Rogan Experience #1234 - Guest Name
⏱️ 0:45:12 elapsed
```

### Example 3: Music

**What you'll see on Discord:**
```
Reading in VLC
📖 The Beatles - Hey Jude
⏱️ 0:03:21 elapsed
```

### Example 4: Generic Media

**What you'll see on Discord (if no title metadata):**
```
Reading in VLC
📖 my-audiobook-file
⏱️ 0:15:00 elapsed
```

## Privacy Considerations

### What Information is Shared?

**Shared with Discord:**
- ✅ That you're using VLC
- ✅ The current media title/filename
- ✅ Current playback time
- ✅ Play/pause state

**NOT shared:**
- ❌ Your full media library
- ❌ File paths or locations
- ❌ Previous playback history
- ❌ Other VLC settings

### Disabling for Specific Files

If you want to temporarily hide your Discord status while playing certain content:

**Option 1: Pause the script**
- Press `Ctrl + C` in the Command Prompt running the script
- Your Discord status will clear

**Option 2: Close VLC**
- Closing VLC automatically clears the status

**Option 3: Disable Discord Rich Presence**
- In Discord: User Settings → Activity Privacy → Untoggle "Display current activity"

## How Others See Your Status

### On Discord Desktop

Friends viewing your profile will see:

```
[Your Name]  ●
Playing a game

🎵 Reading in VLC
📖 The Hobbit - Chapter 1.mp3
⏱️ 00:15:42 elapsed
```

### On Discord Mobile

```
[Your Name]
Reading in VLC
The Hobbit - Chapter 1.mp3
```
(Timestamp may not show on mobile)

### In Server Member List

```
[Your Avatar] [Your Name]
              Reading in VLC
```
(Hover shows full details)

## Status Update Timing

- **Update Interval**: Every 5 seconds (configurable in `config.json`)
- **State Change**: Immediate when you pause/play
- **Clear on Exit**: Instant when VLC closes
- **Initial Display**: Appears within 5 seconds of playing media

## Troubleshooting Appearance Issues

### Status Not Showing

1. **Check Discord Activity Status**
   - User Settings → Activity Privacy
   - Enable "Display current activity"

2. **Check Script is Running**
   - Console should show: "✓ Updated Discord: Playing - [title]"

3. **Restart Discord**
   - Sometimes Discord needs a restart to update Rich Presence

### Wrong Title Displayed

- The title comes from VLC's metadata
- Some files don't have proper metadata
- The script will show the filename if no title metadata exists
- To fix: Edit file metadata using a tool like MP3Tag

### Timestamp Not Syncing

- Timestamp shows VLC's actual playback position
- If it's wrong, try:
  - Restarting the script
  - Seeking in VLC (this updates the position)
  - Waiting for next update cycle (5 seconds)

### Images Not Showing

- Make sure you uploaded assets to Discord Developer Portal
- Asset names must match exactly: `vlc_logo`, `playing`, `paused`
- Wait 5-10 minutes after uploading for Discord to process
- Try restarting the script

---

**Enjoy your customized Discord Rich Presence! Your friends will know exactly what you're reading or listening to! 📚🎧**
