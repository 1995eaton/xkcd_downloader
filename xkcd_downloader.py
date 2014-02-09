#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageFont
from requests import get
from random import randrange
from textwrap import wrap
from json import loads
from re import search
import argparse
import os


class xkcd_downloader:

    def __init__(self, download_dir):
        if not os.path.exists(download_dir+os.path.sep):
            print("Error:", "'"+download_dir+"', no such directory")
            raise SystemExit
        if not os.access(download_dir, os.W_OK):
            print("Error:", "'"+download_dir+"', permission denied")
            raise SystemExit
        self.download_dir = download_dir
        self.title_fontsize = 28
        self.alt_fontsize = 18
        self.line_offset = 10

    def download_json(self, comic_number):
        if comic_number < 0:
            return None
        try:
            if comic_number == 0:
                return get("http://xkcd.com/info.0.json").json()
            else:
                return get("http://xkcd.com/{0}/info.0.json".
                           format(comic_number)).json()
        except (requests.exceptions.ConnectionError, ValueError):
            return None

    def text_wrap(self, font, text, image_width, i=0):
        lines = [[]]
        text = text.split(" ")
        while len(text) > 0:
            while len(text) > 0 \
                    and font.getsize(" ".join(lines[i]))[0] < image_width:
                if font.getsize(text[0]+" "+" ".join(lines[i]))[0] \
                        > image_width*0.95:
                    if len(lines[i]) == 0:
                        text[0] = text[0][:len(text[0])//2+1] \
                            + " " + text[0][:len(text[0])//2+1:]
                        text = text[0].split(" ") + text[1:]
                    break
                lines[i].append(text[0])
                text.pop(0)
            i += 1
            lines.append([])
        sub = []
        for e, i in enumerate(lines):
            if font.getsize(" ".join(lines[e]))[0] > image_width:
                temp_str = ""
                for c in "".join(i):
                    if font.getsize(temp_str+c)[0] > image_width:
                        lines[i] = lines[i][:len(lines[i])//2] \
                            + lines[i][len(lines[i])//2:]
                        break
                    temp_str += c
                sub.append(temp_str)
                del lines[e]
        lines = [i for i in lines if len(i) != 0]
        for c in [i for i in sub if len(i) != 0]:
            lines.append(c)
        return lines

    def add_text(self, image, title, alt, tfont='xkcd.ttf',
                 afont='xkcd.ttf'):

        try:
            img = Image.open(image)
        except OSError:
            return

        tfont = ImageFont.truetype("xkcd.ttf", self.title_fontsize)
        afont = ImageFont.truetype("xkcd.ttf", self.alt_fontsize)
        twidth, theight = tfont.getsize(title)
        awidth, aheight = afont.getsize(alt)
        line_padding = 5
        draw = ImageDraw.Draw(img)
        lines = self.text_wrap(tfont, title, img.size[0])
        lheight = max([tfont.getsize(" ".join(i))[1] for i in lines])
        lheight_total = (lheight+line_padding)*(len(lines))+line_padding*4
        title_crop = (0, -1*lheight_total, img.size[0], img.size[1])
        img = img.crop(title_crop)
        w, h = img.size
        old_h = h
        draw = ImageDraw.Draw(img)
        lheight_total = line_padding
        for i in lines:
            draw.text((w/2-tfont.getsize(" ".join(i))[0]/2,
                      lheight_total),
                      " ".join(i),
                      font=tfont,
                      fill=0xffffff)
            lheight_total += lheight + line_padding
        lheight_total = line_padding
        lines = self.text_wrap(afont, alt, w)
        lheight = max([afont.getsize(" ".join(i))[1] for i in lines])
        lheight_total = lheight*len(lines)
        alt_crop = (0, 0, img.size[0],
                    img.size[1]+lheight_total+(len(lines)+3)*line_padding)
        img = img.crop(alt_crop)
        draw = ImageDraw.Draw(img)
        lheight_total = old_h + line_padding
        for i in lines:
            if not i:
                continue
            draw.text((w/2-afont.getsize(" ".join(i))[0]/2,
                      lheight_total),
                      " ".join(i),
                      font=afont,
                      fill=0xffffff)
            lheight_total += lheight + line_padding

        img.save(image)

    def download_images(self, comic_number, download_only):
        images = []
        if comic_number == 404:
            return
        if comic_number == 0:
            print("Fetching comic -> Latest".format(comic_number))
        else:
            print("Fetching comic -> {0}".format(comic_number))
        info = self.download_json(comic_number)
        if not info:
            print("Error: URL could not be retrieved")
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
                self.add_text(self.download_dir+'/'+image, title, alt)

    def download_all(self, download_only):
        for i in range(1, self.download_json(0)['num']+1):
            self.download_images(i, download_only)

    def download_random(self, download_only, iterations=1):
        info = self.download_json(0)
        if not info:
            raise Exception("Error URL could not be reached!")
        else:
            for i in range(iterations):
                self.download_images(randrange(1, info['num']+1),
                                     download_only)


def main():

    parser = argparse.ArgumentParser(description='Retrieve and embed the\
                                     titles and alt text from XKCD comics\
                                     into single images.', prefix_chars='-+')
    parser.add_argument('N', type=int, nargs='*', help='an integer or set\
                        of integers greater than or equal to zero')
    parser.add_argument('-r', '--range', action="store", metavar='N',
                        type=int, nargs=2, help='fetch comics within\
                        a certain range')
    parser.add_argument('-o', '--output-dir', metavar='DIRECTORY',
                        action='store', default='./', help='change the\
                        output directory. default: current directory')
    parser.add_argument('-a', '--all', action='store_true',
                        help='fetch all comics')
    parser.add_argument('-d', '--download-only', action='store_true',
                        help='download images only')
    parser.add_argument('--random', metavar='ITERATIONS', type=int,
                        help='fetch random comics', nargs='?', const=1)
    args = parser.parse_args()

    x = xkcd_downloader(args.output_dir)
    if args.range:
        if args.N or args.random or args.all:
            raise argparse.ArgumentTypeError("Value may not be used in\
                                             addition to the --range flag")
        else:
            for i in range(args.range[0], args.range[1]+1):
                x.download_images(i, args.download_only)
            return
    if args.all:
        if args.N or args.random:
            raise argparse.ArgumentTypeError("Value may not be used in\
                                             addition to the --all flag")
        return x.download_all(args.download_only)

    if args.random:
        if args.N:
            raise argparse.ArgumentTypeError("'{0}': Value may not be used\
                                             in addition to the --random\
                                             flag".format(args.N))
        return x.download_random(args.download_only, args.random)
    else:
        if not args.N:
            parser.print_help()
        for i in args.N:
            x.download_images(i, args.download_only)
        return

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
