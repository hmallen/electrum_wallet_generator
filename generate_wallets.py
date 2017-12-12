import argparse
from bitcoin import *
import csv
import datetime
from electrum import mnemonic
import logging
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

dt_current = datetime.datetime.now().strftime('%m%d%Y-%H%M%S')
address_file = dt_current + '_addresses.csv'

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--number', default=1, type=int, help='Number of wallets to generate. [Default = 1]')
parser.add_argument('-o', '--output', default=address_file, type=str, help='Specify output file. [Default = \'{datetime}_addresses.csv\'')
args = parser.parse_args()

wallet_count = args.number
logger.debug('wallet_count: ' + str(wallet_count))
output_file = args.output
logger.debug('output_file: ' + output_file)

m = mnemonic.Mnemonic()

if __name__ == '__main__':
    try:
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

            with open(output_file, 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow([seed, addr_pub, addr_priv, pub, priv])
                
    
    except Exception as e:
        logger.exception(e)
