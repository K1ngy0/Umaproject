# Umaproject - Local Video Server

A Python-based local video server that scans your computer for video files and serves them through a web interface with range request support for smooth video playback.

## Overview

Umaproject is a local video streaming solution that allows you to:
1. Scan your computer for video files
2. Generate a JSON catalog of found videos
3. Serve videos through a local web server with range request support
4. Browse and play videos in a web-based interface

## Features

- **Video Discovery**: Automatically scans specified directories for video files
- **Web Interface**: Clean, responsive web interface for browsing videos
- **Range Request Support**: HTTP range requests for smooth video seeking and streaming
- **Cross-Platform**: Works on Windows with batch scripts for easy execution
- **JSON Catalog**: Generates a structured JSON file of all discovered videos
- **Size Filtering**: Configurable minimum file size filtering
- **Path Mapping**: Maps local file paths to server-relative paths for web access

## Project Structure

```
Umaproject-main/
├── Umaproject.py          # Main Python script for video scanning
├── UMA.bat                # Main batch file to start the application
├── start_server.bat       # Batch file to start the web server
├── start_server_with_range.py  # Python HTTP server with range request support
├── index.html             # Main web interface
├── Plyr.html              # Alternative player interface (Plyr.js)
├── windows_videos.json    # Generated video catalog (after scanning)
└── README.md              # This file
```

## Requirements

- Python 3.x
- Windows OS (for batch files, though Python scripts are cross-platform)

## Quick Start

1. **Run the Application**:
   ```
   Double-click UMA.bat
   ```

2. **First Run**:
   - If no `windows_videos.json` exists, you'll be prompted to enter scanning parameters:
     ```
     -r "C:\Users\YourName\Videos" -s "C:\path\to\Umaproject-main" -min 5
     ```
   - Parameters:
     - `-r`: Root directory to scan for videos
     - `-s`: Server root directory (path to this project folder)
     - `-min`: Minimum video file size in MB

3. **Subsequent Runs**:
   - If `windows_videos.json` exists, the server will start immediately

4. **Access the Interface**:
   - Open your browser and go to: `http://localhost:8000`

## Manual Usage

### Video Scanning Script

```bash
python Umaproject.py -r "C:\Videos" -s "C:\path\to\Umaproject-main" -min 3
```

### Starting the Server

```bash
python start_server_with_range.py
```

Or double-click `start_server.bat`

## How It Works

1. **Video Discovery**: 
   - The Python script scans specified directories for video files
   - Filters out files smaller than the minimum size
   - Maps local absolute paths to server-relative paths
   - Generates `windows_videos.json` with video metadata

2. **Web Server**:
   - Custom HTTP server with range request support
   - Enables video seeking and smooth playback
   - Serves HTML interface and video files

3. **Web Interface**:
   - Displays video catalog from JSON file
   - Provides searchable video browser
   - Embedded video player with controls

## Supported Video Formats

- MP4, AVI, MOV, MKV
- FLV, WMV, MPEG, MPG
- M4V, WEBM, 3GP, OGV
- RMVB, RM, ASF, TS, MTS, VOB

## Configuration

### Command Line Arguments

- `-r`, `--root`: Video scanning start directory (default: C:\Users\Administrator\Documents)
- `-s`, `--server-root`: Server root directory (required)
- `-o`, `--output`: Output JSON filename (default: windows_videos.json)
- `-min`, `--min-size`: Minimum video size in MB (default: 3)

## Troubleshooting

1. **Permission Errors**: Run as Administrator if scanning protected directories
2. **Python Not Found**: Ensure Python is installed and added to PATH
3. **Videos Not Playing**: Check that video files are accessible and not corrupted
4. **Server Not Starting**: Ensure port 8000 is not in use by another application

## Customization

- Modify `index.html` to change the web interface
- Adjust CSS variables in the HTML files for theme changes
- Edit the Python scripts to modify scanning behavior

## License

This project is open source and available under the MIT License.


