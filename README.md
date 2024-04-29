# Md Img Downloader

Download images in Markdown files and update links.

This project references [mufidu/download_imgs.py](https://gist.github.com/mufidu/f7b795f844f1ee4dc78e55123d5a398b) but is written independently.

## Usage

```bash
usage: MdImgDownloader [-h] [--only-basename-link] [-o OUTPUT_DIR] dir [dir ...]

Download images in Markdown files and update links

positional arguments:
  dir                   directory of markdown files

options:
  -h, --help            show this help message and exit
  --only-basename-link  by default, link will be updated to `OUTPUT_DIR/IMG_NAME`. If this flag is set, link will be updated to
                        `IMG_NAME` only
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        directory to save images
```

If you don't specify the `OUTPUT_DIR`, the script will create a dir based on the name of the md file.

If you want to use this script to update all the image links in your Hexo posts, run:

```bash
python MdImgDownloader /path-to-your-hexo-project/source/_posts --only-basename-link
```