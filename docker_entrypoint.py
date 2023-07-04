import os
import subprocess


def CreateProcess(args: list[str], cwd: str = ".") -> subprocess.Popen:
    os.chdir(cwd)
    print("running: "+" ".join(args)+" inside "+os.getcwd())
    return subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, text=True)


def RunAsProcess(args: list[str], cwd: str = ".", timeout: int = 5) -> bool:
    CreateProcess(args, cwd)

    res = True
    stdout = None
    stderr = None

    try:
        stdout, stderr = proc.communicate(None, timeout)
    except subprocess.TimeoutExpired:
        print("timeout")
        proc.kill()
        stdout, stderr = proc.communicate()
    except:
        res = False

    if stderr is not None:
        res &= len(str(stderr)) <= 0

    if not res and str(stderr):
        print(f"stderr = {stderr}")
    elif str(stdout):
        print(f"stdout = {stdout}")

    return res


if __name__ == "__main__":
    while True:
        RunAsProcess(["python", "-m", "hoymiles", "-c",
                     "/ahoy_work/ahoy.yml"], "/ahoy", 10*60)

        pigpiod_process = CreateProcess(["pigpiod"])
        RunAsProcess(["python", "Hub.py"], "/weatherstation", 60)
        pigpiod_process.kill()

        RunAsProcess(["bash", "spi_reset.sh"], "/weatherstation")
