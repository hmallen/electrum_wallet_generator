import argparse
from cairosvg import svg2png
import configparser
from drawSVG.drawSVG import SVG
import glob
import json
import logging
import math
import os
from PyPDF2 import PdfFileMerger
from qrcodegen import QrCode, QrSegment
import sys
from wand.image import Image
from wand.display import display
from wand.drawing import Drawing
from wand.color import Color

demo_layout = 'resources/bill_feature_outlines.pdf'
config_file = 'layout_config.ini'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--demo', action='store_true', default=False, help='Print bill features onto bill template to demonstrate.')
parser.add_argument('-d', '--directory', type=str, help='Directory containing wallet file.')
parser.add_argument('-n', '--number', type=str, help='Wallet file number.')
parser.add_argument('-o', '--overlay', action='store_true', default=False, help='Enable creation of png overlays for bill printing.')
parser.add_argument('--pdf', action='store_true', default=False, help='Overlay output formatted as PDF instead of PNG.')
parser.add_argument('-m', '--merge', action='store_true', default=False, help='Skip wallet creation and merge existing PDFs into single file instead.')
args = parser.parse_args()

demo_mode = args.demo
wallet_dir = args.directory
wallet_file = args.number
create_overlay = args.overlay
output_pdf = args.pdf
merge_only = args.merge

if merge_only == False:
    if wallet_dir == None:
        logger.error('No wallet directory defined. Exiting.')
        sys.exit(1)
    elif wallet_file == None:
        logger.error('No wallet number defined. Exiting.')
        sys.exit(1)
    else:
        logger.info('Wallet directory: ' + wallet_dir)


def get_config():
    config = configparser.ConfigParser()
    config.read(config_file)

    # Coordinates of bill features
    features = {'canvas': config['canvas']['dim'], 'square_elements': config['square_elements']['dim'], 'font_size': config['font']['size'],
                     'addr_top': config['addr']['top'], 'addr_middle': config['addr']['middle'], 'addr_bottom': config['addr']['bottom'],
                     'qr_top': config['qr']['top'], 'qr_middle': config['qr']['middle'], 'qr_bottom': config['qr']['bottom'],
                     'seed_top': config['seed']['top'], 'seed_middle': config['seed']['middle'], 'seed_bottom': config['seed']['bottom']}
    """
    features = {'canvas': (1836, 2376), 'square_elements': (195, 195), 'font_size': 20,
                     'addr_top': (1784, 604), 'addr_middle': (1056, 604), 'addr_bottom': (330, 604),
                     'qr_top': (340, 261), 'qr_middle': (340, 989), 'qr_bottom': (340, 1715),
                     'seed_top': (1259, 470), 'seed_middle': (1259, 1199), 'seed_bottom': (1259, 1925)}
    """
    for key in features:
        if key != 'font_size':
            features[key] = tuple(features[key].strip('\(').strip('\)').split(', '))
    logger.debug('[Step #1]features: ' + str(features))
    for key in features:
        if key != 'font_size':
            features[key] = tuple([int(val) for val in features[key]])
        else:
            features[key] = int(features[key])
    logger.debug('[Step #2]features: ' + str(features))
    logger.debug('features[\'font_size\']: ' + str(features['font_size']))
    logger.debug('TYPE: ' + str(type(features['font_size'])))

    logger.debug('font_size: ' + str(features['font_size']))
    logger.debug(type(features['font_size']))

    return features


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
            img.resize(1836, 2376)
            img.save(filename=bill_file)

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


def merge_format_pdfs(path):
    try:
        os.chdir(path)
        contents = os.listdir()
        logger.debug('contents: ' + str(contents))

        os.mkdir('tmp/')

        pdf_files = []
        for file in contents:
            if file.endswith('.pdf'):
                pdf_files.append(file)
                logger.debug('file: ' + file)
        logger.debug('pdf_files: ' + str(pdf_files))

        if len(pdf_files) > 1:
            logger.info('Multiple PDF files found. Merging.')
            merger = PdfFileMerger()
            output_pdf = 'overlay.pdf'

            for doc in pdf_files:
                file = open(doc, 'rb')
                merger.append(fileobj=file)

            output = open(output_pdf, 'wb')
            merger.write(output)
            
            logger.info('Cleaning-up pdf directory.')
            for doc in pdf_files:
                os.rename(doc, ('tmp/' + doc))
        
        else:
            logger.info('Multiple PDF files not found. Renaming overlay and skipping merge.')
            os.rename('overlay_1.pdf', 'overlay.pdf')

    except Exception as e:
        logger.exception('Exception while merging PDF files.')
        logger.exception(e)
        raise


if __name__ == '__main__':
    try:
        bill_features = get_config()

        if merge_only == False:
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
                    if demo_mode == False:
                        draw_canvas()
                    else:
                        import_bill_layout(demo_layout)
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

        else:
            logger.info('Merging PDF files, if multiple present.')
            merge_format_pdfs(wallet_dir)
        
    
    except Exception as e:
        logger.exception(e)
        sys.exit(1)
