import os
import shutil
from pathlib import Path
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading  # For running the organization process in a separate thread

def select_source_folder():
    """Open a file dialog to select the source folder."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        source_entry.delete(0, tk.END)  # Clear the entry
        source_entry.insert(0, folder_path)  # Insert the selected path

def select_destination_folder():
    """Open a file dialog to select the destination folder."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        destination_entry.delete(0, tk.END)  # Clear the entry
        destination_entry.insert(0, folder_path)  # Insert the selected path

def organize_files_by_extension(root, source_folder, destination_folder, action, status_label, progress_bar, progress_label):
    """
    Organize files from source_folder into subfolders in destination_folder based on their extensions.
    """
    status_label.config(text="Organizing files...")  # Update status label

    # Create the destination folder if it doesn't exist
    Path(destination_folder).mkdir(parents=True, exist_ok=True)

    # Dictionary to hold lists of files grouped by their extension
    files_by_extension = defaultdict(list)

    # Traverse the source directory and collect files
    for root_dir, _, files in os.walk(source_folder):
        for file in files:
            file_path = Path(root_dir) / file
            extension = file_path.suffix.lower()  # Extract extension in lowercase

            # Group files without extensions under 'no_extension'
            if not extension:
                extension = "no_extension"
            else:
                extension = extension.strip('.')

            files_by_extension[extension].append(file_path)

    total_files = sum(len(file_list) for file_list in files_by_extension.values())

    # Set up progress bar
    progress_bar["maximum"] = total_files
    progress_bar["value"] = 0  # Reset progress bar
    progress_label.config(text="Progress: 0.00%")  # Reset progress label

    # Move files into corresponding folders by extension with progress tracking
    for extension, file_list in files_by_extension.items():
        ext_folder = Path(destination_folder) / extension
        ext_folder.mkdir(parents=True, exist_ok=True)

        for file_path in file_list:
            destination_path = ext_folder / file_path.name

            # Handle duplicate filenames by adding a number suffix
            counter = 1
            while destination_path.exists():
                destination_path = ext_folder / f"{file_path.stem}_{counter}{file_path.suffix}"
                counter += 1

            try:
                # Move or copy file to the appropriate extension folder
                if action == "Move":
                    shutil.move(str(file_path), str(destination_path))
                else:
                    shutil.copy2(str(file_path), str(destination_path))  # Use copy2 to preserve metadata
                status_label.config(text=f"{action}d: {file_path.name}")  # Update status label
            except Exception as e:
                print(f"Failed to {action.lower()} {file_path}: {e}", flush=True)
                status_label.config(text=f"Failed to {action.lower()} {file_path.name}")

            # Update progress bar
            progress_bar["value"] += 1
            percent_complete = (progress_bar["value"] / total_files) * 100
            progress_label.config(text=f"Progress: {percent_complete:.2f}%")
            root.update_idletasks()  # Update the GUI

    status_label.config(text="Organizing complete!")  # Final status update
    messagebox.showinfo("Completion", "Organizing complete!")  # GUI notification

def start_organizing_thread():
    """Start the organizing process in a separate thread."""
    source_folder = source_entry.get()
    destination_folder = destination_entry.get()
    action = action_var.get()  # Get the selected action (Move or Copy)

    if not source_folder or not destination_folder:
        messagebox.showerror("Error", "Please select both source and destination folders.")
        return

    # Run the organization process in a separate thread
    organizing_thread = threading.Thread(target=organize_files_by_extension, args=(root, source_folder, destination_folder, action, status_label, progress_bar, progress_label))
    organizing_thread.start()

# Create the GUI window
root = tk.Tk()
root.title("File Extension Organizer")

# Create and place the labels and entry fields
tk.Label(root, text="Source Folder:").grid(row=0, column=0, padx=10, pady=10)
source_entry = tk.Entry(root, width=50)
source_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Button(root, text="Browse", command=select_source_folder).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Destination Folder:").grid(row=1, column=0, padx=10, pady=10)
destination_entry = tk.Entry(root, width=50)
destination_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Button(root, text="Browse", command=select_destination_folder).grid(row=1, column=2, padx=10, pady=10)

# Action selection dropdown menu
action_var = tk.StringVar(value="Move")  # Default action is Move
tk.Label(root, text="Select Action:").grid(row=2, column=0, padx=10, pady=10)
action_dropdown = ttk.Combobox(root, textvariable=action_var, values=["Move", "Copy"], state="readonly")
action_dropdown.grid(row=2, column=1, padx=10, pady=10)

# Status label
status_label = tk.Label(root, text="", wraplength=400)  # Wrap long messages
status_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Progress label
progress_label = tk.Label(root, text="Progress: 0.00%")
progress_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Start organizing button
tk.Button(root, text="Organize Files", command=start_organizing_thread).grid(row=6, column=1, padx=10, pady=20)

# Run the GUI event loop
root.mainloop()
