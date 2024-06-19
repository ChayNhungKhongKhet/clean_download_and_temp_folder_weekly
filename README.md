# Automated Cleanup Task Setup Guide

This guide provides instructions on how to set up an automated cleanup task on Windows laptops. This task periodically cleans up specified folders, such as Downloads and Temp, to help maintain a tidy file system.

## Prerequisites

- Windows operating system
- Python installed on your system
  - Verify Python installation by running `python --version` in the Command Prompt.

## Files Description

- `schedule_cleanup.py`: Creates a scheduled task that runs a cleanup script weekly.
- `cleanup_script.py`: Performs the actual cleanup of specified folders, deleting all files except for those explicitly excluded.

## Setup Instructions

### Step 1: Locate Python Executable Path

1. Open Command Prompt.
2. Run `where python` to find the path to the Python executable.
3. Note down the displayed path (e.g., `C:\Users\YourUser\AppData\Local\Programs\Python\Python39\python.exe`).

### Step 2: Prepare Scripts

1. Place both scripts (`schedule_cleanup.py` and `cleanup_script.py`) in a convenient location on your laptop.
2. Open `schedule_cleanup.py` in a text editor.
3. Set `task_name` to a descriptive name for the scheduled task.
4. Update `script_path` to the full path of `cleanup_script.py`.
5. Adjust `start_time` to your preferred cleanup time.
6. Modify `python_path` to the Python executable path noted earlier.
7. Modify `day` if needed, default is "0" -> Sunday
8. Save the changes.

### Step 3: Customize Cleanup Script

1. Open `cleanup_script.py` in a text editor.
2. Modify `downloads_path` to the full path of the folder you wish to clean regularly.
3. Adjust `exceptions` to include any filenames or directories you want to exclude from deletion.
4. Save and close the file.

### Step 4: Create Scheduled Task

1. Open Command Prompt or some CLI(Mac,Linux) as <span style="color:orange">Administrator</span>.
2. Navigate to the folder containing `schedule_cleanup.py`.
3. Run the script by executing: `python schedule_cleanup.py` or `python3 schedule_cleanup.py`(Mac).
4. You should see a confirmation message indicating that the task was created successfully.

### Confirming Task Creation

#### Windows

1. Open the Start Menu, search for "Task Scheduler", and open it.
2. In the Task Scheduler library, find the task named as per your `task_name` variable.
3. Verify the task's properties and conditions are correctly set as per your configuration.

## Troubleshooting

- If the task does not run as expected, check the Task Scheduler for any error messages.
- Ensure the script paths and Python executable path are correctly specified in `schedule_cleanup.py`.
- Verify that Python is correctly installed and accessible from the Command Prompt.

## Conclusion

You have successfully set up an automated cleanup task on your laptop. This task will help you maintain a clean file system by periodically removing unwanted files from specified folders.
