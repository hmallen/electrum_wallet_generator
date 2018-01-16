import argparse
from cairosvg import svg2png
from drawSVG.drawSVG import SVG
import glob
import json
import logging
import os
from qrcodegen import QrCode, QrSegment
import sys
from wand.image import Image
from wand.display import display
from wand.drawing import Drawing
from wand.color import Color

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

# Coordinates of bill features
bill_features = {'canvas': (1836, 2376),
                 'addr_top': (1784, 604), 'addr_middle': (1056, 604), 'addr_bottom': (330, 604),
                 'qr_top': (338, 262), 'qr_middle': (338, 991), 'qr_bottom': (338, 1718),
                 'seed_top': (1257, 471), 'seed_middle': (1257, 1200), 'seed_bottom': (1257, 1926)}

##################################################
#bill_file = 'bill.png'  # NEED TO FIX THIS
#qr_file = 'wallet/qr.png'   # NEED TO FIX THIS
#seed_file = 'wallet/seed.png'   # NEED TO FIX THIS
##################################################


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

        with open(seed_file_path, 'w') as svg_file:
            svg_file.write(seed_file_path)
        
        svg2png(file_obj=open(seed_file_path, 'rb'),
                write_to=(seed_file_path.strip('.svg') + '.png'),
                parent_width=512, parent_height=512)

    except Exception as e:
        logger.exception('Exception while creating seed file.')
        logger.exception(e)
        raise


def create_qr(addr, name):
    qr_file_path = name + '_qr.svg'
    logger.debug('QR file path: ' + qr_file_path)

    try:
        # Error Correction Levels #
        # LOW / MEDIUM / QUARTILE / HIGH
        errcorlvl = QrCode.Ecc.QUARTILE

        qr_data = 'bitcoin:' + addr
        qr_pub = QrCode.encode_text(qr_data, errcorlvl)
        qr_svg_pub = qr_pub.to_svg_str(4)
        
        with open(qr_file_path, 'w') as svg_file:
            svg_file.write(qr_svg_pub)

        svg2png(file_obj=open(qr_file_path, 'rb'),
                write_to=(qr_file_path.strip('.svg') + '.png'),
                parent_width=512, parent_height=512)

    except Exception as e:
        logger.exception('Exception while creating QR file.')
        logger.exception(e)
        raise


def draw_canvas():
    with Drawing() as draw:
        draw.fill_color = Color('transparent')
        draw.rectangle(left=0, top=0, width=bill_features['canvas'][0], height=bill_features['canvas'][1])
        
        with Image(width=bill_features['canvas'][0], height=bill_features['canvas'][1]) as img:
            draw.draw(img)
            img.save(filename=bill_file)


def draw_address(position):
    if position == 'top':
        left_coord = bill_features['addr_top'][0]
        top_coord = bill_features['addr_top'][1]
    elif position == 'middle':
        left_coord = bill_features['addr_middle'][0]
        top_coord = bill_features['addr_middle'][1]
    elif position == 'bottom':
        left_coord = bill_features['addr_bottom'][0]
        top_coord = bill_features['addr_bottom'][1]
    
    with Drawing() as draw:
        draw.font_family = 'Ubuntu'
        draw.font_size = 20
        draw.text(left_coord, top_coord, test_addr)
        with Image(filename=bill_file) as img:
            img.rotate(90)
            draw.draw(img)
            img.rotate(270)
            img.save(filename=bill_file)


def draw_qr(position):
    if position == 'top':
        left_coord = bill_features['qr_top'][0]
        top_coord = bill_features['qr_top'][1]
    elif position == 'middle':
        left_coord = bill_features['qr_middle'][0]
        top_coord = bill_features['qr_middle'][1]
    elif position == 'bottom':
        left_coord = bill_features['qr_bottom'][0]
        top_coord = bill_features['qr_bottom'][1]
    
    with Image(filename=bill_file) as bill:
        with Image(filename=qr_file) as img:
            img.resize(195, 195)
            bill.composite(img, left=left_coord, top=top_coord)
            bill.save(filename=bill_file)


def draw_seed(position):
    if position == 'top':
        left_coord = bill_features['seed_top'][0]
        top_coord = bill_features['seed_top'][1]
    elif position == 'middle':
        left_coord = bill_features['seed_middle'][0]
        top_coord = bill_features['seed_middle'][1]
    elif position == 'bottom':
        left_coord = bill_features['seed_bottom'][0]
        top_coord = bill_features['seed_bottom'][1]
    
    with Image(filename=bill_file) as bill:
        with Image(filename=seed_file) as img:
            img.resize(195, 195)
            bill.composite(img, left=left_coord, top=top_coord)
            bill.save(filename=bill_file)


if __name__ == '__main__':
    try:
        os.chdir(wallet_dir)

        with open(wallet_file, 'r') as file:
            wallet_info_raw = file.read()
        wallet_info = json.loads(wallet_info_raw)

        seed = wallet_info['keystore']['seed']
        logger.info('Seed: ' + seed)
        seed_text_file = wallet_file + '_seed.txt'
        with open(seed_text_file, 'w') as file:
            file.write(seed)

        public_address = wallet_info['addresses']['receiving'][0]
        logger.info('Public address: ' + public_address)
        address_text_file = wallet_file + '_addr.txt'
        with open(address_text_file, 'w') as file:
            file.write(public_address)

        logger.info('Creating bill feature overlay.')
        create_seed(seed, wallet_file)
        create_qr(public_address, wallet_file)
    
    except Exception as e:
        logger.exception(e)
        sys.exit(1)
