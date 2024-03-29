# peanuts-comic-preprocessing

Pre-processing code used to format Peanuts comic strip images

## Introduction

All the scripts within this repository were run on an ad-hoc basis. Some functionality was broken out into the `utils` directory where applicable.

I chose to use Python for this repo because of its robust support for file system traversal/interactions and image manipulation.

There are definitely ehancements/optimizations that could be made to many of the functions/scripts that I have written. Since much of this work by nature is "one and done", I did not spend excess time optimizing.

**NOTE: I am not making the dataset publicly available due to copyright concerns. I created [peanuts.today] as a personal research project with no intentions for personal gain or profit and would like to prevent others from doing so as well.**

## Data

Compressed files of raw and cropped comic images are available [here](https://console.aws.amazon.com/s3/buckets/peanuts-comics) (if you have access...)

## Scripts

Below is a list of the scripts found in this repo and their basic function.

#### bootstrap.py

Used to download/uncompress the raw and cropped images from S3.

#### download.py

Used to download the full, raw dataset to local file system

#### unzip.py

Unzips contents of the `zipped_images` directory

#### crop_images.py

Used to crop all images within the configured directory

#### get_strip_metadata.py

Extracts metadata from the strip using Tesseract OCR. Metadata includes page number and Month/Year of publication.

#### split_strips.py

Identifies individual strips in image files and saves each to separate file

#### fill_in_metadata_report.py

Takes the metadata report generated by `get_strip_metadata.py` and fills in the blanks. Since image pages alternate in what metadata they include, we need to fill in the blanks.

Before:

| Page | Month | Year |
|------|-------|------|
| 210  | May   |      |
| 211  |       | 1968 |
| 212  | May   |      |

After:

| Page | Month | Year |
|------|-------|------|
| 210  | May   | `1968` |
| 211  | `May` | 1968   |
| 212  | May   |  `1968`|

#### upload.py

Uploads image files and metadata to S3 and DynamoDB table

## Utilities

A list of some of the utilities that are used by the scripts

#### aws.py

Just a initializer of the AWS boto3 library that pulls credentials from the config utility (which gets them from environment variables)

#### config.py

Simple `configparser` utility that loads configuration from ini files in the `config` directory. Supports a `local.ini` file that is not versioned controlled that can override the `default.ini`.

#### crop.py

Exposes function to crop images of excess whitespace (and watermark border) and saves cropped images to file or renders them in OS-default image viewer (depending on arguments)

#### metadata.py

Exposes function to extract metadata from images. It grabs the bottom left/right quadrants of the image (sans watermark), sends them to Tesseract OCR for parsing, and returns results

#### split.py

Exposes function to identify and extract individual strips in single image file. Uses combination of whitespace and distance thresholds to know when there are multiple strips.
