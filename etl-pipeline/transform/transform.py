from monitor import logging as log, static
from extract import dd
import numpy as np
import itertools


class DataTransformer(metaclass=static):

    def delete_col(df):
        try:
            log.info("🔄 Deleting unnecessary column...")
            df = df.drop(columns=['Add-ons Purchased'])
            log.info("✅ Column successfully deleted")
            return df
        except Exception as e:
            log.error(f"❌ Error deleting column: {e}")
            return None

    def remove_space(df):
        try:
            log.info("🔄 Removing trailing spaces...") 
            df = df.map_partitions(lambda partition: partition.apply(lambda col: col.str.strip() 
                                                                     if col.dtype == 'object' else col, axis=0))                                                                     
            log.info("✅ Removing trailing spaces successful!")
            return df
        except Exception as e:
            log.error(f"❌ Error removing trailing spaces: {e}")
            return None

    def lowercase_col(df):
        """Transform columns into lowercase"""
        try:
            log.info("🔄 Transforming columns into lowercase")
            df.columns = df.columns.str.lower()
            log.info("✅ Columns successfully transformed")
            return df
        except Exception as e:
            log.error(f"❌ Error transforming columns: {e}")
    
    def strip_space(df):
        """Remove trailing spaces in columns"""
        try:
            log.info("🔄 Removing trailing spaces")
            df.columns = df.columns.str.strip()
            log.info("✅ Trailing spaces successfully removed")
            return df
        except Exception as e:
            log.error(f"❌ Error removing trailing spaces: {e}")
    
    def replace_(df):
        """Replacing space w/ underscore"""
        try:
            log.info("🔄 Adding underscores")
            df.columns = df.columns.str.replace(' ', '_')
            log.info("✅ Underscore successfully added")
            return df
        except Exception as e:
            log.error(f"❌ Error adding underscore: {e}")
    
    def order_id(df):
        """Adding order IDs to a Dask DataFrame"""
        try:
            log.info("🔄 Adding order IDs...")
            letters = [chr(i) for i in range(65, 91)]  
            numbers = [str(i) for i in range(1, 10)]  
            main_ids = [l + n for l, n in itertools.product(letters, numbers)]
            expanded_ids = [f"{base}.{suffix}" for base in main_ids for suffix in range(1, 10)]
            more_expanded_ids = [f"{base}.{suffix}" for base in expanded_ids for suffix in range(1, 10)]

            order_ids = main_ids + expanded_ids + more_expanded_ids

            if len(order_ids) < len(df):
                raise ValueError("❌ Not enough unique Order_IDs generated for the dataframe.")
            order_ids_series = dd.from_array(np.array(order_ids[:len(df)]))
            df["Order_ID"] = order_ids_series
            log.info("✅ Order IDs successfully added")
            return df
        except Exception as e:
            log.error(f"❌ Error adding order IDs: {e}")
            return df 

    
