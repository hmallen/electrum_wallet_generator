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

bill_file = wallet_file + '_overlay.png'


def create_seed(seed, name):
    global seed_png_path
    
    seed_svg_path = name + '_seed.svg'
    logger.debug('Seed svg path: ' + seed_svg_path)

    seed_png_path = seed_svg_path.strip('.svg') + '.png'
    logger.debug('Seed png path: ' + seed_png_path)

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

        svg.write(seed_svg_path)

        with open(seed_svg_path, 'rb') as svg_file:
            svg2png(file_obj=svg_file, write_to=seed_png_path, parent_width=512, parent_height=512)

    except Exception as e:
        logger.exception('Exception while creating seed file.')
        logger.exception(e)
        raise


def create_qr(addr, name):
    global qr_png_path
    
    qr_svg_path = name + '_qr.svg'
    logger.debug('QR svg path: ' + qr_svg_path)

    qr_png_path = qr_svg_path.strip('.svg') + '.png'
    logger.debug('QR png path: ' + qr_png_path)

    try:
        # Error Correction Levels #
        # LOW / MEDIUM / QUARTILE / HIGH
        errcorlvl = QrCode.Ecc.QUARTILE

        qr_data = 'bitcoin:' + addr
        qr_pub = QrCode.encode_text(qr_data, errcorlvl)
        qr_svg_pub = qr_pub.to_svg_str(4)
        
        with open(qr_svg_path, 'w') as svg_file:
            svg_file.write(qr_svg_pub)

        with open(qr_svg_path, 'rb') as svg_file:
            svg2png(file_obj=svg_file, write_to=qr_png_path, parent_width=512, parent_height=512)

    except Exception as e:
        logger.exception('Exception while creating QR file.')
        logger.exception(e)
        raise


def draw_canvas():
    try:
        with Drawing() as draw:
            draw.fill_color = Color('transparent')
            draw.rectangle(left=0, top=0, width=bill_features['canvas'][0], height=bill_features['canvas'][1])
            
            with Image(width=bill_features['canvas'][0], height=bill_features['canvas'][1]) as img:
                draw.draw(img)
                img.save(filename=bill_file)

    except Exception as e:
        logger.exception('Exception while drawing canvas.')
        logger.exception(e)
        raise


def draw_address(addr, position):
    try:
        logger.debug('Address to draw: ' + addr)
        
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
            draw.text(left_coord, top_coord, addr)
            with Image(filename=bill_file) as img:
                img.rotate(90)
                draw.draw(img)
                img.rotate(270)
                img.save(filename=bill_file)

    except Exception as e:
        logger.exception('Exception while drawing address.')
        logger.exception(e)
        raise


def draw_qr(position):
    global qr_png_path

    try:
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
            with Image(filename=qr_png_path) as img:
                img.resize(195, 195)
                bill.composite(img, left=left_coord, top=top_coord)
                bill.save(filename=bill_file)

    except Exception as e:
        logger.exception('Exception while drawing qr.')
        logger.exception(e)
        raise


def draw_seed(position):
    global seed_png_path

    try:
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
            with Image(filename=seed_png_path) as img:
                img.resize(195, 195)
                bill.composite(img, left=left_coord, top=top_coord)
                bill.save(filename=bill_file)

    except Exception as e:
        logger.exception('Exception while drawing seed.')
        logger.exception(e)
        raise


def cleanup():
    directory_contents = os.listdir()
    logger.debug('Directory: ' + str(directory))

    for file in directory_contents:
        if file != bill_file:
            os.rename(file, ('tmp/' + file))


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

        draw_canvas()
        bill_positions = ['top', 'middle', 'bottom']
        for pos in bill_positions:
            draw_address(public_address, pos)
            draw_qr(pos)
            draw_seed(pos)

        logger.info('Cleaning up wallet directory.')
        cleanup()
    
    except Exception as e:
        logger.exception(e)
        sys.exit(1)