import os
import hashlib
import re
import shutil
from downloader import download_video
from clipper import clip_video, cleanup_temp_files

def read_urls_from_file(file_path):
    """Read URLs from a text file, ignoring comments and empty lines."""
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip() and not line.strip().startswith('#')]
    return urls

def get_processed_urls(cache_file):
    """Read list of URLs that have been processed already."""
    if not os.path.exists(cache_file):
        return set()
    
    with open(cache_file, 'r') as file:
        return set(line.strip() for line in file)

def add_processed_url(url, cache_file):
    """Add a URL to the processed cache file."""
    with open(cache_file, 'a') as file:
        file.write(f"{url}\n")

def sanitize_filename(filename):
    """Sanitize the filename to make it safe for use in a directory name."""
    # Replace special characters with underscores
    sanitized = re.sub(r'[\\/*?:"<>|]', "_", filename)
    # Replace special unicode characters and symbols
    sanitized = re.sub(r'[^\x00-\x7F]', "_", sanitized)
    # Replace multiple consecutive underscores with a single one
    sanitized = re.sub(r'_+', "_", sanitized)
    # Limit the length to avoid path too long error - be more conservative
    if len(sanitized) > 40:
        sanitized = sanitized[:37] + "..."
    # Remove trailing dots and spaces which can cause issues on Windows
    sanitized = sanitized.rstrip(". ")
    return sanitized

def create_folder_name(url, video_title=""):
    """Create a folder name with URL hash and title (if available)."""
    # Create a hash of the URL to use as a unique ID
    url_hash = hashlib.md5(url.encode()).hexdigest()[:10]
    
    # Create a directory name with hash (for uniqueness) and title (for readability)
    if video_title:
        sanitized_title = sanitize_filename(video_title)
        dir_name = f"video_{url_hash}_{sanitized_title}"
    else:
        dir_name = f"video_{url_hash}"
    
    return dir_name

def main():
    # Setup
    base_directory = "./downloads"
    os.makedirs(base_directory, exist_ok=True)
    url_file = "urls.txt"
    cache_file = os.path.join(base_directory, "processed_urls.txt")
    
    # Get URLs
    urls = read_urls_from_file(url_file)
    processed_urls = get_processed_urls(cache_file)
    
    print(f"Found {len(urls)} URLs in file")
    print(f"Already processed {len(processed_urls)} URLs")
    
    # Process each unprocessed URL
    for i, url in enumerate(urls):
        if url in processed_urls:
            print(f"\nSkipping already processed video: {url}")
            continue
            
        print(f"\nProcessing video {i+1}/{len(urls)}: {url}")
        
        try:
            # 1. First, get the video title without downloading
            print("Getting video info...")
            title_command = ["yt-dlp", "--cookies", "cookies.txt", "--print", "%(title)s", "--no-download", url]
            
            import subprocess
            try:
                result = subprocess.run(title_command, check=True, capture_output=True, text=True)
                video_title = result.stdout.strip()
                print(f"Video title: {video_title}")
            except subprocess.CalledProcessError:
                video_title = ""
                print("Could not get video title, will use hash only")
            
            # 2. Create the final directory with title (if available)
            folder_name = create_folder_name(url, video_title)
            video_directory = os.path.join(base_directory, folder_name)
            os.makedirs(video_directory, exist_ok=True)
            
            print(f"Video will be stored in: {video_directory}")
            
            # 3. Download video directly to the final directory
            print("Downloading video...")
            download_video(url, video_directory)
            
            # 4. Find the downloaded video file
            video_files = [os.path.join(video_directory, f) for f in os.listdir(video_directory) 
                        if f.endswith(('.mp4', '.mkv')) and "_part_" not in f]
            
            if video_files:
                latest_video = max(video_files, key=os.path.getmtime)
                
                # 5. Clip
                print(f"Clipping video: {os.path.basename(latest_video)}")
                clip_video(latest_video, video_directory)
                
                # 6. Cleanup
                cleanup_temp_files(video_directory)
                
                # Mark URL as processed
                add_processed_url(url, cache_file)
                print(f"Successfully processed: {url}")
            else:
                print(f"No video file found for: {url}")
        except Exception as e:
            print(f"Error processing {url}: {e}")
        
    print("\nAll videos processed!")

if __name__ == "__main__":
    main()
