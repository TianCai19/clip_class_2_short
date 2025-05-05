import os
import subprocess
import json

def download_video(url, output_dir):
    """
    Downloads a YouTube video using yt-dlp with cookies for authentication.
    Forces MP4 as the output format with AAC audio for compatibility.
    Returns the title of the downloaded video.
    """
    # First get the video info to extract the title
    title_command = [
        "yt-dlp",
        "--cookies", "cookies.txt",
        "--print", "%(title)s",
        "--no-download",
        url
    ]
    
    try:
        result = subprocess.run(title_command, check=True, capture_output=True, text=True)
        video_title = result.stdout.strip()
    except subprocess.CalledProcessError:
        video_title = ""  # Default to empty string if can't get title
    
    command = [
        "yt-dlp",
        "--cookies", "cookies.txt",  # Use cookies for authentication
        "--merge-output-format", "mp4",  # Force MP4 as the output format
        "--postprocessor-args", "-c:a aac",  # Convert audio to AAC for MP4 compatibility
        "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
        url
    ]
    
    # Fallback command if the above fails (directly downloading a compatible format)
    fallback_command = [
        "yt-dlp",
        "--cookies", "cookies.txt",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",  # Prefer MP4 compatible formats
        "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
        url
    ]
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print("First download method failed, trying alternative approach...")
        subprocess.run(fallback_command, check=True)
    
    return video_title
