XKCD Downloader
===============

Python modules required: Pillow, requests
```shell
sudo pip install Pillow requests
```
Example-usage
-------------

Fetch comics 150 through 170:
```shell
python xkcd_downloader.py -r 150 170
```
Specify output directory (default: './'):
```shell
python xkcd_downloader.py -o images
```
Fetch the most recent strip:
```shell
python xkcd_downloader.py 0
```
Fetch comic 188:
```shell
python xkcd_downloader.py 188
```
Fetch comics 188, 200, and 350:
```shell
python xkcd_downloader.py 188 200 350
```
Fetch only the image:
```shell
python xkcd_downloader.py -d 188
```
Fetch all comics:
```shell
python xkcd_downloader.py -a
```
Fetch all comics (images-only):
```shell
python xkcd_downloader.py -ad
```
Fetch a random comic:
```shell
python xkcd_downloader.py --random
python xkcd_downloader.py --random -d
```
Fetch 5 random comics:
```shell
python xkcd_downloader.py --random 5
python xkcd_downloader.py --random 5 -d
```

Configuration
-------------

Title font size, alt text font size, and line offset can be changed through the variables in the top of the script. By default, the script looks for the TTF font file 'xkcd.ttf' located in the script directory.
