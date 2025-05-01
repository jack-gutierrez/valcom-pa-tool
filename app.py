import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pydub import AudioSegment
import os
import time
import zipfile

def process_audio(filepath, progress_var, total_files, current_file, processed_files, update_progress_callback):
    """Process each audio file and add it to the processed_files list."""
    # Load audio file
    audio = AudioSegment.from_file(filepath)

    # Force to 4 minutes
    target_duration = 240002
    if len(audio) > target_duration:
        audio = audio[:target_duration]
    else:
        loops = target_duration // len(audio) + 1
        audio = (audio * loops)[:target_duration]

    # Set format
    audio = audio.set_channels(1).set_frame_rate(32000)

    # Fade out last 15 sec
    audio = audio.fade_out(15000)

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

    def update_progress(current_file):
        """Callback function to update the progress bar."""
        progress = (current_file / total_files) * 100
        progress_var.set(progress)
        progress_bar.update_idletasks()

    for current_file, path in enumerate(paths, start=1):
        process_audio(path, progress_var, total_files, current_file, processed_files, update_progress)

    # Save processed files as a ZIP
    zip_file = save_as_zip(processed_files, os.path.dirname(paths[0]))

    # Show success message with the ZIP file path
    messagebox.showinfo("Processing Complete", f"All files processed! The ZIP file is saved as:\n{zip_file}")

# UI Setup
root = tk.Tk()
root.title("Audio Processing Tool")
root.geometry("400x300")

tk.Label(root, text="🎵 Convert and Process Your Songs").pack(pady=10)

# Progress bar setup
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=300)
progress_bar.pack(pady=10)

# Buttons
tk.Button(root, text="Choose Audio Files", command=lambda: browse_and_process(progress_var), width=25).pack(pady=5)
tk.Button(root, text="Exit", command=root.destroy).pack(pady=5)

root.mainloop()
