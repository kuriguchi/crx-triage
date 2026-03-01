import argparse
import os
import subprocess
import zipfile
from pathlib import Path
from rich.console import Console
from rich.progress import track

console = Console()

ROOT = Path(__file__).resolve().parents[2] # project root

def download_dataset(key: str) -> None:
    """Download a single dataset via registry key."""
    console.print(f"Downloading dataset: {key}", style="bold green")

    cmd = [
        "kaggle",
        "datasets",
        "download",
        "-d",
        "xhlulu/vinbigdata-chest-xray-resized-png-256x256",
        "-p",
        str(ROOT / "data" / "raw" / "vinbigdata"),
        "--unzip",
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"Error downloading dataset: {e}", style="bold red")

def main():
    # parser = argparse.ArgumentParser(description="Download CXR dataset from Kaggle")
    # parser.add_argument(
    #     "--dataset",
    #     help="Dataset to download",
    # )

    print(ROOT)

    # download dataset
    download_dataset("vinbigdata")

if __name__ == "__main__":
    main()