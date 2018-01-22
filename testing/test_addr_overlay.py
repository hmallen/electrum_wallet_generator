import configparser
import logging
import os
import sys
from wand.image import Image
from wand.display import display
from wand.drawing import Drawing
from wand.color import Color

output_pdf = True

demo_layout_address = '../resources/address_info_card_test_shifted.pdf'
demo_address_file = 'demo_address.pdf'
qr_png_path = 'test_qr.png'

bill_config_file = '../config/bill.ini'
address_config_file = '../config/address.ini'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


"""
def get_config(config_type):
    config = configparser.ConfigParser()
    
    if config_type == 'bill':
        config.read(bill_config_file)
        features = {'NA': 'NA'}

    elif config_type == 'address':
        config.read(address_config_file)

        features = {'canvas': config['canvas']['dim'], 'square_elements': config['square_elements']['dim'],
                    'left_x': config['addr']['left_x'], 'right_x': config['addr']['right_x'],
                    'row_one_y': config['addr']['row_one_y'], 'row_two_y': config['addr']['row_two_y'],
                    'row_three_y': config['addr']['row_three_y'], 'row_four_y': config['addr']['row_four_y']}

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
"""


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
                    'seed_bottom': config['seed']['bottom']}

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


def import_demo_layout(demo_type):
    #global demo_layout_bill, demo_layout_address
    
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

    except Exception as e:
        logger.exception('Exception while drawing canvas.')
        logger.exception(e)
        raise


def draw_address_layout(position, element, text=None):
    #global qr_png_path

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
            logger.info('Adding QR code.')
            # QR Code
            with Image(filename=addr_file) as layout:
                with Image(filename=qr_png_path) as img:
                    img.resize(addr_features_qr['square_elements'][0], addr_features_qr['square_elements'][1])
                    layout.composite(img, left=x_qr, top=y_qr)
                    layout.save(filename=addr_file)

        elif element == 'address':
            logger.info('Adding public address.')
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
            logger.info('Adding label.')
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
        bill_features = get_config('bill')
        addr_features_qr = get_config('address', 'qr')
        addr_features_addr = get_config('address', 'addr')
        addr_features_label = get_config('address', 'label')

        # Set file suffix based on desired output
        if output_pdf == True:
            #bill_file = '../overlay_' + overlay_num + '.pdf'
            bill_file = 'test_bill.pdf'
            addr_file = 'test_address.pdf'
        else:
            #bill_file = '../overlay_' + overlay_num + '.png'
            bill_file = 'test_bill.png'
            addr_file = 'test_address.png'
        logger.debug('bill_file: ' + bill_file)
        logger.debug('addr_file: ' + addr_file)

        draw_canvas('address')
        #import_demo_layout('address')

        test_array = [1, 2, 3, 4, 5, 6, 7, 8]
        #test_array = [1, 2]
        test_addr = '1JqmJ1R1WyfChgBpPiNEJnknzTbPcwiy3m'
        test_labels = ['W701001', 'W701002', 'W701003', 'W701004', 'W701005', 'W701006', 'W701007', 'W701008']
        for pos in test_array:
            logger.info('Creating address card #' + str(pos) + '.')
            draw_address_layout(pos, 'qr')
            draw_address_layout(pos, 'address', test_addr)
            label_current = '#' + str(pos) + ' - ' + test_labels[(pos - 1)]
            draw_address_layout(pos, 'label', label_current)

    except Exception as e:
        logger.exception(e)
