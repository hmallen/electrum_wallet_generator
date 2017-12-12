from bitcoin import *
from electrum import mnemonic
import logging
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

m = mnemonic.Mnemonic()

if __name__ == '__main__':
    try:
        seed = m.make_seed()
        logger.debug(seed)

        priv = sha256(seed)
        logger.debug(priv)
        
        pub = privtopub(priv)
        logger.debug(pub)
        
        addr = pubtoaddr(pub)
        logger.debug(addr)
        
        addr_priv = privtoaddr(priv)
        logger.debug(addr_priv)
    
    except Exception as e:
        logger.exception(e)
