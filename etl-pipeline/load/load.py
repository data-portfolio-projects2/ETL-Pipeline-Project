from monitor import logging as log, static
from google.cloud import bigquery
from credentials import load
from processed import processed
from pandas_gbq import to_gbq
from category import order
import pandas as pd
import os



class Loader(metaclass=static):

    def completed_orders():
        """Filter completed orders"""
        try:
            log.info("🔄 Filtering completed orders...")
            completed = processed.sales()
            completed = completed.compute()
            completed = completed[completed['order_status'] == 'Completed']
            valid = order.status
            df = completed[completed['order_status'].isin(valid)]
            df['order_status'] = df['order_status'].astype(str)
            log.info(df['order_status'].dtype)
            log.info("✅ Completed orders successfully filtered!")
            return df
        except Exception as e:
            log.error(f"❌ Error filtering completed orders: {e}")
            return None

    def transform_price(df):
        """Transform total price values"""
        try:
            log.info("🔄 Transforming total price values to numeric...")
            total_price = df.copy()
            total_price["total_price"] = total_price["total_price"].astype(str)
            valid = r"^\d+(\.\d+)?$"
            valid = total_price["total_price"].str.match(valid, na=False)
            df = total_price[valid]
            df["total_price"] = pd.to_numeric(df["total_price"], errors="coerce")
            df = df.rename(columns={"total_price": "sales"})
            log.info(df['sales'].dtype)
            log.info("✅ Total price values successfully transformed!")
            return df
        except Exception as e:
            log.error(f"❌ Error transforming total price values: {e}")
            return None
    
    def transform_dates(df):
        """Transform dates to datetime values"""
        try:
            log.info("🔄 Transforming dates to datetime values...")
            date = df.copy()
            date["purchase_date"] = date["purchase_date"].astype(str)
            valid_format = date["purchase_date"].str.match(r"^\d{4}-\d{2}-\d{2}$", na=False) 
            date = date[valid_format]
            df["purchase_date"] = pd.to_datetime(df["purchase_date"], errors="coerce")
            log.info(df['purchase_date'].dtype)
            log.info("✅ Dates successfully transformed!")
            return df
        except Exception as e:
            log.error(f"❌ Error transforming dates: {e}")
            return None  

    def create_sales(df):
        """Create sales data"""
        try:
            log.info("🔄 Creating sales data...")
            sales = df.copy()
            sales = sales.dropna()
            log.info("✅ Sales data successfully created!")
            log.info("\n%s", sales.head())
            return sales
        except Exception as e:
            log.error(f"❌ Error creating sales data: {e}")
            return None
    
    def bigquery_credentials():
        """Authenticate BigQuery credentials"""
        try:
            log.info("🔄 Authenticating BigQuery credentials...")
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=load.google_credentials
            client = bigquery.Client(project=load.project_id)
            log.info("✅ BigQuery credentials successfully authenticated!")
            return client
        except Exception as e:
            log.error(f"❌ Error authenticating BigQuery credentials: {e}")
            return None
        
    def create_schema():
        """Create BigQuery schema"""
        try:
            log.info("🔄 Creating BigQuery schema...")
            schema = [
                {"name": "order_id", "type": "STRING"},
                {"name": "purchase_date", "type": "DATE"},
                {"name": "order_status", "type": "STRING"},
                {"name": "sales", "type": "FLOAT"},
            ]
            log.info("✅ BigQuery schema successfully created!")
            return schema
        except Exception as e:
            log.error(f"❌ Error creating BigQuery schema: {e}")
            return None

    def create_table(df):
        """Uploads DataFrame to BigQuery with authentication and schema."""
        try:
            log.info("🔄 Uploading DataFrame to BigQuery...")
            client = Loader.bigquery_credentials()
            schema = Loader.create_schema()
            project_id = load.project_id
            dataset_id = load.dataset_id
            table_id = load.table_id
            table_path = f"{project_id}.{dataset_id}.{table_id}"
            to_gbq(df, table_path, project_id=project_id, if_exists="replace", table_schema=schema, credentials=client._credentials)
            log.info(f"✅ DataFrame successfully uploaded to BigQuery: {table_path}")
        except Exception as e:
            log.error(f"❌ Error uploading DataFrame to BigQuery: {e}")
            return None
