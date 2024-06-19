import subprocess

def create_task(task_name, script_path, python_path, start_time="07:00"):
    try:
        create_command = f'schtasks /Create /SC WEEKLY /D SUN /TN "{task_name}" /TR "{python_path} \'{script_path}\'" /ST {start_time} /F'
        change_user_command = f'schtasks /Change /TN "{task_name}" /RU SYSTEM'
        change_settings_command = f'schtasks /Change /TN "{task_name}" /RI 15 /DU "24:00" /K /SD "01/01/1910" /ED "01/01/2100" /IT /RL HIGHEST'
        set_power_settings_command = f'PowerShell -Command "Set-ScheduledTask -TaskName \'{task_name}\' -Settings (New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -WakeToRun)"'

        for command in [create_command, change_user_command, change_settings_command, set_power_settings_command]:
            result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(result.stdout.decode())

        print(f"Task '{task_name}' created and configured successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create and configure the task. Error: {e}\nOutput: {e.stdout.decode()}\nError Output: {e.stderr.decode()}")

if __name__ == "__main__":
    task_name = "ScheduleCleanupDownLoadsAndTempFiles" #set task name
    script_path = r"D:\Study\AutomationLap\clean_download_and_temp_folder_weekly\cleanup_temp_download_script.py" #your script path to leanup folder
    start_time = "07:00" #set start time
    python_path = r"D:\Program\Miniconda3\python.exe" #path to python executable
    
    create_task(task_name, script_path, python_path, start_time)