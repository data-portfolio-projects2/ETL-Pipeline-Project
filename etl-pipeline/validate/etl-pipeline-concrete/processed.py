import dask.dataframe as dd
from monitor import static

class processed(metaclass=static):

    def data():
        return dd.read_csv("C:/Users/loydt/Documents/datasets/processed/data.csv", dtype=str)
    
    def sales():
        return dd.read_csv("C:/Users/loydt/Documents/datasets/processed/sales.csv", dtype=str) # , usecols=lambda col: col != "Unnamed: 0"


