File Extension Organizer

This project is a Python application that helps users organize files in a specified source folder into subfolders based on their file extensions. The application features a graphical user interface (GUI) built using Tkinter.
Features

    Organize files by their extensions into corresponding subfolders (e.g., .pdf, .jpg, .txt).
    Option to move or copy files to the destination folder.
    Progress bar with estimated time of arrival (ETA) during the organization process.
    Displays status updates throughout the operation.
    User-friendly interface for selecting source and destination folders.
    Option to include subfolders in the search.

Requirements

    Python 3.x
    tkinter (usually included with Python)
    os, shutil, pathlib, collections, threading, ttk (part of tkinter)

Installation

    Clone the repository (if applicable):

    bash

git clone <repository-url>
cd folder-parser

Run the script:

bash

    python organize_files.py

Usage

    Select the source folder: Use the "Browse" button next to the Source Folder label to choose the folder containing files you want to organize.

    Select the destination folder: Use the "Browse" button next to the Destination Folder label to choose where you want the organized files to be saved.

    Choose the action: Select either "Move" or "Copy" from the dropdown menu based on your preference.

    Start organizing: Click the "Organize Files" button to begin the organization process. The progress bar will indicate the current progress along with status updates.

Example

Given a source folder containing files like:

diff

- report.docx
- photo.png
- video.mp4

After running the organizer, the destination folder will be structured as:

css

- destination_folder/
  - docx/
    - report.docx
  - png/
    - photo.png
  - mp4/
    - video.mp4

Troubleshooting

    Ensure you have permissions to read from the source folder and write to the destination folder.
    If the GUI becomes unresponsive, try running the organization process in a separate thread.
    Check the console for any error messages for further troubleshooting.

Contributing

Contributions are welcome! If you have suggestions for improvements or additional features, please create an issue or submit a pull request.
License

This project is licensed under the MIT License. See the LICENSE file for details.
