# @file s3-uploader.py
# @author gpt-4o

# Configurations
bucket_name = ''
s3_subfolder = 'blog-imgs'  # Specify the subfolder path here, default to '' for root
aws_access_key = ''
aws_secret_key = ''
region_name = 'auto'
s3_endpoint = ''  # Specify your custom S3 endpoint here, or leave as '' to use default
public_url = ''  # Specify the public URL here
naming_rule = 'incremental'  # Options: 'original', 'incremental', 'timestamp_incremental'

from botocore.exceptions import NoCredentialsError
import boto3
import os
import re
import shutil
import time
import urllib.parse

# Initialize boto3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region_name,
    endpoint_url=s3_endpoint if s3_endpoint else None)

def upload_file(file_name, bucket, object_name):
    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"Uploaded {file_name} to s3://{bucket}/{object_name}")
    except FileNotFoundError:
        print(f"The file was not found: {file_name}")
    except NoCredentialsError:
        print("Credentials not available")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                process_markdown_file(root, file, directory)

def generate_new_file_name(img_name, img_count, timestamp):
    if naming_rule == 'original':
        return img_name
    elif naming_rule == 'incremental':
        return f"{img_count}.png"
    elif naming_rule == 'timestamp_incremental':
        return f"{timestamp}_{img_count}.png"
    else:
        raise ValueError("Invalid naming rule specified")

def process_markdown_file(root, file_name, base_directory):
    md_file_path = os.path.join(root, file_name)
    img_dir = os.path.join(root, os.path.splitext(file_name)[0])
    if not os.path.isdir(img_dir):
        return

    # Read the markdown file
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all image links using regex
    img_pattern = re.compile(r'!\[.*?\]\((.*?)\)')
    matches = img_pattern.findall(content)

    timestamp = str(int(time.time()))
    img_count = 0

    for img_name in matches:
        img_path = os.path.join(img_dir, img_name)
        if os.path.isfile(img_path):
            img_count += 1
            # Convert paths to lowercase and use relative path
            relative_path = os.path.relpath(img_dir, base_directory).lower()
            # Generate new file name
            new_file_name = generate_new_file_name(img_name, img_count, timestamp)
            s3_key = f"{relative_path}/{new_file_name}".replace('\\', '/')
            if s3_subfolder:
                s3_key = f"{s3_subfolder}/{s3_key}"
            upload_file(img_path, bucket_name, s3_key)
            # Generate the public URL for the image
            public_img_url = f"{public_url}/{urllib.parse.quote(s3_key)}"
            # Replace the image link in the markdown content
            content = content.replace(f'({img_name})', f'({public_img_url})')

    # Write the updated content back to the markdown file
    with open(md_file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # Remove the local image directory after uploading
    shutil.rmtree(img_dir)
    print(f"Deleted local directory: {img_dir}")

if __name__ == '__main__':
    current_directory = os.getcwd()
    process_directory(current_directory)
