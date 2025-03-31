import platform
import psutil
import subprocess




def get_all_cpu():
    """
    Get CPU model names for both Windows and Linux.
    Returns a sorted list of unique CPU model names.
    """
    if platform.system() == "Windows":
        try:
            cmd = "powershell -Command \"Get-WmiObject -Class Win32_Processor | Select-Object -ExpandProperty Name\""
            output = subprocess.check_output(cmd, shell=True).decode()
            model_names = [name.strip() for name in output.split('\n') if name.strip()]
            return sorted(set(model_names))
        except Exception as e:
            return [f"Error retrieving CPU info: {e}"]
    else:  # Linux
        try:
            output = subprocess.check_output("cat /proc/cpuinfo", shell=True).decode()
            model_names = []
            for line in output.split("\n"):
                if "model name" in line:
                    _, val = line.split(":", 1)
                    model_names.append(val.strip())
            return sorted(set(model_names))
        except Exception as e:
            return [f"Error retrieving CPU info: {e}"]

def get_all_gpu():
    """
    Get GPU information for both Windows and Linux.
    Returns a list of GPU model names.
    """
    if platform.system() == "Windows":
        try:
            # Filter out GPUs with empty names and get unique entries
            cmd = "powershell -Command \"Get-CimInstance Win32_VideoController | Select-Object -Unique Name | ForEach-Object {$_.Name}\""

            output = subprocess.check_output(cmd, shell=True).decode().strip()
            gpu_list = [line.strip() for line in output.split('\n') if line.strip()]
            return gpu_list if gpu_list else ["No GPU found"]
        except Exception as e:
            return [f"Error retrieving GPU info: {e}"]
    else:  # Linux
        try:
            # Get GPUs using PCI class codes for display (0300) and 3D controllers (0302)
            cmd = "lspci -nn | grep -E '\\[0300\\]|\\[0302\\]'"
            output = subprocess.check_output(cmd, shell=True).decode()
            gpu_list = []
            for line in output.split("\n"):
                line = line.strip()
                if line:
                    # Extract model name from lspci output
                    parts = line.split(':', 1)
                    if len(parts) > 1:
                        name_part = parts[1].split(' [')[0].strip()
                        gpu_list.append(name_part)
            return sorted(set(gpu_list)) if gpu_list else ["No GPU found"]
        except Exception as e:
            return [f"Error retrieving GPU info: {e}"]

def gather_machine_specs():
    """
    Gathers system information programmatically for both Windows and Linux.
    """
    info = {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "cpus": get_all_cpu(),
        "gpu": get_all_gpu(),
        "memory_gb": round(psutil.virtual_memory().total / (1024**3))  # Removed decimal places
    }
    return info


def convert_ns(ns):
    # Calculate minutes and remaining seconds
    total_seconds = ns // 1000000000
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    return minutes, seconds

def add_time_dicts(*time_dicts):
    total_minutes = 0
    total_seconds = 0

    # Sum up the minutes and seconds from each dictionary.
    for t in time_dicts:
        total_minutes += t.get('minutes', 0)
        total_seconds += t.get('seconds', 0)

    # Convert seconds to minutes if 60 seconds or more.
    extra_minutes, remaining_seconds = divmod(total_seconds, 60)
    total_minutes += extra_minutes

    return {'minutes': total_minutes, 'seconds': remaining_seconds}

