XKCD Downloader
===============

Python modules required: Pillow
```shell
sudo pip install Pillow
```
Example-usage
-------------

Fetch comics 150 through 170:
```shell
python xkcd_image.py -r 150 170
```
Specify output directory (default: './'):
```shell
python xkcd_image.py -o images
```
Fetch the most recent strip:
```shell
python xkcd_image.py 0
```
Fetch comic 188:
```shell
python xkcd_image.py 188
```
Fetch comics 188, 200, and 350:
```shell
python xkcd_image.py 188 200 350
```
Fetch only the image:
```shell
python xkcd_image.py -d 188
```
Fetch all comics:
```shell
python xkcd_image.py -a
```
Fetch all comics (images-only):
```shell
python xkcd_image.py -ad
```
Fetch a random comic:
```shell
python xkcd_image.py --random
python xkcd_image.py --random -d
```
Fetch 5 random comics:
```shell
python xkcd_image.py --random 5
python xkcd_image.py --random 5 -d
```

Configuration
-------------

Title font size, alt text font size, and line offset can be changed through the variables in the top of the script. The script looks for TTF fonts ('title.ttf' and 'alt.ttf') located in the script directory.
