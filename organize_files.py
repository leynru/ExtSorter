import os
import shutil
from pathlib import Path
from collections import defaultdict

def organize_files_by_extension(source_folder, destination_folder):
    """
    Organize files from source_folder into subfolders in destination_folder based on their extensions.
    """
    print(f"Starting to organize files from '{source_folder}'...\n", flush=True)  # Start message

    # Create the destination folder if it doesn't exist
    Path(destination_folder).mkdir(parents=True, exist_ok=True)

    # Dictionary to hold lists of files grouped by their extension
    files_by_extension = defaultdict(list)

    print("Scanning files...\n", flush=True)  # Debug message

    # Traverse the source directory and collect files
    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = Path(root) / file
            extension = file_path.suffix.lower()  # Extract extension in lowercase

            # Group files without extensions under 'no_extension'
            if not extension:
                extension = "no_extension"
            else:
                extension = extension.strip('.')

            files_by_extension[extension].append(file_path)

    print("Organizing files by extension...\n", flush=True)  # Debug message

    # Move files into corresponding folders by extension
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
                # Move file to the appropriate extension folder
                shutil.move(str(file_path), str(destination_path))
                print(f"Moved: {file_path} -> {destination_path}", flush=True)  # Status for each file
            except Exception as e:
                print(f"Failed to move {file_path}: {e}", flush=True)

    print("\nOrganizing complete!", flush=True)  # Completion message

if __name__ == "__main__":
    # Example usage
    source = input("Enter the path to the folder containing files: ")
    destination = input("Enter the path to the destination folder: ")
    organize_files_by_extension(source, destination)
