import subprocess
import time


def RunAsProcess(args: list[str], cwd:str=".", timeout: int = 5) -> bool:
    print("running: "+" ".join(args))
    proc = subprocess.Popen(args, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, cwd=cwd, text=True)

    res = True
    stdout = None
    stderr = None

    try:
        stdout, stderr = proc.communicate(None, timeout)
        res &= len(str(stderr)) <= 0
    except subprocess.TimeoutExpired:
        print("timeout")
        proc.kill()
        stdout, stderr = proc.communicate()
        res &= len(str(stderr)) <= 0
    except:
        res = False

    if not res and str(stderr):
        print(f"stderr = {stderr}")
    elif str(stdout):
        print(f"stdout = {stdout}")

    return res


if __name__ == "__main__":
    RunAsProcess(["pygpiod", "-g"])
    
    while True:
        RunAsProcess(["python", "-m", "hoymiles", "-c", "/ahoy_work/ahoy.yml" ],"ahoy",10*60)

        RunAsProcess(["python", "Hub.py"],"weatherstation")
        RunAsProcess(["bash", "./spi_reset.sh"],"weatherstation")
