from monitor import logging as log, static
from credentials import load
from file_path import path
import os

class DataDownloader(metaclass=static):

    def authenticate_kaggle():
        """Authenticate Kaggle API"""
        try:
            load.api.authenticate()
            log.info("✅ Kaggle API authenticated successfully!")
        except Exception as e:
            log.error(f"❌ Failed to authenticate Kaggle API: {e}")
    
    def initiate_os():
        """Create download directory if it doesn't exist"""
        if not os.path.exists(path.download_dir):
            os.makedirs(path.download_dir)

    def download_data():
        """Downloads the dataset from Kaggle"""
        try:
            log.info("🔄 Downloading dataset...")
            load.api.dataset_download_files(load.data_set_name, path.download_dir, unzip=True)
            log.info("✅ Dataset downloaded successfully!")
        except Exception as e:
            log.info(f"❌ Error downloading dataset: {e}")

