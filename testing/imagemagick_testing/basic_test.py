import os
from PIL import Image
from wand.image import Image
from wand.display import display

test_file = 'test_file/test.png'

if os.path.isfile(test_file):
    os.remove(test_file)

with Image(width=200, height=100) as img:
    img.save(filename=test_file)
