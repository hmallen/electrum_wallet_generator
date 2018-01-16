import argparse
import glob
import logging
import os
from qrcodegen import QrCode, QrSegment
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', type=str, help='Directory containing wallet and txt files.')
args = parser.parse_args()

wallet_dir = args.directory

if wallet_dir == None:
    logger.error('No wallet directory defined. Exiting.')
    sys.exit(1)
else:
    logger.info('Wallet directory defined as ' + wallet_dir)


def create_svg(addr, name):
    os.chdir('../../..')
    
    errcorlvl = QrCode.Ecc.HIGH # Error correction level. Need to determine best setting!

    try:
        qr_data = 'bitcoin:' + addr
        qr_pub = QrCode.encode_text(qr_data, errcorlvl)
        qr_svg_pub = qr_pub.to_svg_str(4)

        file_name_pub = wallet_dir + name + '_pub.svg'
        logger.debug(file_name_pub)
        
        with open(file_name_pub, 'w') as svg_file:
            svg_file.write(qr_svg_pub)

    except Exception as e:
        logger.exception('Exception while creating svg files.')
        logger.exception(e)
        raise
        

if __name__ == '__main__':
    try:
        os.chdir(wallet_dir)
        
        for file in glob.glob('*.txt'):
            file_path = file

        file_name = file_path.strip('.txt')

        if not file_path:
            logger.error('No txt address file found. Exiting.')
            sys.exit(1)
        
        with open(file_path, 'r') as address_file:
            for line in address_file:
                if '1' in line:
                    public_address = line.strip('\n')

        print(public_address)
        
        create_svg(public_address, file_name)
    
    except Exception as e:
        logger.exception(e)
        sys.exit(1)
