import diff_match_patch
from img2table.document import Image

from IPython.display import display_html
from PIL import Image as PILImage
from openpyxl import load_workbook
from io import BytesIO
import cv2

from img2table.ocr import TesseractOCR
from img2table.document import Image


import webbrowser

import ocr

import sys
import os


PWD = os.getcwd()

PATH_IMAGE = PWD + '/static/image/'
PATH_TEXT = PWD + '/static/text/'

def getImageTable(img_path):
    
    # Instantiation of OCR
    ocr = TesseractOCR(n_threads=1, lang="jpn")

    # Instantiation of document, either an image or a PDF
    doc = Image(src = img_path)

    # Table extraction
    extracted_tables = doc.extract_tables(ocr=ocr,
                                        implicit_rows=False,
                                        borderless_tables=False,
                                        min_confidence=50)

    
    return extracted_tables

if __name__ == '__main__':
    
    result = getImageTable(PATH_IMAGE + '4307.png')
    print(result)