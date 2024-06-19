import subprocess
import platform

def create_task_unix(task_name, script_path, python_path, start_time, day):
     # Convert start_time to a cron format
    hour, minute = start_time.split(':')
    # Cron job format: minute hour day month day-of-week
    cron_time = f'{minute} {hour} * * {day}'  # day indicates the day of week (0-7 where 0 and 7 is Sun)
    cron_job = f'{cron_time} {python_path} {script_path} # {task_name}\n'
    
    try:
        # Save current crontab to a temporary file
        subprocess.run('crontab -l > /tmp/current_crontab', shell=True, check=True)
        print("Current crontab saved.")
    except subprocess.CalledProcessError:
        # If there's an error, it might be because the crontab is empty, so we create an empty file
        subprocess.run('echo "" > /tmp/current_crontab', shell=True, check=True)
        print("No existing crontab. Creating a new one.")
    
    try:
        # Check if the task already exists in the crontab
        check_command = f'grep "{task_name}" /tmp/current_crontab'
        existing_task = subprocess.run(check_command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if existing_task.stdout:
            print(f"Task '{task_name}' already exists in the crontab. Skipping addition.")
            return
        else:
            # Append the new cron job to the temporary file
            with open('/tmp/current_crontab', 'a') as temp_file:
                temp_file.write(cron_job)
            
            # Load the new crontab
            subprocess.run('crontab /tmp/current_crontab', shell=True, check=True)
            print(f"Task '{task_name}' created and configured successfully on Unix-based OS.")

    except subprocess.CalledProcessError as e:
        print(f"Failed to create and configure the task on Unix-based OS. Error: {e}")

    finally:
        # Cleanup: Remove the temporary file
        subprocess.run('rm /tmp/current_crontab', shell=True, check=True)

def create_task_windows(task_name, script_path, python_path, start_time, day):
    try:
        # Windows Task Scheduler uses day names for weekly tasks
        day_names = {"0": "SUN", "1": "MON", "2": "TUE", "3": "WED", "4": "THU", "5": "FRI", "6": "SAT", "7": "SUN"}
        day_name = day_names.get(day, "SUN")  # Default to Sunday if day is invalid
        create_command = f'schtasks /Create /SC WEEKLY /D {day_name} /TN "{task_name}" /TR "{python_path} \'{script_path}\'" /ST {start_time} /F'
        change_user_command = f'schtasks /Change /TN "{task_name}" /RU SYSTEM'
        change_settings_command = f'schtasks /Change /TN "{task_name}" /RI 15 /DU "24:00" /K /SD "01/01/1910" /ED "01/01/2100" /IT /RL HIGHEST'
        set_power_settings_command = f'PowerShell -Command "Set-ScheduledTask -TaskName \'{task_name}\' -Settings (New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -WakeToRun)"'

        for command in [create_command, change_user_command, change_settings_command, set_power_settings_command]:
            result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(result.stdout.decode())

        print(f"Task '{task_name}' created and configured successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create and configure the task. Error: {e}\nOutput: {e.stdout.decode()}\nError Output: {e.stderr.decode()}")

def create_task(task_name, script_path, python_path, start_time="07:00", day="0"):
    os_system = platform.system()
    if os_system == "Windows":
        create_task_windows(task_name, script_path, python_path, start_time, day)
    elif os_system in ["Linux", "Darwin"]:  # Darwin is MacOS
        create_task_unix(task_name, script_path, python_path, start_time, day)
    else:
        print(f"Unsupported operating system: {os_system}")

if __name__ == "__main__":
    task_name = "ScheduleCleanupDownLoadsAndTempFiles" #set task name
    script_path = r"D:\Study\AutomationLap\clean_download_and_temp_folder_weekly\cleanup_temp_download_script.py" #your script path to leanup folder
    start_time = "07:00" #set start time
    python_path = r"D:\Program\Miniconda3\python.exe" #path to python executable
    day = '0'
    
    create_task(task_name, script_path, python_path, start_time, day)