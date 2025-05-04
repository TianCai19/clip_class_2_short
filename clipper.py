import os
import subprocess
import re

def clip_video(video_file, output_directory):
    """
    Splits a video into 1-minute segments using ffmpeg.
    
    Args:
        video_file: Path to the input video file
        output_directory: Directory where the clips will be saved
    """
    # Get the filename without extension
    base_name = os.path.basename(video_file)
    name_without_ext = os.path.splitext(base_name)[0]
    
    # Create the output pattern for the segments
    output_pattern = os.path.join(output_directory, f"{name_without_ext}_part_%03d.mp4")
    
    # ffmpeg command to split video into 1-minute (60 second) segments
    # Convert opus audio to AAC which is better supported in MP4 containers
    command = [
        "ffmpeg",
        "-i", video_file,
        "-c:v", "copy",     # Copy video codec without re-encoding
        "-c:a", "aac",      # Convert audio to AAC (compatible with MP4)
        "-map", "0",
        "-segment_time", "60",  # 1 minute segments
        "-f", "segment",
        "-reset_timestamps", "1",
        output_pattern
    ]
    
    subprocess.run(command, check=True)
    print(f"Video split into 1-minute segments at: {output_directory}")

def cleanup_temp_files(directory):
    """
    Removes temporary files that might be created during the downloading
    and clipping process.
    
    Args:
        directory: The directory to clean up
    """
    # Pattern for temporary files that should be removed
    temp_patterns = [
        r".*\.temp\.*",
        r".*\.part",
        r".*\.ytdl"
    ]
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            for pattern in temp_patterns:
                if re.match(pattern, filename):
                    try:
                        os.remove(file_path)
                        print(f"Removed temporary file: {filename}")
                    except Exception as e:
                        print(f"Error removing {filename}: {e}")
                    break
