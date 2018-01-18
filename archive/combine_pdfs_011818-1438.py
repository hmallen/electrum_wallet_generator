import argparse
import logging
import os
from PyPDF2 import PdfFileMerger
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', type=str, help='Directory with PDFs to combine.')
args = parser.parse_args()

pdf_dir = args.directory
logger.debug('pdf_dir: ' + pdf_dir)

merger = PdfFileMerger()


def combine_pdfs(pdfs):
    try:
        output_pdf = 'overlay.pdf'

        for doc in pdfs:
            file = open(doc, 'rb')
            merger.append(fileobj=file)

        output = open(output_pdf, 'wb')
        merger.write(output)

    except Exception as e:
        logger.exception('Exception while combining pdfs.')
        logger.exception(e)
        raise


def cleanup(pdfs):
    try:
        os.mkdir('tmp/')

        for doc in pdfs:
            os.rename(doc, ('tmp/' + doc))

    except Exception as e:
        logger.exception('Exception while cleaning-up directory.')
        logger.exception(e)
        raise


if __name__ == '__main__':
    try:
        os.chdir(pdf_dir)
        contents = os.listdir()
        logger.debug('contents: ' + str(contents))
        
        pdf_files = []
        for file in contents:
            if file.endswith('.pdf'):
                pdf_files.append(file)
                logger.debug('file: ' + file)
        logger.debug('pdf_files: ' + str(pdf_files))

        if len(pdf_files) > 1:
            logger.info('Multiple PDF files found. Merging.')
            combine_pdfs(pdf_files)
            logger.info('Cleaning-up pdf directory.')
            cleanup(pdf_files)
        else:
            logger.info('Multiple PDF files not found. Skipping merge.')

    except Exception as e:
        logger.exception(e)
