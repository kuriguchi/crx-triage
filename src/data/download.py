import argparse
import os
import subprocess
import zipfile
from pathlib import Path
from rich.console import Console
from rich.progress import track

console = Console()

# registry of datasets with metadata, add more entries as needed
DATASETS = {
    "vinbigdata": {
        "kaggle_key": "xhlulu/vinbigdata-chest-xray-resized-png-256x256",
        "dest": "data/raw/vinbigdata",
        "description": "VinBigData Chest X-ray Resized PNG 256x256",
        "note": (
            "Full 1024px version: 'xhlulu/vinbigdata-chest-xray-resized-png-1024x1024'\n"
            "Full 512px version: 'xhlulu/vinbigdata'\n"
            "  The 256px version above is fine for initial experiments.\n"
            "  Switch to 512px or 1024px for final training runs."
        ),
    }
}

ROOT = Path(__file__).resolve().parents[2] # project root

def download_dataset(key: str, force: bool = False) -> None:
    """Download a single dataset via registry key."""
    if key not in DATASETS:
        console.print(f"Dataset key '{key}' not found in registry.", style="bold red")
        return

    cfg = DATASETS[key]
    dest = ROOT / cfg["dest"]
    dest.mkdir(parents=True, exist_ok=True)

    # skip download if dest already exists and force is not set
    if not force and any(dest.iterdir() if dest.exists() else []):
        console.print(f"Dataset '{key}' already exists at {dest}. Use --force to re-download.", style="bold yellow")
        return

    console.print(f"Downloading dataset: {key}", style="bold green")

    # command to download and unzip dataset using Kaggle CLI
    cmd = [
        "kaggle",
        "datasets",
        "download",
        "-d",
        cfg["kaggle_key"],
        "-p",
        str(dest),
        "--unzip",
    ]

    try:
        console.print(f"Running command: {' '.join(cmd)}", style="dim")
        subprocess.run(cmd, check=True)
        console.print(f"Dataset '{key}' downloaded successfully to {dest}", style="bold green")
    except subprocess.CalledProcessError as e:
        console.print(f"Error downloading dataset: {e}", style="bold red")
        console.print("Make sure you have the Kaggle CLI installed and configured properly.", style="bold yellow")

def check_kaggle_auth() -> bool:
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    if not kaggle_json.exists():
        console.print("Kaggle API credentials not found. Please place kaggle.json in ~/.kaggle/", style="bold red")
        console.print("To get kaggle.json, go to Kaggle and create an API token from your account settings.", style="bold yellow")
        console.print("This should be the contents of kaggle.json:")
        console.print('{"username": "your_kaggle_username", "key": "your_kaggle_api_key"}', style="dim")
        return False

    console.print("Kaggle API credentials found.", style="bold green")
    return True

def main():
    parser = argparse.ArgumentParser(description="Download CXR dataset from Kaggle")
    parser.add_argument(
        "--dataset",
        choices=list(DATASETS.keys()),
        help="Dataset to download",
    )
    parser.add_argument("--all", action="store_true", help="Download all datasets in registry")
    parser.add_argument("--force", action="store_true", help="Force re-download even if dataset already exists")
    parser.add_argument("--list", action="store_true", help="List available datasets in registry")
    args = parser.parse_args()

    if args.list:
        console.print("Available datasets:", style="bold blue")
        for key, cfg in DATASETS.items():
            console.print(f"- {key}: {cfg['description']}")
            console.print(f"  Note: {cfg['note']}")
        return

    # check Kaggle authentication before attempting downloads
    if not check_kaggle_auth():
        return 

    if args.all:
        for key in DATASETS:
            download_dataset(key, force=args.force)
    elif args.dataset:
        download_dataset(args.dataset, force=args.force)
    else:
        parser.print_help()
        return

if __name__ == "__main__":
    main()