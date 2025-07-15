from monitor import logging as log, static, memory_usage as memory, time_execution as time

from credentials import load
import dask.dataframe as dd
from file_path import path


class Convert(metaclass=static):

    def extract_file():
        """Extract csv file"""
        csv_file = load.csv
        try:
            log.info("🔄 Extracting file...")
            df = dd.read_csv(csv_file, blocksize="100MB", dtype=str)
            log.info("✅ CSV file extracted successfully!")
            return df  
        except Exception as e:
            log.info(f"❌ Failed to extract file in chunks due: {e}")

    def to_parquet(data):
        """Convert csv file to parquet"""
        file_path = path.parquet_folder
        try:
            log.info("🔄 Converting data to parquet...")
            log.info(f"✅ Saving parquet to: {file_path}")
            df = data.to_parquet(file_path, engine="pyarrow", compression="snappy")
            log.info("✅ CSV file was successfully converted to parquet")
            return df
        except Exception as e:
            log.info(f"❌ Error converting data to parquet: {e}")

    @time
    @memory
    def __call__(self):
        df = self.extract_file()
        self.to_parquet(df)

  





