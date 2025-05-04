import os
import subprocess

def download_video(url, output_dir):
    """
    Downloads a YouTube video using yt-dlp with cookies for authentication.
    Forces MP4 as the output format with AAC audio for compatibility.
    """
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
