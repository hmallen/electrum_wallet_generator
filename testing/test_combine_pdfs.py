import logging
import os
from PyPDF2 import PdfFileMerger

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

merger = PdfFileMerger()


def combine_pdfs(pdfs):
    output_pdf = 'overlay.pdf'

    for doc in pdfs:
        file = open(doc, 'rb')
        merger.append(fileobj=file)

    output = open(output_pdf, 'wb')
    merger.write(output)


if __name__ == '__main__':
    contents = os.listdir()
    logger.debug('contents: ' + str(contents))
    
    pdf_files = []
    for file in contents:
        if file.endswith('.pdf'):
            pdf_files.append(file)
            logger.debug('file: ' + file)
    logger.debug('pdf_files: ' + str(pdf_files))

    if len(pdf_files) > 1:
        combine_pdfs(pdf_files)
