import argparse
import glob
import json
import logging
import os
from qrcodegen import QrCode, QrSegment
import sys

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

        with open(wallet_file, 'r') as file:
            wallet_info_raw = file.read()

        wallet_info = json.loads(wallet_info_raw)

        seed = wallet_info['keystore']['seed']
        logger.info('Seed: ' + seed)

        seed_file = wallet_file + '_seed.txt'
        with open(seed_file, 'w') as file:
            file.write(seed)

        public_address = wallet_info['addresses']['receiving'][0]
        logger.info('Public address: ' + public_address)

        address_file = wallet_file + '_addr.txt'
        with open(address_file, 'w') as file:
            file.write(public_address)
        
        create_svg(public_address, wallet_file)
    
    except Exception as e:
        logger.exception(e)
        sys.exit(1)
