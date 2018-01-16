import argparse
from cairosvg import svg2png
from drawSVG.drawSVG import SVG
import glob
import json
import logging
import os
from PIL import Image
from qrcodegen import QrCode, QrSegment
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', type=str, help='Directory containing wallet file.')
parser.add_argument('-n', '--number', type=str, help='Wallet file number.')
args = parser.parse_args()

wallet_dir = args.directory
wallet_file = args.number

if wallet_dir == None:
    logger.error('No wallet directory defined. Exiting.')
    sys.exit(1)
elif wallet_file == None:
    logger.error('No wallet number defined. Exiting.')
    sys.exit(1)
else:
    logger.info('Wallet directory: ' + wallet_dir)


def create_seed(seed, name):
    seed_file_path = name + '_seed.svg'
    logger.debug('Seed file path: ' + seed_file_path)

    try:
        svg = SVG({'width':5700, 'height':5700})

        svg.addChildElement('rect',
                            {'x':0, 'y':0,
                             'fill':'none',
                             'stroke':'black',
                             'stroke-width':0.5})

        seed_words = seed.split(' ')

        seed_lines = []
        for x in range(0, 12, 2):
            word_num = x + 1
            line = seed_words[x] + ' ' + seed_words[x + 1]
            seed_lines.append(line)

        position = 750
        for x in range(0, 6):
            svg.addChildElement('text',
                                {'x':2850, 'y':position,
                                 'font-family':'Ubuntu',
                                 'font-size':600,
                                 'text-anchor':'middle'},
                                seed_lines[x])
            position += 900

        svg.write(seed_file_path)

    except Exception as e:
        logger.exception('Exception while creating seed file.')
        logger.exception(e)
        raise


def create_addr(addr, name):
    addr_file_path = name + '_addr.svg'
    logger.debug('Address SVG file path: ' + addr_file_path)
    png_file_path = name + '_addr.png'
    logger.debug('Address PNG file path: ' + png_file_path)

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

    except Exception as e:
        logger.exception('Exception while creating address file.')
        logger.exception(e)
        raise


def create_qr(addr, name):
    qr_file_path = name + '_qr.svg'
    logger.debug('QR file path: ' + qr_file_path)

    try:
        # Error Correction Levels #
        # LOW / MEDIUM / QUARTILE / HIGH
        errcorlvl = QrCode.Ecc.QUARTILE # Error correction level. Need to determine best setting!

        qr_data = 'bitcoin:' + addr
        qr_pub = QrCode.encode_text(qr_data, errcorlvl)
        qr_svg_pub = qr_pub.to_svg_str(4)
        
        with open(qr_file_path, 'w') as svg_file:
            svg_file.write(qr_svg_pub)

    except Exception as e:
        logger.exception('Exception while creating QR file.')
        logger.exception(e)
        raise


def convert_svg_png(directory='./'):
    dir_change = False
    if directory != './':
        os.chdir(directory)
        dir_change = True
    
    logger.debug('Conversion directory: ' + directory)

    try:
        dir_list = os.listdir()

        svg_files = []
        for file in dir_list:
            if file.endswith('.svg'):
                svg_files.append(file)
        logger.debug('SVG files: ' + str(svg_files))

        png_files = []
        for file in svg_files:
            svg_path = directory + file
            logger.debug('SVG path: ' + svg_path)
            png_path = directory + file.strip('.svg') + '.png'
            logger.debug('PNG path: ' + png_path)
            png_files.append(png_path)

            svg2png(file_obj=open(svg_path, 'rb'), write_to=png_path, parent_width=512, parent_height=512)
        
        for file in png_files:
            if file.endswith('_addr.png'):
                addr_path = file
            elif file.endswith('_qr.png'):
                qr_path = file
            elif file.endswith('_seed.png'):
                seed_path = file

        converted = {'addr':addr_path, 'qr':qr_path, 'seed':seed_path}

        if dir_change == True:
            os.chdir(wallet_dir)

        return converted

    except Exception as e:
        logger.exception('Exception while converting svg files to png.')
        logger.exception(e)
        raise


def rotate_png(path):
    img_orig = Image.open(path)
    img_rotated = img_orig.rotate(90, expand=True)
    os.remove(path)
    img_rotated.save(path)


def cleanup_directory(directory='./'):
    if directory != './':
        os.chdir(directory)
    
    os.mkdir('tmp')

    for file in os.listdir():
        if not file.endswith('.png') and file != 'tmp':
            new_path = 'tmp/' + file
            logger.debug('New path: ' + new_path)
            os.rename(file, new_path)
            logger.debug('Moved to tmp/: ' + file)


if __name__ == '__main__':
    try:
        os.chdir(wallet_dir)

        with open(wallet_file, 'r') as file:
            wallet_info_raw = file.read()

        wallet_info = json.loads(wallet_info_raw)

        seed = wallet_info['keystore']['seed']
        logger.info('Seed: ' + seed)

        seed_file = wallet_file + '_seed.txt'
        with open(seed_file, 'w') as file:
            file.write(seed)

        public_address = wallet_info['addresses']['receiving'][0]
        logger.info('Public address: ' + public_address)

        address_file = wallet_file + '_addr.txt'
        with open(address_file, 'w') as file:
            file.write(public_address)

        logger.info('Creating bill features.')
        create_seed(seed, wallet_file)
        create_addr(public_address, wallet_file)
        create_qr(public_address, wallet_file)

        logger.info('Converting svg files to png.')
        converted_files = convert_svg_png()
        logger.debug('Converted files: ' + str(converted_files))

        logger.info('Rotating public address png image.')
        rotate_png(converted_files['addr'])

        logger.info('Cleaning-up working directory.')
        cleanup_directory()
    
    except Exception as e:
        logger.exception(e)
        sys.exit(1)
