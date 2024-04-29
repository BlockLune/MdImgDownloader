#!/usr/bin/env python
import argparse
import os
import re
import time
import urllib.parse
import urllib.request


def download_image(img_url: str, save_path: str) -> str:
    """Download an image from a url and save it to a directory.

    Args:
        img_url (str): url of the image
        save_path (str): path to save the image

    Returns:
        str: new path of the image if downloaded, or the original url

    Example:
        download_image("https://example.com/image.jpg", "images") returns "images/1234567890.123_image.jpg" if downloaded successfully, or "https://example.com/image.jpg" if failed
    """
    img_file_name = (
        str(time.time()) + "_" + os.path.basename(urllib.parse.urlparse(img_url).path)
    )  # new name: timestamp + the original name
    file_path = os.path.join(save_path, img_file_name)
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
        "Accept-Encoding": "none",
        "Accept-Language": "en-US,en;q=0.8",
        "Connection": "keep-alive",
    }
    print(f"Trying to download {img_url} ...")
    try:
        req = urllib.request.Request(img_url, headers=headers)
        response = urllib.request.urlopen(req)
        with open(file_path, "wb") as f:
            f.write(response.read())
        print(f"Downloaded {img_url} to {file_path}")
        return os.path.join(os.path.basename(save_path), img_file_name)
    except Exception as e:
        print(f"Error downloading {img_url}: {str(e)}")
        return img_url


def create_image_dir(base_path: str, image_dir_name: str) -> str:
    """Create a directory for images.

    Args:
        base_path (str): parent directory
        image_dir_name (str): name of the directory

    Returns:
        str: full path of the directory
    """
    image_dir = os.path.join(base_path, image_dir_name)
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    return image_dir


def get_img_dir_basename_from_md_basename(md_file_basename: str) -> str:
    """Get the image directory name from a markdown file name.

    Args:
        md_file_name (str): markdown file name

    Returns:
        str: image directory name
    """
    return os.path.splitext(md_file_basename)[0]


my_parser = argparse.ArgumentParser(
    prog="MdImgDownloader",
    description="Download images in Markdown files and update links",
)
my_parser.add_argument(
    "--only-basename-link",
    action="store_true",
    help="by default, link will be updated to `OUTPUT_DIR/IMG_NAME`. If this flag is set, link will be updated to `IMG_NAME` only",
)
my_parser.add_argument("dir", nargs="+", type=str, help="directory of markdown files")
my_parser.add_argument("-o", "--output-dir", type=str, help="directory to save images")
args = my_parser.parse_args()

for md_dir in args.dir:
    for root, dirs, files in os.walk(md_dir):
        for file in files:
            if not file.endswith(".md"):
                continue
            file_path = os.path.join(root, file)
            image_dir = create_image_dir(
                root,
                (
                    args.output_dir
                    if args.output_dir
                    else get_img_dir_basename_from_md_basename(file)
                ),
            )
            with open(file_path, "r") as f:
                content = f.read()

            new_content = content
            for img_url in re.findall(r"!\[.*\]\((.*)\)", content):
                new_img_path = download_image(img_url, image_dir)
                new_content = new_content.replace(
                    img_url,
                    (
                        new_img_path
                        if not args.only_basename_link
                        else os.path.basename(new_img_path)
                    ),
                )

            with open(file_path, "w") as f:
                f.write(new_content)
            print(f"Updated file {file_path}")
