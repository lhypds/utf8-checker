import os
import subprocess
import chardet
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get ignore formats and folders from environment variables
ignore_formats = os.getenv("IGNORE_FORMATS", "").split(",")
ignore_folders = os.getenv("IGNORE_FOLDERS", "").split(",")


def select_folder_with_fzf():
    try:
        # Use shell=True to run the command in a shell context and exclude specified root-level folders
        exclude_paths = " ".join(
            f"-not -path './{folder}'" for folder in ignore_folders if folder
        )
        command = f"find . -maxdepth 1 -type d {exclude_paths} | fzf"
        result = subprocess.run(
            command, text=True, shell=True, check=True, stdout=subprocess.PIPE
        )
        selected_folder = result.stdout.strip()
        return selected_folder
    except subprocess.CalledProcessError:
        print("No folder selected.")
        exit(1)


def is_utf8(filepath):
    with open(filepath, "rb") as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result.get("encoding")
    if encoding is None:
        print(f"Could not detect encoding for {filepath}")
        return False
    return encoding.lower() == "utf-8"


def check_folder_for_utf8(folder_path):
    for root, dirs, files in os.walk(folder_path):
        # Modify dirs in place to skip ignored folders
        dirs[:] = [d for d in dirs if d not in ignore_folders]

        for file in files:
            # Skip files with ignored formats
            if any(file.endswith(ext) for ext in ignore_formats):
                continue

            file_path = os.path.join(root, file)
            if not is_utf8(file_path):
                print(f"{file_path} is not in UTF-8 format")


if __name__ == "__main__":
    # Select the folder using fzf
    folder_path = select_folder_with_fzf()
    check_folder_for_utf8(folder_path)
