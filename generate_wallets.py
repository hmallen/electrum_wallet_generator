import argparse
from bitcoin import *
import csv
#import datetime
from electrum import mnemonic
import logging
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

output_dir = 'output/'

#dt_current = datetime.datetime.now().strftime('%m%d%Y-%H%M%S')
#address_file = output_dir + dt_current + '_addresses.csv'
address_file = output_dir + 'addresses.csv'

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--number', default=1, type=int, help='Number of wallets to generate. [Default = 1]')
parser.add_argument('-o', '--output', default=address_file, type=str, help='Specify output file. [Default = \'{datetime}_addresses.csv\'')
parser.add_argument('-q', '--qr', default=False, help='Include QR codes of pub/priv keys as svg files in output.')
args = parser.parse_args()

wallet_count = args.number
logger.debug('wallet_count: ' + str(wallet_count))
output_file = args.output
logger.debug('output_file: ' + output_file)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    logger.info('Created output directory.')
else:
    logger.info('Found output directory.')

m = mnemonic.Mnemonic()


def generate_wallets():
    wallet_list = []
    for x in range(0, wallet_count):
        seed = m.make_seed()
        logger.debug(seed)

        priv = sha256(seed)
        logger.debug(priv)
        
        pub = privtopub(priv)
        logger.debug(pub)
        
        addr_pub = pubtoaddr(pub)
        logger.debug(addr_pub)
        
        addr_priv = privtoaddr(priv)
        logger.debug(addr_priv)

        wallet_list.append([seed, addr_pub, addr_priv, pub, priv])

    return wallet_list
        

if __name__ == '__main__':
    try:
        wallets = generate_wallets()
        logger.debug(wallets)

        with open(output_file, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for x in range(0, len(wallets)):
                csv_writer.writerow(wallets[x])
    
    except Exception as e:
        logger.exception(e)
