import subprocess

def Run_Linux_Terminal_Command(Command):
    result = subprocess.run(
        'cd /home/noi/MyManus/WorkSpace/ && ' + Command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout