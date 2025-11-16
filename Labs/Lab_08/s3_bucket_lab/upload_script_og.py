import boto3

s3 = boto3.client('s3', region_name='us-east-1')

bucket = 'ds2002-f25-hwk8jq'
local_file = 'google_logo.png'

with open(local_file, 'rb') as data:
    s3.put_object(
        Body=data,
        Bucket=bucket,
        Key=local_file
    )

url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket, 'Key': local_file},
    ExpiresIn=60
)

print(url)
