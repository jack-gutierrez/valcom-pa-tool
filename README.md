# Valcom PA Tool

**Automate audio formatting for PA system transitions**

This tool allows you to process multiple audio files for the Valcom PA system, ensuring they are formatted correctly (looped or trimmed to 4 minutes, correct sample rate, mono channel) and optionally adds timing cue overlays. Processed files can also be exported as a ZIP file for convenience.


## Features

- **Automatic audio formatting**:  
  - Loop or trim audio to 4 minutes  
  - Convert to mono, 32 kHz WAV format  
  - Fade out last 15 seconds  

- **Optional timing cues**:  
  - Add “2 minutes,” “60 seconds,” and “30 seconds” audio cues to songs  
  - Toggle cues on or off with a checkbox  

- **Batch processing**:  
  - Process multiple audio files at once  
  - Export all processed audio as a single ZIP archive  

- **Smart file naming**:  
  - Files are saved with `[original_name]_processed.wav`  
  - Character limit enforced for long filenames  

- **Cross-platform friendly**:  
  - Built with Python and Tkinter  
  - Works on Windows and macOS with Python 3.11+  

## Requirements

- Python 3.11+  
- [pydub](https://github.com/jiaaro/pydub)  
- ffmpeg (included in `dist` folder for distribution)  
- Tkinter (usually comes with Python)  

Install dependencies via pip:

```bash
pip install pydub
```

## Usage

1. **Run the app**  
   ```bash
   python app.py
   ```  
   or use the generated executable `ValcomTool.exe` (no Python installation required).

2. **Upload audio files**  
   - Click “Choose Audio Files”  
   - Select one or multiple `.mp3`, `.wav`, or `.m4a` files  

3. **Optional cues**  
   - Enable the checkbox to add timing announcements  

4. **Process audio**  
   - Files are automatically formatted  
   - A ZIP file containing all processed files will be created in the same folder as the original files  

5. **Completion**  
   - A success message will show the location of the ZIP file  

## File Structure

```
valcom-pa-tool/
│
├── app.py                     # Main application script
├── cues/                      # Optional cue audio files
│   ├── cue_2min.wav
│   ├── cue_60sec.wav
│   └── cue_30sec.wav
├── dist/                      # Generated executable and included ffmpeg
│   └── ValcomTool.exe
│   └── ffmpeg.exe
├── build/                     # Temporary build files (auto-generated)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Notes

- The executable includes `ffmpeg.exe` for convenience; users do **not** need to install ffmpeg manually.  
- Progress bar updates as each audio file is processed.  
- Volume can be boosted in `app.py` by applying a gain in the `process_audio` function:  

```python
audio = audio + 5  # Increase volume by 5 dB
```
---


