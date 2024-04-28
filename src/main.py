#!/usr/bin/env python
from utils import create_image_dir, download_image
import os
import re

# Change this to the root directory of your md files
MD_FILES_ROOT_DIR = "md_files"
IMG_DIR_NAME = "images"

for root, dirs, files in os.walk(MD_FILES_ROOT_DIR):
    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            image_dir = create_image_dir(root, IMG_DIR_NAME)
            with open(file_path, "r") as f:
                content = f.read()

            new_content = content
            for img_url in re.findall(r"!\[.*\]\((.*)\)", content):
                new_img_path = download_image(img_url, image_dir)
                new_content = new_content.replace(img_url, new_img_path)

            with open(file_path, "w") as f:
                f.write(new_content)
            print(f"Updated file {file_path}")
