from monitor import logging as log, static
from file_path import path


class DataSaver(metaclass=static):

    def save_df(df):
        """Save the dataframe as a csv file"""
        try:
            log.info("🔄 Saving dataframe...")
            output_path = f"{path.output_dir}data.csv"
            df.to_csv(output_path, single_file=True, index=False)
            log.info("✅ Dataframe successfully saved!")
        except Exception as e:
            log.error(f"❌ Error saving dataframe: {e}")
            return None

    def save_col(df):
        """Save each column as a separate csv file"""
        try:
            log.info("🔄 Saving individual columns...")
            for col in df.columns:
                col_df = df[[col]]
                col_path = f"{path.output_dir}{col}.csv"
                col_df.to_csv(col_path, index=False, single_file=True)
            log.info("✅ Saving individual columns successful!")
        except Exception as e:  
            log.error(f"❌ Error saving columns: {e}")
            return None
    
    def sales_data(df):
        """Filter sales data"""
        try:
            log.info("🔄 Filtering sales data...")
            sales = df[['order_id', 'purchase_date', 'order_status', 'total_price']].copy()
            output_path = f"{path.output_dir}sales.csv" 
            sales.to_csv(output_path, single_file=True, index=False)
            log.info("✅ Sales data successfully filtered!")
        except Exception as e:
            log.error(f"❌ Error filtering sales data: {e}")
            return None
