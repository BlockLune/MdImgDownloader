#!/usr/bin/env python
from utils import create_image_dir, download_image
import os
import re


def get_img_dir_basename(md_file_basename: str) -> str:
    """Get the image directory name from a markdown file name.

    Args:
        md_file_name (str): markdown file name

    Returns:
        str: image directory name
    """
    return os.path.splitext(md_file_basename)[0]


# Put this script to your `source` dir in your Hexo project
MD_FILES_ROOT_DIR = "_posts"

for root, dirs, files in os.walk(MD_FILES_ROOT_DIR):
    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            image_dir = create_image_dir(root, get_img_dir_basename(file))
            with open(file_path, "r") as f:
                content = f.read()

            new_content = content
            for img_url in re.findall(r"!\[.*\]\((.*)\)", content):
                new_img_path = download_image(img_url, image_dir)
                new_content = new_content.replace(img_url, os.basename(new_img_path))

            with open(file_path, "w") as f:
                f.write(new_content)
            print(f"Updated file {file_path}")
