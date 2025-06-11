# Demo Reel Thumbnail Commands

## Extract thumbnail at different timestamps:

### At 3 seconds:
```bash
ffmpeg -i "app\static\videos\demo-reel.mp4" -ss 00:00:03 -vframes 1 "app\static\images\demo-reel-thumbnail.jpg"
```

### At 8 seconds:
```bash
ffmpeg -i "app\static\videos\demo-reel.mp4" -ss 00:00:08 -vframes 1 "app\static\images\demo-reel-thumbnail.jpg"
```

### At 10 seconds:
```bash
ffmpeg -i "app\static\videos\demo-reel.mp4" -ss 00:00:10 -vframes 1 "app\static\images\demo-reel-thumbnail.jpg"
```

### Higher quality thumbnail:
```bash
ffmpeg -i "app\static\videos\demo-reel.mp4" -ss 00:00:05 -vframes 1 -q:v 2 "app\static\images\demo-reel-thumbnail.jpg"
```

## Manual Options:
1. Open the video in VLC, Windows Media Player, or any video editor
2. Seek to the desired timestamp (a few seconds in)
3. Take a screenshot or export frame
4. Save as `demo-reel-thumbnail.jpg` in `app\static\images\`

## Video Thumbnail Best Practices:
- Choose a frame that represents your best work
- Avoid blurry or transitional frames
- Consider a frame with good lighting and clear facial visibility
- Aspect ratio should match your video (16:9)
- Recommended size: 1280x720 or higher for HD quality
