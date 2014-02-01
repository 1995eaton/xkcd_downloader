from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlopen
from random import randrange
from textwrap import wrap
from sys import argv
import os

class XKCD_downloader:

  def __init__(self,
               DOWNLOAD_DIRECTORY = "images",
               TITLE_FONTSIZE = 28,
               ALT_FONTSIZE = 18,
               LINE_OFFSET = 10):

    self.download_directory = DOWNLOAD_DIRECTORY
    self.title_fontsize = TITLE_FONTSIZE
    self.alt_fontsize = ALT_FONTSIZE
    self.line_offset = LINE_OFFSET

  def fetchJSON(self, comic_number):
    from json import loads
    xkcd_json_url = "http://xkcd.com/info.0.json"
    try:
      if comic_number < 0:
        return ""
      elif comic_number == 0:
        xkcd_json = loads(urlopen(xkcd_json_url).read().decode('utf-8'))
      else:
        xkcd_json = loads(urlopen("http://xkcd.com/{0}/info.0.json".format(str(comic_number))).read().decode('utf-8'))
    except:
      return
    return xkcd_json

  def formatImage(self, image, title, alt, tfont = 'title.ttf', afont = 'alt.ttf'):

    try:
      img = Image.open(image)
    except OSError:
      return
    wrap_width = int(img.size[0] * 0.183+0.001*1/2 * 5/self.alt_fontsize)

    # Font sizing is a pain in the ass

    title_font = ImageFont.truetype(tfont, self.title_fontsize)
    title_font_width, title_font_height = title_font.getsize(title)
    title = wrap(title, int(img.size[0] * 0.09+0.001*1/2))

    if not title or title[0] == '...' and len(title) == 1: title_crop = 0
    else: title_crop = title_font_height + self.line_offset * (len(title) * 2) + 15

    alt_font = ImageFont.truetype(afont, self.alt_fontsize)
    alt_font_width, alt_font_height = alt_font.getsize(alt)
    alt = wrap(alt, wrap_width - 15)

    if not alt or alt[0] == '...' and len(alt) == 1: alt_crop = 0
    else: alt_crop = alt_font_height * len(alt) + self.line_offset * len(alt) + 15

    img_width, img_height = img.size
    img = img.crop((0, -1 * title_crop, img_width, img_height + alt_crop))
    img_width, img_height = img.size

    draw = ImageDraw.Draw(img)
    loffset_temp = self.line_offset
    for line in title:
      w, h = draw.textsize(line, font = title_font)
      draw.text(((img_width-w)/2, loffset_temp), line, font = title_font, fill = 0xffffff)
      loffset_temp += h
    loffset_temp = self.line_offset
    for line in alt:
      w, h = draw.textsize(line, font = alt_font)
      draw.text(((img_width-w)/2, (img_height - alt_crop - 5) + loffset_temp), line, font = alt_font, fill = 0xffffff)
      loffset_temp += h + 10

    img.save(image)

  def getComicRange(self, comic_string):
    comics = str(comic_string).split('-')
    if len(comics) == 1:
      try: return [int(comics[0])]
      except ValueError: return []
    elif len(comics) == 2:
      try: return [i for i in range(int(comics[0]), int(comics[1])+1)]
      except ValueError: return []
    return []

  def checkPath(self):
    if self.download_directory[-1] == '/':
      self.download_directory = self.download_directory[:-1]
    if not os.path.exists(self.download_directory):
      os.makedirs(self.download_directory)

  def fetchImages(self, comic_number, data_type):
    self.checkPath()
    images = []
    for i in self.getComicRange(comic_number):
      if i == 404:
        continue
      if i == 0:
        print("Fetching comic -> Latest".format(i))
      else:
        print("Fetching comic -> {0}".format(i))
      info = self.fetchJSON(i)
      if not info:
        print("Error: URL could not be reached!")
        continue
      title, alt, num = info['safe_title'], info['alt'], str(info['num'])
      image = '{0}.png'.format(num)
      with open(self.download_directory+'/'+image, 'wb') as image_file:
        image_file.write(urlopen(info['img']).read())
        if data_type == 'create':
          print("Processing comic -> {0}".format(i))
          self.formatImage(self.download_directory+'/'+image, title, alt)

  def getAll(self, data_type):
    all_comics = '1-{0}'.format(self.fetchJSON(0)['num'])
    if data_type == 'images':
      self.fetchImages(all_comics, 'images')
    elif data_type == 'create':
      self.fetchImages(all_comics, 'create')

  def getRandom(self, data_type, iterations = 1):
    info = self.fetchJSON(0)
    if not info:
      print("Error URL could not be reached!")
      return
    comic_count = info['num']
    for i in range(iterations):
      r = randrange(1, comic_count + 1)
      if data_type == 'images':
        self.fetchImages(r, 'images')
      elif data_type == 'create':
        self.fetchImages(r, 'create')

def main():
  x = XKCD_downloader()
  a = argv[1:]

  if '-random' in a:
    if len(a) == 1:
      x.getRandom('create', 1)
    elif len(a) == 2:
      if '-download-only' in a:
        x.getRandom('images', 1)
      else:
        try: x.getRandom('create', int(a[a.index('-random')+1]))
        except (ValueError, IndexError): pass
    elif '-download-only' in a:
      try: x.getRandom('images', int(a[a.index('-random')+1]))
      except (ValueError, IndexError): pass

  elif '-fetch-all' in a:
    if '-download-only' in a:
      x.getAll('images')
    else:
      x.getAll('create')

  elif '-download-only' in a:
    for i in a:
      if i != '-download-only':
        x.fetchImages(i, 'images')

  else:
    for i in a:
      x.fetchImages(i, 'create')

if __name__ == '__main__':
  main()
