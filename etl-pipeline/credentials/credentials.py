from kaggle.api.kaggle_api_extended import KaggleApi

class load:
    """Storing all credentials"""
    data_set_name = "berkayclik/fake-passenger-name-record-pnr-data-amadeus" # for testing purposes
    #data_set_name = "cameronseamons/electronic-sales-sep2023-sep2024"
    #csv = 'C:/Users/loydt/Documents/datasets/raw/Electronic_sales_Sep2023-Sep2024.csv'
    csv = "C:/Users/loydt/Documents/datasets/raw/trips.csv"
    api = KaggleApi()
    project_id = ""
    dataset_id = "sales_data"
    table_id = "completed_orders"
    google_credentials = ""
    postgresql_host = "localhost"
    postgresql = "postgres"
    postgresql_pass = ""
    postgresql_port = ""
