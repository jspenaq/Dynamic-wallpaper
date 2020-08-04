import ctypes
import configparser
import os
from PIL import Image, ImageDraw, ImageFont
from math import ceil

SPI_SETDESKWALLPAPER = 20
user32 = ctypes.windll.user32
screen_w, screen_h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) # width, height

def read_config(filename = 'config.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    return config

def change_wallpaper(filename):
    return user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, filename, 0)

def draw_image(filename):
    img = Image.open(filename).convert("RGBA")
    w, h = img.size

    shape = [(w*.75, h*.80), (w, h*0.85)]
    print("shape:", shape)
    rect_w, rect_h = shape[1][0]-shape[0][0], shape[1][1]-shape[0][1]
    print(f"rect_w: {rect_w}, rect_h: {rect_h}")

    # img2 = Image.new('RGB', img.size, (255,255,255))
    # img2.putalpha(128)
    TINT_COLOR = (255, 255, 255)  # White
    TRANSPARENCY = .60  # Degree of transparency, 0-100%
    OPACITY = int(255 * TRANSPARENCY)

    overlay = Image.new('RGBA', img.size, TINT_COLOR+(0,))
    dr = ImageDraw.Draw(overlay)
    # dr.rectangle(shape, fill=(255, 255, 255, 204))
    dr.rectangle(shape, fill=TINT_COLOR+(OPACITY,))
    fontsize = 24 * h / screen_h
    print(f'fontsize: {ceil(fontsize)}')
    font = ImageFont.truetype("verdanab.ttf", int(fontsize))
    text = "12°C Clouds"
    text_w, text_h = dr.textsize(text, font=font)
    text_xy = (rect_w-text_w)/2 + shape[0][0], (rect_h-text_h*1.20)/2 + shape[0][1]
    print("text_xy:", text_xy)
    dr.text(text_xy, text, fill="#404040", font=font)
    # dr.text(shape[0], text, fill="#404040", font=font)

    new_filename = os.path.join(folder, "new_wallpaper.jpg")
    # https://stackoverflow.com/questions/43618910/pil-drawing-a-semi-transparent-square-overlay-on-image
    # https://stackoverflow.com/questions/41413956/pil-unable-to-change-the-transparency-level-for-jpeg-image
    # https://stackoverflow.com/questions/43730389/correctly-centring-text-pil-pillow
    
    # Alpha composite these two images together to obtain the desired result.
    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB") # Remove alpha for saving in jpg format.
    img.save(new_filename, quality=100)
    return new_filename

if __name__ == "__main__":
    config = read_config()
    folder = config['Settings']['folder']
    # image = 'Tokyo.jpg'
    image = 'wp4180977-3840x2160-wallpapers.jpg'
    filename = os.path.join(folder, image)
    print(filename)

    new_filename = draw_image(filename)    
    change_wallpaper(new_filename)
    