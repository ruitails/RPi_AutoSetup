import platform
import subprocess


# Unix functions

# Checks if the OS is Linux or macOS
def is_linux():
    return platform.system() == "Linux"

def is_macos():
    return platform.system() == "Darwin"

# Lists removable devices on Linux
def list_removable_devices_linux():
    result = subprocess.run(['lsblk', '-o', 'NAME,SIZE,TYPE,MOUNTPOINT'], capture_output=True, text=True)
    print("[?] Available block devices:\n" + result.stdout)

# Lists removable devices on macOS
def list_removable_devices_macos():
    result = subprocess.run(['diskutil', 'list'], capture_output=True, text=True)
    print("[?] Available disks:\n" + result.stdout)

# Flashes an image to a device on Linux or macOS using dd
def flash_image_unix(image_path, device_path):
    print(f"[!] Flashing {image_path} to {device_path} using dd...")
    cmd = ["sudo", "dd", f"if={image_path}", f"of={device_path}", "bs=4M", "status=progress", "conv=fsync"]
    subprocess.run(cmd, check=True)
    print("[✓] Flash complete.")

# Windows functions 

# Checks if the OS is Linux or macOS
def is_windows():
    return platform.system() == "Windows"

# Lists removable devices on Windows
def list_removable_devices_windows():
    result = subprocess.run(['wmic', 'logicaldisk', 'get', 'DeviceID,VolumeName,Description'], capture_output=True, text=True)
    print("[?] Available disks:\n" + result.stdout)

# Flashes an image to a device on Windows (TO DO)
def flash_image_windows(image_path, device_path):
    print(f"[!] Windows flashing not implemented yet.")
    print(f"[>] Please use Raspberry Pi Imager or balenaEtcher to flash:\n   {image_path}")
