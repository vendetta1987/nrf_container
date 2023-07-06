import os
import subprocess


def CreateProcess(args: list[str], cwd: str = ".") -> subprocess.Popen:
    old_dir = os.getcwd()
    os.chdir(cwd)
    print("running: "+" ".join(args)+" inside "+os.getcwd())
    proc = subprocess.Popen(args, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, cwd=cwd, text=True)
    os.chdir(old_dir)
    return proc


def RunAsProcess(args: list[str], cwd: str = ".", timeout: int = 5) -> bool:
    proc = CreateProcess(args, cwd)

    result = True
    stdout = None
    stderr = None

    try:
        stdout, stderr = proc.communicate(None, timeout)
    except subprocess.TimeoutExpired:
        print("timeout")

        proc.kill()
        _stdout, _stderr = proc.communicate()

        if stdout is None:
            stdout = _stdout
        else:
            stdout += "\n"+_stdout

        if stderr is None:
            stderr = _stderr
        else:
            stderr += "\n"+_stderr

        result = False
    except Exception as exc:
        print("exception occured:\n"+exc)
        result = False

    if stdout is not None and len(str(stdout)) > 0:
        print(f"stdout:\n{stdout}")

    if stderr is not None and len(str(stderr)) > 0:
        print(f"stderr:\n{stderr}")
        result = False

    return result


if __name__ == "__main__":
    while True:
        RunAsProcess(["bash", "spi_reset.sh"], "/weatherstation")

        RunAsProcess(["python", "-m", "hoymiles", "-c",
                     "/ahoy_work/ahoy.yml"], "/ahoy", 10)  # *60)

        RunAsProcess(["bash", "spi_reset.sh"], "/weatherstation")

        pigpiod_process = CreateProcess(["pigpiod"])
        RunAsProcess(["python", "Hub.py"], "/weatherstation", 10)

        try:
            pigpiod_process.terminate()
            print("waiting for pigpiod to end")
            pigpiod_process.wait(10)
        except subprocess.TimeoutExpired:
            pigpiod_process.kill()

        break
