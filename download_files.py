import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from tqdm import tqdm

load_dotenv()
conn_str = os.environ.get("CONNECTION_STRING")
blob_service = BlobServiceClient.from_connection_string(conn_str=conn_str)
container_client = blob_service.get_container_client('preliminarydata')
DATA_DIR = '/data'

def download_data():
    if not os.path.exists(DATA_DIR):
        # Create the directory
        os.makedirs(DATA_DIR)

    for blob_name in tqdm(container_client.list_blob_names(), total=13):
        csv_name = blob_name.split('/')[-1]
        with open(file=os.path.join(DATA_DIR, csv_name), mode="wb") as blob_file:
            downloaded_blob = container_client.download_blob(blob=blob_name)
            blob_file.write(downloaded_blob.readall())


if __name__ == '__main__':
    download_data()
