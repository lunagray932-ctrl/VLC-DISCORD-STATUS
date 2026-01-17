# Manual Cover Art Upload Guide

Since Discord doesn't support automated asset uploads, here's how to show your audiobook covers on Discord.

## Quick Process (5 minutes)

### Step 1: Extract & Compress Cover Art

1. **Play your audiobook in VLC** - The script automatically extracts the cover to `cover_cache/`

2. **Run the compression tool:**
   ```bash
   python compress_cover.py
   ```
   Or double-click: `compress_cover.bat`

3. **Result:** A compressed image ready for Discord (1024x576, under 500KB)
   - Saved as: `cover_cache/[filename]_compressed.jpg`

### Step 2: Upload to Discord Developer Portal

1. Go to: https://discord.com/developers/applications
2. Select your **VLC Rich Presence** application
3. Click: **Rich Presence** → **Art Assets** (in left sidebar)
4. Click: **Add Image** button
5. Upload the `_compressed.jpg` file from Step 1
6. **Important:** Name it exactly: **`book_cover`**
7. Click: **Save Changes**
8. Wait 5-10 minutes for Discord to process

### Step 3: Restart & Enjoy

1. Restart the VLC Discord Presence script
2. Play your audiobook in VLC
3. Check your Discord profile - your cover art is now showing! 📚

## What Gets Displayed

**Your Discord Profile:**
```
🎵 Reading in VLC
📖 H. D. Carlton - Haunting Adeline
⏱️ 00:15:32 elapsed

[Book Cover Image - 1024x576]
```

## Cover Art Specifications

- **Dimensions:** 1024x576 (Discord Rich Presence standard)
- **Aspect Ratio:** Maintained - no stretching or distortion
- **Letterboxing:** Black bars added if needed to preserve clarity
- **Format:** JPEG
- **Size:** Under 500KB
- **Quality:** High (95) for clear readability

## Tips & Strategies

### Strategy 1: Generic Book Icon (Recommended)
- Find/create one generic audiobook icon
- Upload it once as `book_cover`
- Works for all your audiobooks
- Never needs changing

**Pros:** Set it and forget it  
**Cons:** Same icon for everything

### Strategy 2: Current Book Cover
- Compress your current audiobook's cover
- Upload it as `book_cover`
- When you start a new book, repeat the process
- Old cover gets replaced

**Pros:** Shows actual book covers  
**Cons:** Need to update when switching books

### Strategy 3: Favorite Book
- Upload your favorite book's cover
- Keep it showing permanently

**Pros:** Shows off your favorite  
**Cons:** Might not match what you're currently listening to

## Troubleshooting

### Cover not showing on Discord
- Wait 10 minutes (Discord processing time)
- Verify asset name is exactly `book_cover` (lowercase, no spaces)
- Restart Discord app
- Restart VLC Discord Presence script

### Image quality issues
- Script automatically maintains aspect ratio
- No stretching or distortion
- High quality (95) ensures readability
- Black bars preserve original proportions

### Where's my extracted cover?
Check: `d:\GULP\cover_cache\`
- If empty, make sure VLC HTTP interface is enabled
- Play media with embedded artwork
- Script extracts covers automatically

## Finding Generic Icons

Free icon sources:
- https://flaticon.com (search "audiobook" or "book")
- https://icons8.com (search "reading")
- Google Images (search "audiobook icon PNG")

**Requirements:**
- PNG or JPEG format
- Will be resized to 1024x576
- Under 512KB file size (script handles compression)

## Quick Reference

**Compress cover:**
```bash
python compress_cover.py
# or
compress_cover.bat
```

**Discord Developer Portal:**
https://discord.com/developers/applications

**Asset name:**
`book_cover` (exactly, lowercase)

**Dimensions:**
1024x576 (no stretching, aspect ratio preserved)

**Wait time:**
5-10 minutes after upload

**Result:**
Beautiful, readable cover art on your Discord profile! 📚✨
