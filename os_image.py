import os
import requests
import shutil
import subprocess
from urllib.parse import urlparse

def download_image(url, dest_path):
    print(f"[+] Downloading image from {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(dest_path, 'wb') as f:
        shutil.copyfileobj(response.raw, f)

    print(f"[✓] Downloaded to {dest_path}")
    return dest_path

def extract_image(compressed_path):
    print(f"[+] Extracting image: {compressed_path}")
    if compressed_path.endswith(".xz"):
        extracted_path = compressed_path[:-3]  # remove .xz
        subprocess.run(["xz", "-d", "-k", compressed_path], check=True)
        print(f"[✓] Extracted to {extracted_path}")
        return extracted_path
    else:
        raise ValueError("Unsupported compression format for extraction.")

def get_os_image(config):
    os_image = config["os_image"]
    image_path = os_image["path"]

    if os_image["type"] == "download":
        if not os.path.exists(image_path):
            image_path = download_image(os_image["url"], image_path)
        else:
            print(f"[i] Using existing downloaded image at {image_path}")

    if os_image.get("auto_extract", False):
        image_path = extract_image(image_path)

    return image_path
