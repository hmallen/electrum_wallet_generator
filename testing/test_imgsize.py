import logging
from wand.image import Image

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

test_image = 'test_layout.pdf'

if __name__ == '__main__':
    with Image(filename=test_image) as img:
        #logger.info('img: ' + img)
        logger.info('img.width: ' + str(img.width))
        logger.info('img.height: ' + str(img.height))
