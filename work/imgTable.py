##Azureセットアップ

import configparser

config = configparser.ConfigParser()
config.read('../config.ini')
key = config['setting']['ACCOUNT_KEY']
endpoint = config['setting']['END_POINT']

##OCR関数

from img2table.ocr import TesseractOCR
from img2table.document import Image
from img2table.ocr import AzureOCR
import cv2
from PIL import Image as PILImage

import os

PWD = os.getcwd()

PATH_IMAGE = PWD + '/static/image/'

PATH_IMAGE = PWD + '/static/image/'
PATH_TEXT = PWD + '/static/text/'

def getImageTable_Azuru(img_path):
    
    # Instantiation of OCR
    ocr = AzureOCR(endpoint=endpoint,subscription_key=key)

    # Instantiation of document, either an image or a PDF
    doc = Image(src = img_path)

    # Table extraction
    extracted_tables = doc.extract_tables(ocr=ocr,
                                        implicit_rows=True,
                                        borderless_tables=True,
                                        min_confidence=50)
    
    return extracted_tables

def visualTable(extracted_tables,imageFileName,BA_Flag='mae'):

    if BA_Flag == 'mae':
        
        # Display extracted tables
        table_img = cv2.imread(PATH_IMAGE +'mae/'+imageFileName)

    if BA_Flag == 'ato':
        # Display extracted tables
        table_img = cv2.imread(PATH_IMAGE +'ato/'+imageFileName)
        

    for table in extracted_tables:
        for row in table.content.values():
            for cell in row:
                cv2.rectangle(table_img, (cell.bbox.x1, cell.bbox.y1), (cell.bbox.x2, cell.bbox.y2), (255, 0, 0), 2)
                
    return PILImage.fromarray(table_img)

if __name__ == '__main__':
        
    t_mae = extracted_tables = getImageTable_Azuru(PATH_IMAGE + 'mae/'+ '4307.png')
    t_ato = extracted_tables = getImageTable_Azuru(PATH_IMAGE + 'ato/'+ '4307.png')
    vt_mae_image = visualTable(t_mae,'4307.png',BA_Flag='mae')
    vt_ato_image = visualTable(t_ato,'4307.png',BA_Flag='ato')