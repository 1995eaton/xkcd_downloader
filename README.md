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
python xkcd_image.py 150-170
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
python xkcd_image.py 188-250 -download-only
```
Fetch all comics:
```shell
python xkcd_image.py -fetch-all
```
Fetch all comics (images-only):
```shell
python xkcd_image.py -fetch-all -download-only
```

Configuration
-------------

Title font size, alt text font size, and line offset can be changed through the variables in the top of the script. The script looks for TTF fonts ('title.ttf' and 'alt.ttf') located in the script directory.
