from PIL import Image, ImageDraw, ImageFont
import storage as st


def convert_to_grayscale(image, text):
    img = Image.open(st.__UPLOADS__+image)
    insert_name(img, text[0])
    img = img.convert('L')
    img.save("grayscale/"+image)
    # img.show()


def insert_name(image, text):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('./fonts/DejaVuSansMono.ttf', size=17)

    # in format :- draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((0, 0), text, (255, 255, 255), font=font)
