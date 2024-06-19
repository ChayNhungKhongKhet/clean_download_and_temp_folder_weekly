# cleanup_script.py
import os
import shutil
import stat
import tempfile

def remove_readonly(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clean_folder(folder_path, exceptions):
    for filename in os.listdir(folder_path):
        if filename in exceptions:
            continue  # Skip the exceptions
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.chmod(file_path, stat.S_IWRITE)  # Remove read-only attribute
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path, onerror=remove_readonly)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
    print(f"{folder_path} cleaned.")

def main():
    downloads_path = 'D:/Downloads/'  # Adjust the path as necessary
    temp_path = tempfile.gettempdir()  # Path to the temp folder
    exceptions = ['important.txt', 'do_not_delete']  # List filenames or directories to exclude from deletion
    clean_folder(downloads_path, exceptions)
    clean_folder(temp_path, [])

if __name__ == "__main__":
    main()