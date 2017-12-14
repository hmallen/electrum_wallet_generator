import argparse
from bitcoin import *
import csv
import datetime
from electrum import mnemonic
import logging
from qrcodegen import QrCode, QrSegment
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

dt_current = datetime.datetime.now().strftime('%m%d%Y_%H%M%S')
output_dir = 'output/' + dt_current +'/'

#address_file = output_dir + dt_current + '_addresses.csv'
address_file = output_dir + 'addresses.csv'

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', default=False, help='Include DEBUG level output.')
parser.add_argument('-n', '--number', default=1, type=int, help='Number of wallets to generate. [Default = 1]')
parser.add_argument('-o', '--output', default=address_file, type=str, help='Specify output file. [Default = \'output/addresses.csv\'')
parser.add_argument('-q', '--qr', action='store_true', default=False, help='Include QR codes of pub/priv keys as svg files in output.')
args = parser.parse_args()

debug = args.debug
if debug == False:
    logger.setLevel(logging.INFO)
logger.debug('debug: ' + str(debug))
wallet_count = args.number
logger.debug('wallet_count: ' + str(wallet_count))
output_path = args.output
logger.debug('output_path: ' + output_path)
qr_output = args.qr
logger.debug('qr_output: ' + str(qr_output))

logger.info('Creating ' + str(wallet_count) + ' wallets.')
logger.info('Output directory: ' + output_dir)
logger.info('QR Creation: ' + str(qr_output))

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    logger.info('Created output directory.')
else:
    logger.info('Found output directory.')


def generate_wallets():
    wallet_list = []
    try:
        for x in range(0, wallet_count):
            seed = m.make_seed()
            logger.debug(seed)

            bip32_priv = bip32_master_key(seed.encode('utf-8'))
            logger.debug(bip32_priv)

            bip32_pub = bip32_privtopub(bip32_priv)
            logger.debug(bip32_pub)

            bip32_extract = bip32_extract_key(bip32_pub)
            logger.debug(bip32_extract)
            
            addr = pubtoaddr(bip32_extract)
            logger.debug(bip32_extract)

            wallet_list.append([seed, addr, bip32_pub, bip32_priv])
            
    except Exception as e:
        logger.exception(e)
        raise

    return wallet_list


def create_svg(input_file):
    global output_dir
    
    errcorlvl = QrCode.Ecc.QUARTILE # Error correction level. Need to determine best setting!
    svg_list = []

    with open(input_file, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        try:
            count = 0
            output_dir_initial = output_dir
            for row in csv_reader:
                count += 1
                output_dir = output_dir_initial + str(count) + '/'
                os.makedirs(output_dir)
                
                qr_pub = QrCode.encode_text(row[1], errcorlvl)
                qr_svg_pub = qr_pub.to_svg_str(4)
                
                file_name_pub = output_dir + str(count) + '_pub.svg'
                logger.debug(file_name_pub)
                
                with open(file_name_pub, 'w') as svg_file:
                    svg_file.write(qr_svg_pub)

                file_name_info = output_dir + str(count) + '_info.txt'
                with open(file_name_info, 'w') as info_file:
                    info_file.write(row[0])
                    info_file.write('\n\n')
                    info_file.write(row[1])
                    #info_file.write('\n\n')
                    #info_file.write(row[4])

        except Exception as e:
            logger.exception('Exception while creating svg files.')
            logger.exception(e)
            raise
        

if __name__ == '__main__':
    language = 'english'
    m = mnemonic.Mnemonic()

    try:
        wallets = generate_wallets()
        logger.debug(wallets)

        with open(output_path, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for x in range(0, len(wallets)):
                logger.info(str(x) + ': ' + str(wallets[x]))
                csv_writer.writerow(wallets[x])

        if qr_output == True:
            logger.info('Creating QR codes.')
            create_svg(output_path)
    
    except Exception as e:
        logger.exception(e)
        sys.exit(1)
