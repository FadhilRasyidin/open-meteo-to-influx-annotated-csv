import subprocess
import os


def create_shell_script(directory, script_name, shell_content):
    if not os.path.exists(directory):
        os.makedirs(directory)
    script_path = os.path.join(directory, script_name)
    with open(script_path, 'w') as file:
        file.write(shell_content)
    os.chmod(script_path, 0o755)
    return script_path


def execute_shell_script(script_path):
    subprocess.run([script_path], shell=True, check=True, timeout=5)


def push_files_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".csv") and not (filename == "is_day ().csv" or filename == "weathercode (wmo code).csv"):
            file_path = os.path.join(directory, filename)
            shell_content = f'influx write -b "intern-bucket" -f "{file_path}" --precision s ' \
                            f'--header "#constant measurement,forecast" --header "#datatype string,tag,tag,tag,tag,tag,tag,' \
                            f'dateTime:number,tag,tag,double"'
            script_name = f'push_{filename.replace(" ", "_").replace("(", "").replace(")", "").replace("°C", "Celsius").replace("%", "Percent").replace("W_m²", "W_Msquared").replace("°", "Degrees").replace(".csv","")}.sh'
            script_directory = "scripts"  # Replace with your desired directory name
            script_path = create_shell_script(script_directory, script_name, shell_content)
            execute_shell_script(script_path)


directory_to_push = "openMeteoParameters"
push_files_in_directory(directory_to_push)
