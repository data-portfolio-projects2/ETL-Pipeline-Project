from monitor import logging as log, static
from load import Loader as authenticate
from sqlalchemy import create_engine
from credentials import load


class DataIngestor(metaclass=static):
            
    def query_table():
        """Query BigQuery table"""
        try:
            client = authenticate.bigquery_credentials()
            log.info("🔄 Querying BigQuery table...")
            query = f"""
            SELECT * 
            FROM `{load.dataset_id}.{load.table_id}`
            """
            query_job = client.query(query)
            df = query_job.to_dataframe()
            log.info("✅ Query successfully executed!")
            return df
        except Exception as e:
            log.error(f"❌ Error querying BigQuery table: {e}")
            return None
    
    def load_to_postgres(df):
        """Load DataFrame into PostgreSQL"""
        DB_HOST = load.postgresql_host
        DB_NAME = load.postgresql
        DB_USER = load.postgresql
        DB_PASS = load.postgresql_pass
        DB_PORT = load.postgresql_port
        try:
            log.info("🔄 Loading data into PostgreSQL...")
            engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
            df.to_sql("sales_data", engine, if_exists="replace", index=False)
            log.info("✅ Data successfully loaded into PostgreSQL!")
        except Exception as e:
            log.info(f"❌ Error loading data into PostgreSQL: {e}")
