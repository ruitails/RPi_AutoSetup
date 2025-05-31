import yaml
import os

def load_config(path="config.yaml"):

    if not os.path.exists(path):
        raise FileNotFoundError(f"Condiguration file '{path}' not found.")
    
    with open(path, 'r') as file:
        config = yaml.safe_load(file)

    return config