import argparse
from cairosvg import svg2png
import configparser
from drawSVG.drawSVG import SVG
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#bill_config_file = 'config/bill.ini'
#address_config_file = 'config/address.ini'

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', type=str, help='Directory containing wallet files for new overlay generation.')
parser.add_argument('-s', '--serial', type=str, default='', help='Starting serial number in series for overlay placement.')
parser.add_argument('-c', '--config', type=str, help='Path to config file for layout element coordinates.')
args = parser.parse_args()

wallet_dir = args.directory
serial_number = args.serial
config_file = args.config

if wallet_dir == None:
    logger.error('No wallet directory defined. Exiting.')
    sys.exit(1)
elif config_file == None:
    logger.error('No config file defined. Exiting.')
    sys.exit(1)


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


if __name__ == '__main__':
    try:
        # Determine wallet count in directory
        os.chdir(wallet_dir)
        contents_all = os.listdir()

        contents = []
        for item in contents_all:
            if not os.path.isfile(item) and item != 'tmp':
                contents.append(item)
        contents.sort()
        logger.debug('Wallet directories: ' + str(contents))

        # Move original overlays into new directory
        os.mkdir('old/')
        os.rename('overlay.pdf', 'old/overlay_orig.pdf')
        os.rename('overlay_addr.pdf', 'old/overlay_addr_orig.pdf')
        
        bill_features = get_config('bill')
        addr_features_qr = get_config('address', 'qr')
        addr_features_addr = get_config('address', 'addr')
        addr_features_label = get_config('address', 'label')

        for directory in contents:
            logger.info('Moving into ' + directory + ' for feature rearrangement.')
            # Move into individual wallet directory
            os.chdir(directory)

            # Get serial number from txt file
            serial_file = directory + '_serial.txt'
            with open(serial_file, 'r') as file:
                serial_current = file.read().rstrip()
            
            # Get public address from txt file
            addr_file = directory + '_addr.txt'
            with open(addr_file, 'r') as file:
                public_address = file.read().rstrip()

            # Construct label for overlay
            label_current = '#' + directory
            if serial_number != '':
                label_current = label_current + ' - ' + serial_number
            logger.debug('label_current: ' + label_current)
            
            # Determine overlay number and file name based on wallet number
            overlay_num_bill = str(math.ceil(int(directory) / 3))
            logger.debug('overlay_num: ' + overlay_num_bill)

            overlay_num_addr = str(math.ceil(int(directory) / 8))
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

            pos_modulo_bill = int(directory) % 3
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

            pos_modulo_addr = int(directory) % 8
            logger.debug('pos_modulo_addr: ' + str(pos_modulo_addr))

            addr_positions = [8, 1, 2, 3, 4, 5, 6, 7]
            logger.debug('addr_positions[pos_modulo_addr]: ' + str(addr_positions[pos_modulo_addr]))

            draw_address_layout(addr_positions[pos_modulo_addr], 'qr')
            draw_address_layout(addr_positions[pos_modulo_addr], 'address', public_address)
            draw_address_layout(addr_positions[pos_modulo_addr], 'label', label_current)

            # Move back into working directory
            os.chdir('../')

    except Exception as e:
        logger.exception(e)
