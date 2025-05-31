from config_loader import load_config
from os_image import get_os_image
from device_manager import flash_device

def main():
    config = load_config("config.yaml")
    image_path = get_os_image(config)
    flash_device(image_path, config)

if __name__ == "__main__":
    main()
