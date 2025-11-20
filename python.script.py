import pandas as pd
from google.cloud import storage
from google.colab import auth
from google.cloud import bigquery

project_id = 'aerobic-coast-478721-s5'
bucket_name = 'cis9440-assignment1-bikedata'
file_name = 'austin_metrobike.csv'
dataset_id = 'austin_data'
table_id = 'trips_table'
url = "https://data.austintexas.gov/resource/tyfh-5r8s.json"

df = pd.read_json(url)
df.to_csv(file_name, index=False)

auth.authenticate_user()

storage_client = storage.Client(project=project_id)
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(file_name)
blob.upload_from_filename(file_name)

print("Data uploaded to Google Cloud")

client = bigquery.Client(project=project_id)

full_dataset_ref = f'{project_id}.{dataset_id}'
full_table_ref = f'{full_dataset_ref}.{table_id}'
bucket_uri = f'gs://{bucket_name}/{file_name}'

client.create_dataset(full_dataset_ref, exists_ok=True)

job_config = bigquery.LoadJobConfig(
    autodetect=True,                
    skip_leading_rows=1,             
    write_disposition="WRITE_TRUNCATE" 
)

load_job = client.load_table_from_uri(bucket_uri, full_table_ref, job_config=job_config)
load_job.result()

print("Data loaded into BigQuery")
