
import subprocess


with open("C:/Users/Reset/Documents/GitHub/OVRDOZE/commit_message.txt", "r") as f:
    version = f.readline().strip("\n")

with open("C:/Users/Reset/Documents/GitHub/OVRDOZE/utilities/version.py", "w") as f:
    f.write(f"frozenVersion = {version}")


# Replace 'your_command_here' with the actual command you want to run
command_to_run = 'pyinstaller C:/Users/Reset/Documents/GitHub/OVRDOZE/onefile.spec'

# Run the command in the command prompt
subprocess.run(command_to_run, shell=True)
