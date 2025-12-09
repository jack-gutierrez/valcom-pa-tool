import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pydub import AudioSegment
import os
import time
import zipfile
# -------------------------------------------------
#  CUE AUDIO FILES (folder "cues")
# -------------------------------------------------

CUE_FOLDER = "cues"
CUE_2MIN = os.path.join(CUE_FOLDER, "cue_2min.wav")
CUE_60SEC = os.path.join(CUE_FOLDER, "cue_60sec.wav")
CUE_30SEC = os.path.join(CUE_FOLDER, "cue_30sec.wav")


def load_cues():
    """Load countdown cue audio files, return None if missing."""
    try:
        cue2 = AudioSegment.from_file(CUE_2MIN)
        cue60 = AudioSegment.from_file(CUE_60SEC)
        cue30 = AudioSegment.from_file(CUE_30SEC)
        return cue2, cue60, cue30
    except:
        messagebox.showerror("Missing Cue Files",
                             "One or more cue audio files are missing in the 'cues' folder.")
        return None


# -------------------------------------------------
#  AUDIO PROCESSING
# -------------------------------------------------
def process_audio(filepath, apply_cues, cue_data, total_files, current_file, update_progress_callback, processed_files):
    """Clean, process, and optionally overlay cue speech announcements."""
    # Load audio file
    audio = AudioSegment.from_file(filepath)

    # Force to 4 minutes
    target_duration = 240000
    if len(audio) > target_duration:
        audio = audio[:target_duration]
    else:
        loops = target_duration // len(audio) + 1
        audio = (audio * loops)[:target_duration]

    # Set format
    audio = audio.set_channels(1).set_frame_rate(32000)

    # Fade out last 15 sec
    audio = audio.fade_out(15000)

    if apply_cues and cue_data is not None:
        cue2, cue60, cue30 = cue_data

        # Duck music by 6 dB during cues
        audio_ducked = audio - 18

        audio = audio_ducked.overlay(cue2, position=120000)   # 2-min
        audio = audio.overlay(cue60, position=180000)         # 60-sec
        audio = audio.overlay(cue30, position=210000)         # 30-sec

    # Clean file name and create the output path
    filename = os.path.basename(filepath).rsplit('.', 1)[0].replace(" ", "")[:30]
    output_filename = f"{filename}_processed.wav"
    
    # Get the directory of the original file
    output_dir = os.path.dirname(filepath)
    
    output_path = os.path.join(output_dir, output_filename)
    
    # Export the audio file
    audio.export(output_path, format="wav")

    # Add the processed file to the list
    processed_files.append(output_path)

    # Call the progress update callback function
    update_progress_callback(current_file)

    return output_path

def save_as_zip(processed_files, output_dir):
    """Save all processed files into a ZIP archive."""
    zip_filename = os.path.join(output_dir, "Processed_Audio_Files.zip")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in processed_files:
            zipf.write(file, os.path.basename(file))
    return zip_filename

def browse_and_process(progress_var):
    """Browse and process multiple audio files."""
    # Ask for files to process first
    paths = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.wav *.mp3 *.m4a")])
    if not paths:
        return  # Exit if no files are selected

    total_files = len(paths)
    processed_files = []  # List to store paths of processed files

    # Should we apply the cues?
    apply_cues = checkbox_var.get() == 1

    cue_data = load_cues() if apply_cues else None

    def update_progress(current_file):
        """Callback function to update the progress bar."""
        progress = (current_file / total_files) * 100
        progress_var.set(progress)
        progress_bar.update_idletasks()

    for current_file, path in enumerate(paths, start=1):
        process_audio(
            path,
            apply_cues,
            cue_data,
            total_files,
            current_file,
            update_progress,
            processed_files
        )

    # Save processed files as a ZIP
    zip_file = save_as_zip(processed_files, os.path.dirname(paths[0]))

    # Show success message with the ZIP file path
    messagebox.showinfo("Processing Complete", f"All files processed! The ZIP file is saved as:\n{zip_file}")

# UI Setup
root = tk.Tk()
root.title("Audio Processing Tool")
root.geometry("400x300")

tk.Label(root, text="🎵 Convert and Process Your Songs").pack(pady=10)

# Checkbox
checkbox_var = tk.IntVar()
tk.Checkbutton(root,
               text="Include countdown cues (2 min / 60 sec / 30 sec)",
               variable=checkbox_var).pack(pady=5)

# Progress bar setup
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=300)
progress_bar.pack(pady=10)

# Buttons
tk.Button(root, text="Choose Audio Files", command=lambda: browse_and_process(progress_var), width=25).pack(pady=5)
tk.Button(root, text="Exit", command=root.destroy).pack(pady=5)

root.mainloop()
