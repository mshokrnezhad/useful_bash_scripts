# Image and Audio to Video Converter

This script creates a video file by combining a static image with an audio file. It's useful for creating simple videos like slideshows, presentations, or music videos with a static background.

## Prerequisites

Before running the script, you need to install the following dependencies:

1. **Python 3.x**
2. **moviepy** (Python package)
3. **ffmpeg** (Required by moviepy)

### Installation Steps

1. Install Python 3.x from [python.org](https://www.python.org/downloads/)

2. Install moviepy:

   ```bash
   pip install moviepy
   ```

3. Install ffmpeg:
   - **macOS**:
     ```bash
     brew install ffmpeg
     ```
   - **Ubuntu/Debian**:
     ```bash
     sudo apt-get install ffmpeg
     ```
   - **Windows**:
     - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
     - Add ffmpeg to your system PATH

## Usage

1. Place your image and audio files in the same directory as the script
2. Update the file paths in the script or pass them as arguments
3. Run the script:
   ```bash
   python movie.py
   ```

### File Requirements

- **Image**: Can be in any common format (PNG, JPG, etc.)
- **Audio**: Can be in any common format (WAV, MP3, etc.)
- **Output**: Will be created as an MP4 file

### Example

```python
# Default file paths in the script
image_path = "image.png"  # Your image file
audio_path = "audio.wav"  # Your audio file
output_path = "output.mp4"  # Where to save the video
```

## Troubleshooting

1. **File Not Found Error**

   - Ensure all file paths are correct
   - Check that files exist in the specified locations

2. **FFmpeg Not Found**

   - Verify ffmpeg is installed
   - Check that ffmpeg is in your system PATH

3. **Memory Issues**
   - For large files, ensure you have sufficient memory
   - Consider reducing the resolution of the input image

## Notes

- The video duration will match the audio duration
- The script uses 24 FPS (frames per second) by default
- All resources are automatically cleaned up after processing
