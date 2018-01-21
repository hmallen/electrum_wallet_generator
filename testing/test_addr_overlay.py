import configparser
import logging
import os
import sys
from wand.image import Image
from wand.display import display
from wand.drawing import Drawing
from wand.color import Color

output_pdf = True

demo_layout_address = '../resources/address_info_card_layout_front.pdf'
demo_address_file = 'demo_address.pdf'
qr_png_path = 'test_qr.png'

bill_config_file = '../config/bill.ini'
address_config_file = '../config/address.ini'

logging.basicConfig(level=logging.DEBUG)
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

    elif config_type == 'address':
        config.read(address_config_file)

        features = {'canvas': config['canvas']['dim'], 'square_elements': config['square_elements']['dim'],
                    'left_x': config[config_element]['left_x'], 'right_x': config[config_element]['right_x'],
                    'row_one_y': config[config_element]['row_one_y'], 'row_two_y': config[config_element]['row_two_y'],
                    'row_three_y': config[config_element]['row_three_y'], 'row_four_y': config[config_element]['row_four_y']}
        
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
                draw.rectangle(left=0, top=0, width=addr_features['canvas'][0], height=addr_features['canvas'][1])
                
                with Image(width=addr_features['canvas'][0], height=addr_features['canvas'][1]) as img:
                    draw.draw(img)
                    img.save(filename=addr_file)

    except Exception as e:
        logger.exception('Exception while drawing canvas.')
        logger.exception(e)
        raise


def draw_address_layout(position):
    #global qr_png_path

    try:
        # 8 positions available on print layout
        # Position argument is an integer from 1-8
        if (position % 2) > 0:
            # Left column
            x = addr_features_qr['left_x']
            logger.debug('Left column')
        else:
            # Right column
            x = addr_features_qr['right_x']
            logger.debug('Right column')

        if position <= 2:
            # First row
            y = addr_features_qr['row_one_y']
        elif 2 < position <= 4:
            # Second row
            y = addr_features_qr['row_two_y']
        elif 4 < position <= 6:
            # Third row
            y = addr_features_qr['row_three_y']
        elif 6 < position <= 8:
            # Fourth row
            y = addr_features_qr['row_four_y']

        logger.debug('x: ' + str(x))
        logger.debug('y: ' + str(y))

        with Image(filename=addr_file) as addr:
            with Image(filename=qr_png_path) as img:
                img.resize(addr_features_qr['square_elements'][0], addr_features_qr['square_elements'][1])
                addr.composite(img, left=x, top=y)
                addr.save(filename=addr_file)

    except Exception as e:
        logger.exception('Exception while drawing info on address layout.')
        logger.exception(e)
        raise


if __name__ == '__main__':
    try:
        bill_features = get_config('bill')
        addr_features_qr = get_config('address', 'qr')

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

        import_demo_layout('address')
        #draw_canvas('address')

        test_array = [1, 2, 3, 4, 5, 6, 7, 8]
        for val in test_array:
            draw_address_layout(val)
        #draw_address_layout(3)

    except Exception as e:
        logger.exception(e)
