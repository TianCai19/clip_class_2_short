import os
import hashlib
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

def get_video_directory(url, base_dir):
    """Create a unique directory name for the video based on URL hash."""
    # Create a hash of the URL to use as a unique ID
    url_hash = hashlib.md5(url.encode()).hexdigest()[:10]
    
    # Create a directory path
    video_dir = os.path.join(base_dir, f"video_{url_hash}")
    os.makedirs(video_dir, exist_ok=True)
    return video_dir

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
        
        # Create a separate directory for this video
        video_directory = get_video_directory(url, base_directory)
        print(f"Video will be stored in: {video_directory}")
        
        try:
            # Step 1: Download
            print("Downloading video...")
            download_video(url, video_directory)
            
            # Step 2: Find the downloaded video file
            video_files = [os.path.join(video_directory, f) for f in os.listdir(video_directory) 
                        if f.endswith(('.mp4', '.mkv')) and "_part_" not in f]
            
            if video_files:
                latest_video = max(video_files, key=os.path.getmtime)
                
                # Step 3: Clip
                print(f"Clipping video: {os.path.basename(latest_video)}")
                clip_video(latest_video, video_directory)
                
                # Step 4: Cleanup
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
