from pathlib import Path

DATASETS = {
    "vinbigdata": {
            "kaggle_key": "xhlulu/vinbigdata-chest-xray-resized-png-256x256",
            "dest": "data/raw/vinbigdata",      
    }
}
    
ROOT = Path(__file__).resolve().parents[2] # project root
dest = ROOT / DATASETS["vinbigdata"]["dest"]
print(any(dest.iterdir() if dest.exists() else []))