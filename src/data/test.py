import kaggle
kaggle.api.authenticate()
# kaggle.api.dataset_download_files('xhlulu/vinbigdata-chest-xray-resized-png-256x256', path='./data/raw/vinbigdata', unzip=True)
kaggle.api.dataset_download_files('soumikrakshit/github-chats', path='./data/test', unzip=True)