import os
import sys
import glob

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clipper import clip_video, cleanup_temp_files

def test_clipper():
    """
    Test the clipper functionality by splitting a video into 1-minute segments.
    Usage: python test_clipper.py [video_file]
    If no video file is provided, the script will use the first video found in the downloads directory.
    """
    root_dir = os.path.dirname(os.path.dirname(__file__))
    output_directory = os.path.join(root_dir, "downloads")
    
    # Check if video file is provided as command line argument
    if len(sys.argv) > 1:
        video_file = sys.argv[1]
        if not os.path.exists(video_file):
            print(f"Error: Video file '{video_file}' not found.")
            return
    else:
        # Find the first video file in the downloads directory
        os.makedirs(output_directory, exist_ok=True)
        video_files = glob.glob(os.path.join(output_directory, "*.mp4"))
        video_files.extend(glob.glob(os.path.join(output_directory, "*.mkv")))
        video_files = [f for f in video_files if "_part_" not in f]  # Exclude existing parts
        
        if not video_files:
            print("No video files found in the downloads directory.")
            print("Please run test_downloader.py first or provide a video file path.")
            return
            
        video_file = video_files[0]  # Use the first video file
    
    print(f"Testing clipper with video file: {video_file}")
    
    # Clip the video into 1-minute segments
    try:
        print("Splitting video into 1-minute segments...")
        clip_video(video_file, output_directory)
        
        # List the generated segments
        segments = glob.glob(os.path.join(output_directory, "*_part_*.mp4"))
        segments.sort()
        
        print(f"\nGenerated {len(segments)} segments:")
        for i, segment in enumerate(segments):
            segment_name = os.path.basename(segment)
            size_mb = os.path.getsize(segment) / (1024 * 1024)
            print(f"{i+1}. {segment_name} ({size_mb:.2f} MB)")
        
        # Optional: clean up temporary files
        print("\nCleaning up temporary files...")
        cleanup_temp_files(output_directory)
        
        print("\nClipping completed successfully!")
        
    except Exception as e:
        print(f"Error during clipping: {e}")

if __name__ == "__main__":
    test_clipper()
