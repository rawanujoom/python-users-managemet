import boto3
from botocore.exceptions import ClientError
import os
from flask import request
from configuration.config import CONFIG


def upload_file(file, bucket, object_name):
    file_name = file.filename

    object_name = os.path.join(object_name, file_name)
    content_type = request.mimetype
    s3_client = boto3.client('s3', aws_access_key_id=CONFIG["AWS_ACCESS_KEY"],
                             aws_secret_access_key=CONFIG["AWS_SECRET_KEY"], )
    try:
        s3_client.put_object(Body=file,
                             Bucket=bucket,
                             Key=object_name,
                             ContentType=content_type)
    except ClientError as e:
        return False
    return True
