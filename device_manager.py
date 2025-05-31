from utils import *


def select_target_device(config):
    device = config.get("target_device", "auto")

    if device != "auto":
        return device

    print("[!] No target device specified. Scanning...")

    if is_linux():
        list_removable_devices_linux()
    elif is_macos():
        list_removable_devices_macos()
    elif is_windows():
        list_removable_devices_windows()
    else:
        raise RuntimeError("Unsupported OS")

    return input("[?] Enter the device path (e.g., /dev/sdX, /dev/disk2, E:\\): ").strip()


def flash_device(image_path, config):
    device_path = select_target_device(config)

    if is_linux() or is_macos():
        flash_image_unix(image_path, device_path)
    elif is_windows():
        flash_image_windows(image_path, device_path)
    else:
        raise RuntimeError("Unsupported OS")

