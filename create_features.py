import argparse
from cairosvg import svg2png
from drawSVG.drawSVG import SVG
import glob
import json
import logging
import os
from qrcodegen import QrCode, QrSegment
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', type=str, help='Directory containing wallet file.')
parser.add_argument('-n', '--number', type=str, help='Wallet file number.')
parser.add_argument('-c', '--convert', action='store_true', default=False, help='Convert resulting svg file to png.')
args = parser.parse_args()

wallet_dir = args.directory
wallet_file = args.number
convert_svg = args.convert

if wallet_dir == None:
    logger.error('No wallet directory defined. Exiting.')
    sys.exit(1)
elif wallet_file == None:
    logger.error('No wallet number defined. Exiting.')
    sys.exit(1)
else:
    logger.info('Wallet directory: ' + wallet_dir)


def create_seed(seed, name):
    seed_file_path = wallet_dir + name + '_seed.svg'
    logger.debug('Seed file path: ' + seed_file_path)

    try:
        svg = SVG({'width':5800, 'height':5800})

        svg.addChildElement('rect',
                            {'x':0, 'y':0,
                             'fill':'none',
                             'stroke':'black',
                             'stroke-width':0.5})

        seed_words = seed.split(' ')

        seed_lines = []
        for x in range(0, 12, 2):
            word_num = x + 1
            #line = str(word_num) + ') ' + seed_words[x] + ' ' + str(word_num + 1) + ') ' + seed_words[x + 1]
            line = seed_words[x] + ' ' + seed_words[x + 1]
            seed_lines.append(line)

        position = 650
        for x in range(0, 6):
            svg.addChildElement('text',
                                {'x':2900, 'y':position,
                                 'font-family':'Ubuntu',
                                 'font-size':600,
                                 'text-anchor':'middle',
                                 'dominant-baseline':'central'},
                                seed_lines[x])
            position += 900

        svg.write(seed_file_path)

    except Exception as e:
        logger.exception('Exception while creating seed file.')
        logger.exception(e)
        raise


def create_addr(addr, name):
    addr_file_path = wallet_dir + name + '_addr.svg'
    logger.debug('Address file path: ' + addr_file_path)

    try:
        logger.debug('---- NOT YET IMPLEMENTED ----')

    except Exception as e:
        logger.exception('Exception while creating address file.')
        logger.exception(e)
        raise


def create_qr(addr, name):
    qr_file_path = wallet_dir + name + '_qr.svg'
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


def convert_svg_png(directory):
    logger.debug('Conversion directory: ' + directory)

    try:
        dir_list = os.listdir(directory)

        svg_files = []
        for file in dir_list:
            if file.endswith('.svg'):
                svg_files.append(file)

        logger.debug('SVG files: ' + str(svg_files))

        for file in svg_files:
            svg_path = directory + file
            logger.debug('SVG path: ' + svg_path)
            png_path = directory + file.strip('.svg') + '.png'
            logger.debug('PNG path: ' + png_path)

            svg2png(file_obj=open(svg_path, 'rb'), write_to=png_path, parent_width=512, parent_height=512)

    except Exception as e:
        logger.exception('Exception while converting svg files to png.')
        logger.exception(e)
        raise
        

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

        os.chdir('../../..')

        create_seed(seed, wallet_file)
        create_addr(public_address, wallet_file)
        create_qr(public_address, wallet_file)
        if convert_svg == True:
            convert_svg_png(wallet_dir)
    
    except Exception as e:
        logger.exception(e)
        sys.exit(1)
