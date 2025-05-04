import os
import sys
import glob

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from downloader import download_video

def test_downloader():
    """
    Test the downloader functionality by downloading a video from the specified URL in urls.txt.
    """
    # Get the URL from urls.txt
    root_dir = os.path.dirname(os.path.dirname(__file__))
    url_file = os.path.join(root_dir, "urls.txt")
    
    try:
        with open(url_file, 'r') as file:
            urls = [line.strip() for line in file if line.strip() and not line.strip().startswith('#')]
    except Exception as e:
        print(f"Error reading URLs file: {e}")
        return
    
    if not urls:
        print("No URLs found in urls.txt file")
        return
    
    # Use the first URL for testing
    youtube_url = urls[0]
    print(f"Testing downloader with URL: {youtube_url}")
    
    # Create output directory
    output_directory = os.path.join(root_dir, "downloads")
    os.makedirs(output_directory, exist_ok=True)
    
    # Download the video
    print("Downloading video...")
    try:
        download_video(youtube_url, output_directory)
        print("Download completed successfully!")
        
        # List the downloaded files
        downloaded_files = [
            f for f in os.listdir(output_directory)
            if os.path.isfile(os.path.join(output_directory, f))
        ]
        
        print("\nDownloaded files in output directory:")
        for file in downloaded_files:
            file_path = os.path.join(output_directory, file)
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            print(f"- {file} ({size_mb:.2f} MB)")
            
    except Exception as e:
        print(f"Error during download: {e}")

if __name__ == "__main__":
    test_downloader()
