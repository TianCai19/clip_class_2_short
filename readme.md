# Clip Youtube long Class Video 2 short video

A simple yet powerful tool to download YouTube videos and automatically split them into shorter segments.

## Features

- Download videos from YouTube using provided URLs
- Split videos into customizable segments (default: 1-minute clips)
- Process multiple videos in batch mode
- Cache mechanism to avoid reprocessing the same URLs
- Organize downloads in separate folders for each video
- Clean up temporary files automatically

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/youtube-video-clipper.git
   cd youtube-video-clipper
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Make sure you have FFmpeg installed on your system:
   - **macOS**: `brew install ffmpeg`
   - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

4. Obtain YouTube cookies (optional, for restricted videos):
   - Using a browser extension like "Get cookies.txt" or similar
   - Save the file as `cookies.txt` in the project directory

## Usage

1. Add YouTube URLs to the `urls.txt` file (one URL per line)
2. Run the main script:
   ```
   python main.py
   ```
3. Find your downloaded videos and segments in the `downloads` directory

## Running Tests

Test files are located in the `tests` directory and can be run individually:

```
# Test just the downloader
python tests/test_downloader.py

# Test just the clipper
python tests/test_clipper.py [optional_video_path]
```

## Project Structure

- `main.py` - Main script that orchestrates the pipeline
- `downloader.py` - Handles YouTube video downloads
- `clipper.py` - Splits videos into segments
- `urls.txt` - List of videos to process
- `requirements.txt` - Python dependencies
- `tests/` - Directory containing test files

## License

MIT License - Feel free to use and modify this code for your projects.
