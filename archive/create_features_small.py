import argparse
from cairosvg import svg2png
from drawSVG.drawSVG import SVG
import glob
import json
import logging
import math
import os
from qrcodegen import QrCode, QrSegment
import sys
from wand.image import Image
from wand.display import display
from wand.drawing import Drawing
from wand.color import Color

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', type=str, help='Directory containing wallet file.')
parser.add_argument('-n', '--number', type=str, help='Wallet file number.')
parser.add_argument('-o', '--overlay', action='store_true', default=False, help='Enable creation of png overlays for bill printing.')
parser.add_argument('--pdf', action='store_true', default=False, help='Overlay output formatted as PDF instead of PNG.')
args = parser.parse_args()

wallet_dir = args.directory
wallet_file = args.number
create_overlay = args.overlay
output_pdf = args.pdf

if wallet_dir == None:
    logger.error('No wallet directory defined. Exiting.')
    sys.exit(1)
elif wallet_file == None:
    logger.error('No wallet number defined. Exiting.')
    sys.exit(1)
else:
    logger.info('Wallet directory: ' + wallet_dir)

# Coordinates of bill features
"""
bill_features = {'canvas': (1836, 2376), 'square_elements': (195, 195), 'font_size': 20,
                 'addr_top': (1784, 604), 'addr_middle': (1056, 604), 'addr_bottom': (330, 604),
                 'qr_top': (338, 262), 'qr_middle': (338, 991), 'qr_bottom': (338, 1718),
                 'seed_top': (1257, 471), 'seed_middle': (1257, 1200), 'seed_bottom': (1257, 1926)}
"""
bill_features = {'canvas': (612, 792), 'square_elements': (65, 65), 'font_size': 7,
                 'addr_top': (595, 201), 'addr_middle': (352, 201), 'addr_bottom': (110, 201),
                 'qr_top': (114, 87), 'qr_middle': (114, 329), 'qr_bottom': (114, 571),
                 'seed_top': (420, 157), 'seed_middle': (420, 400), 'seed_bottom': (420, 642)}


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
            svg2png(file_obj=svg_file, write_to=seed_png_path, parent_width=1024, parent_height=1024)

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


def import_bill_layout(path):
    try:
        with Image(filename=path) as img:
            #img.resize
            pass

    except Exception as e:
        logger.exception('Exception while importing bill layout.')
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
            draw.font_size = bill_features['font_size']
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
                img.resize(bill_features['square_elements'][0], bill_features['square_elements'][1])
                bill.composite(img, left=left_coord, top=top_coord)
                bill.save(filename=bill_file)

    except Exception as e:
        logger.exception('Exception while drawing QR.')
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
                img.resize(bill_features['square_elements'][0], bill_features['square_elements'][1])
                bill.composite(img, left=left_coord, top=top_coord)
                bill.save(filename=bill_file)

    except Exception as e:
        logger.exception('Exception while drawing seed.')
        logger.exception(e)
        raise


def cleanup():
    directory_contents = os.listdir()

    os.mkdir('tmp/')
    for file in directory_contents:
        if file != bill_file:
            os.rename(file, ('tmp/' + file))


if __name__ == '__main__':
    try:
        os.chdir(wallet_dir)

        # Determine overlay number and file name based on wallet number
        overlay_num = str(math.ceil(int(wallet_file) / 3))
        logger.debug('overlay_num: ' + overlay_num)

        # Set file suffix based on desired output
        if output_pdf == True:
            bill_file = '../overlay_' + overlay_num + '.pdf'
        else:
            bill_file = '../overlay_' + overlay_num + '.png'
        logger.debug('bill_file: ' + bill_file)

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

        logger.info('Creating bill feature elements.')
        create_seed(seed, wallet_file)
        create_qr(public_address, wallet_file)

        if create_overlay == True:
            logger.info('Creating bill printing overlay.')
            if os.path.isfile(bill_file) == False:
                logger.info('Creating new canvas.')
                draw_canvas()
                #import_bill_layout()
            else:
                logger.info('Using existing canvas.')

            pos_modulo = int(wallet_file) % 3
            logger.debug('pos_modulo: ' + str(pos_modulo))
            # pos_modulo = 1 --> Top bill
            # pos_modulo = 2 --> Middle bill
            # pos_modulo = 3 --> Bottom bill
            
            bill_positions = ['top', 'middle', 'bottom']
            logger.debug('bill_positions[pos_modulo]: ' + bill_positions[pos_modulo])
            
            draw_address(public_address, bill_positions[pos_modulo])
            draw_qr(bill_positions[pos_modulo])
            draw_seed(bill_positions[pos_modulo])

        #logger.info('Cleaning up wallet directory.')
        #cleanup()
    
    except Exception as e:
        logger.exception(e)
        sys.exit(1)
