import os
import sys
import boto3
from dotenv import load_dotenv

def load():
    #load the secrets into variables
    load_dotenv()
    aws_acess_key = os.getenv('AWS_ACCESS_KEY')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    bucket = os.getenv('bucket')

    #set up our AWS connection
    s3_client = boto3.client(
        's3'
        , aws_access_key_id = aws_acess_key
        , aws_secret_access_key = aws_secret_key
    )

    try:
        try:
            #test if the connect to AWS has been successful, if not quit the script
            s3_client.list_objects_v2(Bucket=bucket)
        except:
            print('Access to AWS denied')
            sys.exit(1)

        #inside the data folder, create a list of file names that are json    
        dir = 'data'
        file = [f for f in os.listdir(dir) if f.endswith('.json')]
        #if there is at least file to upload, push it to S3 and delete it locally
        if len(file)>0:
            filename = dir + '/' + file[0]
            s3filename = file[0]
            s3_client.upload_file(filename, bucket, s3filename)
            print('Upload successful ✅')
            os.remove(filename)
        else:
            print('No files to upload 😔')
    except Exception as e:
        print(e)
        raise e