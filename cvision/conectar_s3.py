import boto3
import os

ACCESS_KEY = 'FAKE_ACCESS_KEY'
SECRET_KEY = 'FAKE_SECRET_KEY'

def conectar_bucket_s3(bucket_name):
    """Conecta com um bucket na Amazon S3."""
    #ACCESS_KEY = os.environ('ACCESS_KEY')
    #SECRET_KEY = os.environ('SECRET_KEY')

    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-1',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY)
    
    bucket = s3.Bucket(bucket_name)
    return bucket
    

    