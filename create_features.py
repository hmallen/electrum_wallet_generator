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

demo_layout_bill = '../../../resources/bill_feature_outlines.pdf'
demo_layout_address = '../../../resources/address_info_card_new.pdf'

bill_config_file = 'config/bill.ini'
address_config_file = 'config/address.ini'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--demo', action='store_true', default=False, help='Print bill features onto bill template to demonstrate.')
parser.add_argument('-d', '--directory', type=str, help='Directory containing wallet file.')
parser.add_argument('-n', '--number', type=str, help='Wallet file number.')
parser.add_argument('-o', '--overlay', action='store_true', default=False, help='Enable creation of png overlays for bill printing.')
parser.add_argument('--pdf', action='store_true', default=False, help='Overlay output formatted as PDF instead of PNG.')
parser.add_argument('-s', '--serial', type=str, default='', help='Serial number to print on overlays for reference.')
parser.add_argument('-m', '--merge', action='store_true', default=False, help='Skip wallet creation and merge existing PDFs into single file instead.')
args = parser.parse_args()

demo_mode = args.demo
wallet_dir = args.directory
wallet_file = args.number
create_overlay = args.overlay
output_pdf = args.pdf
serial_number = args.serial
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


def get_config(config_type, config_element=None):
    config = configparser.ConfigParser()

    if config_type == 'bill':
        config.read(bill_config_file)

        # Coordinates of bill features
        features = {'canvas': config['canvas']['dim'],
                    'square_elements': config['square_elements']['dim'],
                    'font_size': config['font']['size'],
                    'addr_top': config['addr']['top'],
                    'addr_middle': config['addr']['middle'],
                    'addr_bottom': config['addr']['bottom'],
                    'qr_top': config['qr']['top'],
                    'qr_middle': config['qr']['middle'],
                    'qr_bottom': config['qr']['bottom'],
                    'seed_top': config['seed']['top'],
                    'seed_middle': config['seed']['middle'],
                    'seed_bottom': config['seed']['bottom'],
                    'label_top': config['label']['top'],
                    'label_middle': config['label']['middle'],
                    'label_bottom': config['label']['bottom']}

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

    elif config_type == 'address':
        config.read(address_config_file)

        if config_element == 'qr':
            features = {'canvas': config['canvas']['dim'],
                        'square_elements': config['square_elements']['dim'],
                        'left_x': config[config_element]['left_x'],
                        'right_x': config[config_element]['right_x'],
                        'row_one_y': config[config_element]['row_one_y'],
                        'row_two_y': config[config_element]['row_two_y'],
                        'row_three_y': config[config_element]['row_three_y'],
                        'row_four_y': config[config_element]['row_four_y'],
                        'font_size': config[config_element]['font_size']}

        elif config_element == 'addr':
            features = {'canvas': config['canvas']['dim'],
                        'square_elements': config['square_elements']['dim'],
                        'top_y': config[config_element]['top_y'],
                        'bottom_y': config[config_element]['bottom_y'],
                        'column_one_x': config[config_element]['column_one_x'],
                        'column_two_x': config[config_element]['column_two_x'],
                        'column_three_x': config[config_element]['column_three_x'],
                        'column_four_x': config[config_element]['column_four_x'],
                        'font_size': config[config_element]['font_size']}

        elif config_element == 'label':
            features = {'canvas': config['canvas']['dim'],
                        'square_elements': config['square_elements']['dim'],
                        'left_x': config[config_element]['left_x'],
                        'right_x': config[config_element]['right_x'],
                        'row_one_y': config[config_element]['row_one_y'],
                        'row_two_y': config[config_element]['row_two_y'],
                        'row_three_y': config[config_element]['row_three_y'],
                        'row_four_y': config[config_element]['row_four_y'],
                        'font_size': config[config_element]['font_size']}
        
        for key in features:
            if key == 'canvas' or key == 'square_elements':
                features[key] = tuple(features[key].strip('\(').strip('\)').split(', '))
        logger.debug('[Step #1]features: ' + str(features))
        for key in features:
            if key == 'canvas' or key == 'square_elements':
                features[key] = tuple([int(val) for val in features[key]])
            else:
                features[key] = int(features[key])
        logger.debug('[Step #2]features: ' + str(features))

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
            svg2png(file_obj=svg_file, write_to=qr_png_path, parent_width=1024, parent_height=1024)

    except Exception as e:
        logger.exception('Exception while creating QR file.')
        logger.exception(e)
        raise


def draw_canvas(canvas_type):
    try:
        if canvas_type == 'bill':
            with Drawing() as draw:
                draw.fill_color = Color('transparent')
                draw.rectangle(left=0, top=0, width=bill_features['canvas'][0], height=bill_features['canvas'][1])
                
                with Image(width=bill_features['canvas'][0], height=bill_features['canvas'][1]) as img:
                    draw.draw(img)
                    img.save(filename=bill_file)

        elif canvas_type == 'address':
            with Drawing() as draw:
                draw.fill_color = Color('transparent')
                draw.rectangle(left=0, top=0, width=addr_features_qr['canvas'][0], height=addr_features_qr['canvas'][1])
                
                with Image(width=addr_features_qr['canvas'][0], height=addr_features_qr['canvas'][1]) as img:
                    draw.draw(img)
                    img.save(filename=addr_file)
            """
            with Image(filename=demo_layout_address) as img:
                img.resize(1836, 2376)
                #display(img)
                img.save(filename=addr_file)
            """

    except Exception as e:
        logger.exception('Exception while drawing canvas.')
        logger.exception(e)
        raise


def import_demo_layout(demo_type):
    try:
        if demo_type == 'bill':
            demo_layout = demo_layout_bill
            demo_file = bill_file
        elif demo_type == 'address':
            demo_layout = demo_layout_address
            demo_file = addr_file
    
        with Image(filename=demo_layout) as img:
            img.resize(1836, 2376)
            #display(img)
            img.save(filename=demo_file)

    except Exception as e:
        logger.exception('Exception while importing demo layout.')
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
        logger.exception('Exception while drawing public address on bill overlay.')
        logger.exception(e)
        raise


def draw_qr(position):
    global qr_png_path
    logger.debug('[draw_qr()]-qr_png_path: ' + qr_png_path)

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
        logger.exception('Exception while drawing QR on bill overlay.')
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
        logger.exception('Exception while drawing seed on bill overlay.')
        logger.exception(e)
        raise


def draw_label(position, text):
    logger.info('Adding label to bill overlay.')

    try:
        if position == 'top':
            x_label = bill_features['label_top'][0]
            y_label = bill_features['label_top'][1]
        elif position == 'middle':
            x_label = bill_features['label_middle'][0]
            y_label = bill_features['label_middle'][1]
        elif position == 'bottom':
            x_label = bill_features['label_bottom'][0]
            y_label = bill_features['label_bottom'][1]
            
        with Drawing() as draw:
            draw.font_family = 'Ubuntu'
            draw.font_style = 'oblique'
            draw.font_size = bill_features['font_size']
            draw.text_alignment = 'left'
            draw.text(x_label, y_label, text)
            with Image(filename=bill_file) as layout:
                draw.draw(layout)
                layout.save(filename=bill_file)

    except Exception as e:
        logger.exception('Exception while drawing label on bill overlay.')
        logger.exception(e)
        raise


def draw_address_layout(position, element, text=None):
    global qr_png_path
    logger.debug('[draw_address_layout()]-qr_png_path: ' + qr_png_path)

    try:
        # 8 positions available on print layout
        # Position argument is an integer from 1-8
        if position == 1:
            x_qr = addr_features_qr['left_x']
            y_qr = addr_features_qr['row_one_y']
            
            x_addr = addr_features_addr['column_four_x']
            y_addr = addr_features_addr['top_y']

            x_label = addr_features_label['left_x']
            y_label = addr_features_label['row_one_y']
            
        elif position == 2:
            x_qr = addr_features_qr['right_x']
            y_qr = addr_features_qr['row_one_y']

            x_addr = addr_features_addr['column_four_x']
            y_addr = addr_features_addr['bottom_y']

            x_label = addr_features_label['right_x']
            y_label = addr_features_label['row_one_y']
            
        elif position == 3:
            x_qr = addr_features_qr['left_x']
            y_qr = addr_features_qr['row_two_y']

            x_addr = addr_features_addr['column_three_x']
            y_addr = addr_features_addr['top_y']

            x_label = addr_features_label['left_x']
            y_label = addr_features_label['row_two_y']
            
        elif position == 4:
            x_qr = addr_features_qr['right_x']
            y_qr = addr_features_qr['row_two_y']

            x_addr = addr_features_addr['column_three_x']
            y_addr = addr_features_addr['bottom_y']

            x_label = addr_features_label['right_x']
            y_label = addr_features_label['row_two_y']
            
        elif position == 5:
            x_qr = addr_features_qr['left_x']
            y_qr = addr_features_qr['row_three_y']

            x_addr = addr_features_addr['column_two_x']
            y_addr = addr_features_addr['top_y']

            x_label = addr_features_label['left_x']
            y_label = addr_features_label['row_three_y']
            
        elif position == 6:
            x_qr = addr_features_qr['right_x']
            y_qr = addr_features_qr['row_three_y']

            x_addr = addr_features_addr['column_two_x']
            y_addr = addr_features_addr['bottom_y']

            x_label = addr_features_label['right_x']
            y_label = addr_features_label['row_three_y']
            
        elif position == 7:
            x_qr = addr_features_qr['left_x']
            y_qr = addr_features_qr['row_four_y']

            x_addr = addr_features_addr['column_one_x']
            y_addr = addr_features_addr['top_y']

            x_label = addr_features_label['left_x']
            y_label = addr_features_label['row_four_y']
            
        elif position == 8:
            x_qr = addr_features_qr['right_x']
            y_qr = addr_features_qr['row_four_y']

            x_addr = addr_features_addr['column_one_x']
            y_addr = addr_features_addr['bottom_y']

            x_label = addr_features_label['right_x']
            y_label = addr_features_label['row_four_y']

        if element == 'qr':
            logger.info('Adding QR code to address card overlay.')
            # QR Code
            with Image(filename=addr_file) as layout:
                with Image(filename=qr_png_path) as img:
                    img.resize(addr_features_qr['square_elements'][0], addr_features_qr['square_elements'][1])
                    layout.composite(img, left=x_qr, top=y_qr)
                    layout.save(filename=addr_file)

        elif element == 'address':
            logger.info('Adding public address to address card overlay.')
            # Public Address
            with Drawing() as draw:
                draw.font_family = 'Ubuntu'
                draw.font_size = addr_features_addr['font_size']
                draw.text_alignment = 'center'
                draw.text(x_addr, y_addr, text)
                with Image(filename=addr_file) as layout:
                    layout.rotate(90)
                    draw.draw(layout)
                    layout.rotate(270)
                    layout.save(filename=addr_file)

        elif element == 'label':
            logger.info('Adding label to address card overlay.')
            # Label
            with Drawing() as draw:
                draw.font_family = 'Ubuntu'
                draw.font_style = 'oblique'
                draw.font_size = addr_features_label['font_size']
                draw.text_alignment = 'left'
                draw.text(x_label, y_label, text)
                with Image(filename=addr_file) as layout:
                    draw.draw(layout)
                    layout.save(filename=addr_file)

    except Exception as e:
        logger.exception('Exception while drawing info on address layout.')
        logger.exception(e)
        raise


def merge_format_pdfs(path):
    try:
        os.chdir(path)
        contents = os.listdir()
        logger.debug('contents: ' + str(contents))

        os.mkdir('tmp/')

        # Merge bill files, if multiple present
        pdf_files_bill = []
        for file in contents:
            if file.endswith('.pdf'):
                if file.split('_')[1] != 'addr':
                    pdf_files_bill.append(file)
                    logger.debug('file: ' + file)
                else:
                    logger.debug('Skipping address file: ' + file)
        pdf_files_bill.sort()
        logger.debug('pdf_files_bill: ' + str(pdf_files_bill))

        if len(pdf_files_bill) > 1:
            logger.info('Multiple bill overlays found. Merging.')
            merger = PdfFileMerger()
            merged_output = 'overlay.pdf'

            for doc in pdf_files_bill:
                file = open(doc, 'rb')
                merger.append(fileobj=file)

            output = open(merged_output, 'wb')
            merger.write(output)
            
            logger.info('Cleaning-up pdf directory.')
            for doc in pdf_files_bill:
                os.rename(doc, ('tmp/' + doc))
        
        else:
            logger.info('Multiple bill overlays not found. Renaming overlay and skipping merge.')
            os.rename('overlay_1.pdf', 'overlay.pdf')

        # Merge address overlays, if multiple present
        pdf_files_addr = []
        for file in contents:
            if file.endswith('.pdf'):
                if file.split('_')[1] == 'addr':
                    pdf_files_addr.append(file)
                    logger.debug('file: ' + file)
                else:
                    logger.debug('Skipping bill file: ' + file)
        pdf_files_addr.sort()
        logger.debug('pdf_files_addr: ' + str(pdf_files_addr))

        if len(pdf_files_addr) > 1:
            logger.info('Multiple address overlays found. Merging.')
            merger = PdfFileMerger()
            merged_output = 'overlay_addr.pdf'

            for doc in pdf_files_addr:
                file = open(doc, 'rb')
                merger.append(fileobj=file)

            output = open(merged_output, 'wb')
            merger.write(output)
            
            logger.info('Cleaning-up pdf directory.')
            for doc in pdf_files_addr:
                os.rename(doc, ('tmp/' + doc))

        else:
            logger.info('Multiple address overlays not found. Renaming overlay and skipping merge.')
            os.rename('overlay_addr_1.pdf', 'overlay_addr.pdf')

    except Exception as e:
        logger.exception('Exception while merging PDF files.')
        logger.exception(e)
        raise


if __name__ == '__main__':
    try:
        if merge_only == False:
            bill_features = get_config('bill')
            addr_features_qr = get_config('address', 'qr')
            addr_features_addr = get_config('address', 'addr')
            addr_features_label = get_config('address', 'label')
        
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

            logger.info('Creating bill feature elements.')
            create_seed(seed, wallet_file)
            create_qr(public_address, wallet_file)

            if create_overlay == True:
                # Construct label for overlay
                label_current = '#' + wallet_file
                if serial_number != '':
                    label_current = label_current + ' - ' + serial_number
                logger.debug('label_current: ' + label_current)
                
                # Determine overlay number and file name based on wallet number
                overlay_num_bill = str(math.ceil(int(wallet_file) / 3))
                logger.debug('overlay_num: ' + overlay_num_bill)

                overlay_num_addr = str(math.ceil(int(wallet_file) / 8))
                logger.debug('overlay_num: ' + overlay_num_addr)

                # Set file suffix based on desired output
                if output_pdf == True:
                    bill_file = '../overlay_' + overlay_num_bill + '.pdf'
                    addr_file = '../overlay_addr_' + overlay_num_addr + '.pdf'
                else:
                    bill_file = '../overlay_' + overlay_num_bill + '.png'
                    addr_file = '../overlay_addr_' + overlay_num_addr + '.png'
                logger.debug('bill_file: ' + bill_file)
                logger.debug('addr_file: ' + addr_file)
                
                #### BILL OVERLAY FUNCTIONS ####
                logger.info('Creating bill print overlay.')
                if os.path.isfile(bill_file) == False:
                    logger.info('Creating new bill canvas.')
                    if demo_mode == False:
                        draw_canvas('bill')
                    else:
                        import_demo_layout('bill')
                else:
                    logger.info('Using existing bill canvas.')

                pos_modulo_bill = int(wallet_file) % 3
                logger.debug('pos_modulo_bill: ' + str(pos_modulo_bill))
                # pos_modulo_bill = 1 --> Top bill
                # pos_modulo_bill = 2 --> Middle bill
                # pos_modulo_bill = 3 --> Bottom bill
                
                #bill_positions = ['top', 'middle', 'bottom']
                bill_positions = ['bottom', 'top', 'middle']
                logger.debug('bill_positions[pos_modulo_bill]: ' + bill_positions[pos_modulo_bill])
                
                draw_address(public_address, bill_positions[pos_modulo_bill])
                draw_qr(bill_positions[pos_modulo_bill])
                draw_seed(bill_positions[pos_modulo_bill])
                draw_label(bill_positions[pos_modulo_bill], label_current)

                #### ADDRESS CARD OVERLAY FUNCTIONS ####
                logger.info('Creating address card print overlay.')
                if os.path.isfile(addr_file) == False:
                    logger.info('Creating new address canvas.')
                    if demo_mode == False:
                        draw_canvas('address')
                    else:
                        import_demo_layout('address')
                else:
                    logger.info('Using existing address canvas.')

                pos_modulo_addr = int(wallet_file) % 8
                logger.debug('pos_modulo_addr: ' + str(pos_modulo_addr))

                addr_positions = [8, 1, 2, 3, 4, 5, 6, 7]
                logger.debug('addr_positions[pos_modulo_addr]: ' + str(addr_positions[pos_modulo_addr]))

                draw_address_layout(addr_positions[pos_modulo_addr], 'qr')
                draw_address_layout(addr_positions[pos_modulo_addr], 'address', public_address)
                draw_address_layout(addr_positions[pos_modulo_addr], 'label', label_current)

        else:
            logger.info('Merging PDF files, if multiple present.')
            merge_format_pdfs(wallet_dir)

    except KeyboardInterrupt:
        logger.info('Exit signal received.')
        sys.exit()
    
    except Exception as e:
        logger.exception(e)
        sys.exit(1)
