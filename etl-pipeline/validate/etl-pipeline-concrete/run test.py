from download import DataDownloader as download
from multiprocessing import Process
from test import Convert

#d = download()
#d.authenticate_kaggle()
#d.initiate_os()
#d.download_data()

if __name__ == '__main__':
    converter = Convert()
    p = Process(target=converter.__call__) 
    p.start()
    p.join()
