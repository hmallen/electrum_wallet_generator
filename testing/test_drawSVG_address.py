from cairosvg import svg2png
from drawSVG.drawSVG import SVG
import logging
from PIL import Image
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_addr(addr):
    addr_file_path = 'test_addr.svg'
    logger.debug('Address file path: ' + addr_file_path)
    png_file_path = 'test_addr.png'
    logger.debug('PNG file path (original): ' + png_file_path)
    png_file_rotated_path = 'test_addr_rotated.png'
    logger.debug('PNG file path (rotated): ' + png_file_rotated_path)

    try:
        svg = SVG({'width':700, 'height':32})

        svg.addChildElement('text',
                            {'x':0, 'y':13,
                             'font-family':'Ubuntu',
                             'font-size':30,
                             'text-anchor':'start',
                             'alignment-baseline':'central'},
                            addr)

        svg.write(addr_file_path)

        svg2png(file_obj=open(addr_file_path, 'rb'), write_to=png_file_path)

        img_orig = Image.open(png_file_path)
        img_rotated = img_orig.rotate(90, expand=True)
        img_rotated.save(png_file_rotated_path)

    except Exception as e:
        logger.exception('Exception while creating address file.')
        logger.exception(e)
        raise


if __name__ == '__main__':
    try:
        address = '1NysEmArgZAQsSmNDQIIGXJ8ggyyCbCqoj'
        create_addr(address)

    except KeyboardInterrupt:
        logger.info('Exit signal received.')
        sys.exit()

    except Exception as e:
        logger.exception(e)
        sys.exit(1)
