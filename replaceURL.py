import os
import re
import tkinter as tk
from tkinter import filedialog

def replace_links(directory, old_link, new_link, extensions=None):
    """Replaces links in files (with specified extensions) within a directory and its subdirectories."""

    if not extensions:
        extensions = ['*']

    for root, _, files in os.walk(directory):
        for filename in files:
            if extensions == ['*'] or filename.split('.')[-1] in extensions:
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r+', encoding='utf-8') as file:
                        content = file.read()
                        pattern = rf"{re.escape(old_link)}(/.+)"
                        new_content = re.sub(pattern, f"{new_link}\\1", content)
                        if content != new_content:
                            file.seek(0)
                            file.write(new_content)
                            file.truncate()
                            print(f"Replaced links in: {file_path}")
                except UnicodeDecodeError:
                    print(f"Skipped (UnicodeDecodeError): {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

def select_directory():
    """Opens a folder selection dialog and returns the selected directory."""
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory()
    return directory

if __name__ == "__main__":  # Prevents code from running on import
    directory = select_directory()

    if not directory:
        print("No directory selected. Exiting.")
        exit()

    old_link = input("Enter the old base URL: ")
    new_link = input("Enter the new base URL: ")
    extensions_input = input("Enter file extensions (comma-separated, or leave blank for all): ")
    extensions = [ext.strip() for ext in extensions_input.split(",")] if extensions_input else None

    replace_links(directory, old_link, new_link, extensions)

    print("Replacement completed!")
