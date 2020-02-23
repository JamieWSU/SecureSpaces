from PIL import Image

left = 1
upper = 2
right = 10
lower = 13
name = "toCrop.jpg"

def cropImage(left, upper, right, lower, name):
    intruder = Image.open("temp/working/"+name)
    box = (left, upper, right, lower)
    intruder_crop = intruder.crop((left, upper, right, lower))
    intruder_crop.save("temp/"+name, quality=95)
cropImage(left, upper, upper, right, name)
