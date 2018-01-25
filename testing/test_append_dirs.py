import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

test_dir = '../wallets/01242018_220402/'

if __name__ == '__main__':
    os.chdir(test_dir)
    contents_all = os.listdir()
    logger.debug('contents_all: ' + str(contents_all))

    contents = []
    for item in contents_all:
        logger.debug('item: ' + item)
        if not os.path.isfile(item) and item != 'tmp':
            contents.append(item)
    logger.debug('contents (unsorted): ' + str(contents))

    contents.sort()
    logger.debug('contents (sorted): ' + str(contents))
