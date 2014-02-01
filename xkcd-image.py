from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlopen
from textwrap import wrap
from json import loads
from sys import argv
import os

DOWNLOAD_DIRECTORY = "images"
TITLE_FONTSIZE = 28
ALT_FONTSIZE = 18
LINE_OFFSET = 11
WRAP_WIDTH = 30

def fetchJSON(comic_number):
  xkcd_json_url = "http://xkcd.com/info.0.json"
  if comic_number < 0:
    return
  elif comic_number == 0:
    xkcd_json = loads(urlopen(xkcd_json_url).read().decode('utf-8'))
  else:
    xkcd_json = loads(urlopen("http://xkcd.com/{0}/info.0.json".format(str(comic_number))).read().decode('utf-8'))
  return xkcd_json

def formatImage(image, title, alt, tfont = 'title.ttf', afont = 'alt.ttf'):

  global LINE_OFFSET, TITLE_FONTSIZE, ALT_FONTSIZE, WRAP_WIDTH, DOWNLOAD_DIRECTORY
  img = Image.open(DOWNLOAD_DIRECTORY+'/'+image)

  title_font = ImageFont.truetype(tfont, TITLE_FONTSIZE)
  title_font_width, title_font_height = title_font.getsize(title)
  title = wrap(title, WRAP_WIDTH)
  title_crop = title_font_height + LINE_OFFSET * (len(title) + 2)

  alt_font = ImageFont.truetype(afont, ALT_FONTSIZE)
  alt_font_width, alt_font_height = alt_font.getsize(alt)
  alt = wrap(alt, WRAP_WIDTH)
  alt_crop = alt_font_height * len(alt) + LINE_OFFSET * len(alt) + 10

  img_width, img_height = img.size
  img = img.crop((0, -1 * title_crop, img_width, img_height + alt_crop))
  img_width, img_height = img.size

  draw = ImageDraw.Draw(img)
  loffset_temp = LINE_OFFSET
  for line in title:
    w, h = draw.textsize(line, font = title_font)
    draw.text(((img_width-w)/2, loffset_temp), line, font = title_font, fill = 0xffffff)
    loffset_temp += h
  loffset_temp = LINE_OFFSET
  for line in alt:
    w, h = draw.textsize(line, font = alt_font)
    draw.text(((img_width-w)/2, (img_height - alt_crop - 5) + loffset_temp), line, font = alt_font, fill = 0xffffff)
    loffset_temp += h + 10

  img.save(DOWNLOAD_DIRECTORY+'/'+image)

def getComicRange(comic_string):
  comics = comic_string.split('-')
  if len(comics) == 1:
    try: return [int(comics[0])]
    except ValueError: return []
  elif len(comics) == 2:
    try: return [i for i in range(int(comics[0]), int(comics[1])+1)]
    except ValueError: return []
  return []

def fetchImage(comic_number):
  pass

def createImage(comic_number):
  global DOWNLOAD_DIRECTORY
  if DOWNLOAD_DIRECTORY[-1] == '/': DOWNLOAD_DIRECTORY = DOWNLOAD_DIRECTORY[:-1]
  if not os.path.exists(DOWNLOAD_DIRECTORY): os.makedirs(DOWNLOAD_DIRECTORY)

  info = fetchJSON(comic_number)
  image = str(info['num'])+'.png'

  with open(DOWNLOAD_DIRECTORY+'/'+image, 'wb') as image_file:
    image_file.write(urlopen(info['img']).read())

  formatImage(image, info['safe_title'], info['alt'])

def main():
  for i in getComicRange(argv[1]):
    print("Processing image {0}".format(i))
    createImage(i)

if __name__ == '__main__':
  main()
