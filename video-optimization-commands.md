# Video Optimization for Web Streaming

## Current Audio Issues
Based on your feedback, the crunchy audio is likely due to:
1. Audio codec compatibility issues
2. Variable bitrate (VBR) audio
3. Incorrect audio profile for browsers
4. Buffer underflow during streaming

## Recommended FFmpeg Commands

### 1. Check Current Video Properties
```bash
ffmpeg -i static/videos/demo-reel.mp4
```

### 2. Optimize Video for Web Streaming (Recommended)
```bash
ffmpeg -i static/videos/demo-reel.mp4 \
  -c:v libx264 -profile:v baseline -level 3.0 \
  -c:a aac -profile:a aac_low -ac 2 -ar 48000 -b:a 128k \
  -movflags +faststart \
  -preset medium -crf 23 \
  -maxrate 2000k -bufsize 4000k \
  static/videos/demo-reel-optimized.mp4
```

### 3. Audio-Focused Optimization (For Crunchy Audio Fix)
```bash
ffmpeg -i static/videos/demo-reel.mp4 \
  -c:v copy \
  -c:a aac -profile:a aac_low -ac 2 -ar 48000 -b:a 128k \
  -movflags +faststart \
  static/videos/demo-reel-audio-fixed.mp4
```

### 4. Conservative Audio Fix (Lower Bitrate)
```bash
ffmpeg -i static/videos/demo-reel.mp4 \
  -c:v copy \
  -c:a aac -profile:a aac_low -ac 2 -ar 44100 -b:a 96k \
  -movflags +faststart \
  static/videos/demo-reel-conservative.mp4
```

## Parameter Explanations

### Video Settings:
- `-c:v libx264`: Use H.264 codec (widely supported)
- `-profile:v baseline`: Most compatible H.264 profile
- `-level 3.0`: Compatible with most devices
- `-preset medium`: Balanced encoding speed/quality
- `-crf 23`: Good quality (18-28 range, lower = better)
- `-movflags +faststart`: Optimize for web streaming

### Audio Settings (Critical for Fixing Crunchy Audio):
- `-c:a aac`: Use AAC audio codec
- `-profile:a aac_low`: AAC-LC profile (most compatible)
- `-ac 2`: Force stereo (2 channels)
- `-ar 48000`: 48kHz sample rate (or 44100 for conservative)
- `-b:a 128k`: Constant bitrate 128kbps (or 96k for lower)

## Testing Steps

1. **Backup your original video**:
   ```bash
   cp static/videos/demo-reel.mp4 static/videos/demo-reel-original.mp4
   ```

2. **Try the audio-focused fix first** (keeps original video quality):
   ```bash
   ffmpeg -i static/videos/demo-reel-original.mp4 \
     -c:v copy \
     -c:a aac -profile:a aac_low -ac 2 -ar 48000 -b:a 128k \
     -movflags +faststart \
     static/videos/demo-reel.mp4
   ```

3. **Test in browser** - check for:
   - No crunchy audio on first play
   - Audio plays immediately (not muted)
   - Video doesn't stop at 7 seconds
   - Consistent audio quality on replay

4. **If still issues, try conservative settings**:
   ```bash
   ffmpeg -i static/videos/demo-reel-original.mp4 \
     -c:v copy \
     -c:a aac -profile:a aac_low -ac 2 -ar 44100 -b:a 96k \
     -movflags +faststart \
     static/videos/demo-reel.mp4
   ```

## Browser Developer Tools Check

After optimization, verify in DevTools Network tab:
- ✅ Content-Type: video/mp4
- ✅ Accept-Ranges: bytes
- ✅ Status: 206 Partial Content (for range requests)
- ✅ Content-Range: bytes X-Y/Total

## Notes
- The `+faststart` flag moves metadata to the beginning of the file for immediate playback
- AAC-LC with constant bitrate prevents the audio artifacts you're experiencing
- Stereo audio (2 channels) is most compatible with web browsers
- 48kHz is the standard for video, 44.1kHz for audio-only content
