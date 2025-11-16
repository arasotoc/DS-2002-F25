import requests
import boto3
import os

def download_file(url, file_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded to {file_path}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading: {e}")

image_url = "https://www.discoverboating.com/sites/default/files/Sailboat-Types_1.jpg"
file_name = "downloaded_image.gif"
path = os.path.join(os.getcwd(), file_name)

download_file(image_url, path)


bucket = "ds2002-f25-hwk8jq"
s3 = boto3.client("s3", region_name="us-east-1")

with open(path, "rb") as f:
    s3.put_object(
        Bucket= "ds2002-f25-hwk8jq",
        Key=file_name,
        Body=f
)

expires_in = 60

response = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': "ds-2002-F25-hwk8jq", 'Key': file_name},
    ExpiresIn=expires_in
)
