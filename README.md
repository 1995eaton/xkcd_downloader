xkcd_downloader
===============

Python modules required: Pillow
```shell
sudo pip install Pillow
```
Example-usage
-------------

Fetch comics 150 through 170:
```shell
python xkcd-image.py 150-170
```
Fetch the most recent strip:
```shell
python xkcd-image.py 0
```
Fetch comic 188:
```shell
python xkcd-image.py 188
```

Configuration
-------------

Title font size, alt text font size, line wrap width, and line offset can be changed through the variables in the top of the script. The script looks for TTF fonts ('title.ttf' and 'alt.ttf') located in the script directory.
