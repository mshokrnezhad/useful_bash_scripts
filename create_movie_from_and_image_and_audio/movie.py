"""
Movie Creation Script

This script creates a video file by combining an image and an audio file.
It uses the moviepy library to handle the video and audio processing.

The script:
1. Loads an audio file and determines its duration
2. Creates an image clip with the same duration as the audio
3. Combines the image and audio into a video file
4. Handles resource cleanup and error cases

Dependencies:
    - moviepy: For video and audio processing
    - ffmpeg: Required by moviepy for video encoding (must be installed separately)
"""

from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
import os


def create_video(image_path, audio_path, output_path):
    """
    Create a video file by combining an image and an audio file.

    Args:
        image_path (str): Path to the input image file
        audio_path (str): Path to the input audio file
        output_path (str): Path where the output video will be saved

    Raises:
        FileNotFoundError: If either the image or audio file doesn't exist
        Exception: For any other errors during video creation
    """
    try:
        # Verify input files exist before processing
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        # Load the audio file first to determine the video duration
        audio_clip = AudioFileClip(audio_path)

        # Create an image clip with the same duration as the audio
        # This ensures the video length matches the audio length
        image_clip = ImageClip(image_path, duration=audio_clip.duration)

        # Combine the image clip with the audio
        video_clip = image_clip
        video_clip.audio = audio_clip

        # Write the final video to a file
        # Using 24 FPS as it's a common frame rate for video
        video_clip.write_videofile(output_path, fps=24)

        print(f"Video successfully created at: {output_path}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Ensure all resources are properly closed
        # This is important to prevent memory leaks and file handle issues
        try:
            audio_clip.close()
            image_clip.close()
            video_clip.close()
        except:
            pass


if __name__ == "__main__":
    # Example usage with default file paths
    # Replace these with your actual file paths
    image_path = "image.png"  # or "image.png"
    audio_path = "audio.wav"
    output_path = "output.mp4"

    create_video(image_path, audio_path, output_path)
