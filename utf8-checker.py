import os
import subprocess
import chardet


def select_folder_with_fzf():
    try:
        # Use shell=True to run the command in a shell context and exclude .venv
        result = subprocess.run(
            'find . -type d -not -path "./.venv*" "./.git*" | fzf',
            text=True,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
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
    return result["encoding"].lower() == "utf-8"


def check_folder_for_utf8(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not is_utf8(file_path):
                print(f"{file_path} is not in UTF-8 format")
            else:
                print(f"{file_path} is in UTF-8 format")


if __name__ == "__main__":
    # Select the folder using fzf
    folder_path = select_folder_with_fzf()
    check_folder_for_utf8(folder_path)
