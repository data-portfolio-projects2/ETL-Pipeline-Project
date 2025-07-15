from monitor import logging as log, static
from raw import raw
import dask.dataframe as dd

class DataExtractor(metaclass=static):

    def extract_data():
        try:
            log.info("🔄 Extracting CSV file...")
            df = dd.read_csv(raw.csv, dtype=str)   
            log.info("✅ CSV file extracted successfully!")
            return df
        except Exception as e:
            log.error(f"❌ Error extracting CSV file: {e}")
            return None
    
