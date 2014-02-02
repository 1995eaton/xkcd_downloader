#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
from requests import get
from random import randrange
from textwrap import wrap
from json import loads
from re import search
import argparse
import os


class XKCD_downloader:

    def __init__(self, download_dir):
        self.download_dir = download_dir
        self.title_fontsize = 28
        self.alt_fontsize = 18
        self.line_offset = 10

    def fetchJSON(self, comic_number):
        if comic_number < 0:
            return None
        try:
            if comic_number == 0:
                return get("http://xkcd.com/info.0.json").json()
            else:
                return get("http://xkcd.com/{0}/info.0.json".
                           format(str(comic_number))).json()
        except:
            return None

    def formatImage(self, image, title, alt, tfont='title.ttf',
                    afont='alt.ttf'):

        try:
            img = Image.open(image)
        except OSError:
            return

        wrap_width = int(img.size[0]*0.183+0.0025/self.alt_fontsize)

        title_font = ImageFont.truetype(tfont, self.title_fontsize)
        title_font_width, title_font_height = title_font.getsize(title)
        title = wrap(title, int(img.size[0]*0.09+0.0005))

        if not title or title[0] == '...' and len(title) == 1:
            title_crop = 0
        else:
            title_crop = title_font_height+self.line_offset*len(title)*2+15

        alt_font = ImageFont.truetype(afont, self.alt_fontsize)
        alt_font_width, alt_font_height = alt_font.getsize(alt)
        alt = wrap(alt, wrap_width-15)

        if not alt or alt[0] == '...' and len(alt) == 1:
            alt_crop = 0
        else:
            alt_crop = alt_font_height*len(alt)+self.line_offset*len(alt)+15

        img_width, img_height = img.size
        img = img.crop((0, -1*title_crop, img_width, img_height+alt_crop))
        img_width, img_height = img.size

        draw = ImageDraw.Draw(img)
        loffset_temp = self.line_offset
        for line in title:
            w, h = draw.textsize(line, font=title_font)
            draw.text(((img_width-w)/2, loffset_temp), line,
                      font=title_font, fill=0xffffff)
            loffset_temp += h
        loffset_temp = self.line_offset
        for line in alt:
            w, h = draw.textsize(line, font=alt_font)
            draw.text(((img_width-w)/2, img_height-alt_crop+loffset_temp-5),
                      line, font=alt_font, fill=0xffffff)
            loffset_temp += h+10

        img.save(image)

    def checkPath(self):
        if self.download_dir[-1] == '/':
            self.download_dir = self.download_dir[:-1]
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def fetchImages(self, comic_number, download_only):
        self.checkPath()
        images = []
        if comic_number == 404:
            return
        if comic_number == 0:
            print("Fetching comic -> Latest".format(comic_number))
        else:
            print("Fetching comic -> {0}".format(comic_number))
        info = self.fetchJSON(comic_number)
        if not info:
            print("Error: URL could not be reached!")
            return
        title, alt, num = info['safe_title'], info['alt'], str(info['num'])
        image = num+search("\.([a-z])+$", info['img']).group()
        with open(self.download_dir+'/'+image, 'wb') as image_file:
            req = get(info['img'], stream=True)
            for block in req.iter_content(1024):
                if block:
                    image_file.write(block)
                    image_file.flush()
            if not download_only and not search("\.gif", info['img']):
                print("Processing comic -> {0}".format(comic_number))
                self.formatImage(self.download_dir+'/'+image, title, alt)

    def getAll(self, download_only):
        for i in range(1, self.fetchJSON(0)['num']+1):
            self.fetchImages(i, download_only)

    def getRandom(self, download_only, iterations=1):
        info = self.fetchJSON(0)
        if not info:
            raise Exception("Error URL could not be reached!")
        else:
            for i in range(iterations):
                self.fetchImages(randrange(1, info['num']+1), download_only)


def main():

    parser = argparse.ArgumentParser(description='Retrieve and embed the titles and alt text from XKCD comics into single images.', prefix_chars='-+')
    parser.add_argument('N', type=int, nargs='*', help='an integer or set of integers greater than or equal to zero')
    parser.add_argument('-r', '--range', action="store", metavar='N', type=int, nargs=2, help='fetch comics within a certain range')
    parser.add_argument('-o', '--output-dir', metavar='DIRECTORY', action='store', default='./', help='change the output directory. default: current directory')
    parser.add_argument('-a', '--all', action='store_true', help='fetch all comics')
    parser.add_argument('-d', '--download-only', action='store_true', help='download images only')
    parser.add_argument('--random', metavar='ITERATIONS', type=int, help='fetch random comics', nargs='?', const=1)
    args = parser.parse_args()

    x = XKCD_downloader(args.output_dir)
    if args.range:
        if args.N or args.random or args.all:
            raise argparse.ArgumentTypeError("Value may not be used in addition to the --range flag".format(args.N))
        else:
            for i in range(args.range[0], args.range[1]+1):
                x.fetchImages(i, args.download_only)
            return
    if args.all:
        if args.N or args.random:
            raise argparse.ArgumentTypeError("Value may not be used in addition to the --all flag".format(args.N))
        return x.getAll(args.download_only)

    if args.random:
        if args.N:
            raise argparse.ArgumentTypeError("'{0}': Value may not be used in addition to the --random flag".format(args.N))
        return x.getRandom(args.download_only, args.random)
    else:
        if not args.N:
            parser.print_help()
        for i in args.N:
            x.fetchImages(i, args.download_only)
        return

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit

