from wand.image import Image
from wand.display import display
from wand.drawing import Drawing
from wand.color import Color

bill_layout_file = 'bill_feature_outlines.pdf'
bill_file = 'bill.png'
qr_file = 'wallet/qr.png'
seed_file = 'wallet/seed.png'

test_addr = '1Dc3rcMhtycbavyax4VCp7ToMqfHjeTJPN'
test_seed = 'throw thumb dignity link salute immense brand box chase whip ranch gasp'

# Coordinates of bill features
bill_features = {'canvas': (1836, 2376),
                 'addr_top': (1784, 604), 'addr_middle': (1056, 604), 'addr_bottom': (330, 604),
                 'qr_top': (338, 262), 'qr_middle': (338, 991), 'qr_bottom': (338, 1718),
                 'seed_top': (1257, 471), 'seed_middle': (1257, 1200), 'seed_bottom': (1257, 1926)}


def draw_canvas():
    with Drawing() as draw:
        draw.fill_color = Color('transparent')
        #draw.fill_color = Color('white')
        draw.rectangle(left=0, top=0, width=bill_features['canvas'][0], height=bill_features['canvas'][1])
        with Image(width=bill_features['canvas'][0], height=bill_features['canvas'][1]) as img:
            draw.draw(img)
            img.save(filename=bill_file)


def import_bill_layout():
    with Image(filename=bill_layout_file) as layout:
        layout.resize(bill_features['canvas'][0], bill_features['canvas'][1])
        layout.save(filename=bill_file)


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
    draw_canvas()
    #import_bill_layout()
    
    bill_positions = ['top', 'middle', 'bottom']
    for pos in bill_positions:
        draw_address(pos)
        draw_qr(pos)
        draw_seed(pos)
    
    with Image(filename=bill_file) as img:
        display(img)
