## OCRのAPIの使用により、空白検出は気まぐれのため、OCRの読み取り後に空白や改行コード削除処理を行う。

## ★制約として、現新比較する場合に空白を検知できないので、そこを見分ける必要がある。　
## ★制約として、表のフッダー部分は差分を検知できない。

##Azureセットアップ

import configparser
import pandas

config = configparser.ConfigParser()
config.read('config.ini')
key = config['setting']['ACCOUNT_KEY']
endpoint = config['setting']['END_POINT']

##OCR関数

from img2table.document import Image
from img2table.ocr import AzureOCR
import cv2
from PIL import Image as PILImage

import os

##PWD = os.getcwd()
PWD = '/Users/satoki252595/work/20240114_nriocr2'

PATH_IMAGE = PWD + '/static/image/'
PATH_IMAGE = PWD + '/static/image/'
PATH_TEXT = PWD + '/static/text/'

def getImageTable_Azuru(img_path,lessFlag= False):
    
    # Instantiation of OCR
    ocr = AzureOCR(endpoint=endpoint,subscription_key=key)

    # Instantiation of document, either an image or a PDF
    doc = Image(src = img_path)

    
    # 見えない線を加味オプション設定。
    implicit_rows = False
    borderless_tables = False
    if lessFlag == True:
        implicit_rows = True
        borderless_tables = True
        

    # Table extraction
    extracted_tables = doc.extract_tables(ocr=ocr,
                                        implicit_rows=implicit_rows,
                                        borderless_tables=borderless_tables,
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

def cleansing(extracted_tables):
    
    t_extracted_tables_cleansing = []
    
    for t_mae_ExtractedTable in extracted_tables:
        if t_mae_ExtractedTable.title != None:
            title = t_mae_ExtractedTable.title.replace('\n','')
            title = title.replace(' ','')
            title = title.replace('　','')
        else:
            title = ''
        df = t_mae_ExtractedTable.df.fillna('')
        df = df.replace('\n','',regex=True)
        df = df.replace(' ','',regex=True)
        df = df.replace('　','',regex=True)
        t_extracted_tables_cleansing.append([title,df])
        
        return t_extracted_tables_cleansing

def check_true(target):
    
    if isinstance(target,bool):
        return 'title',target
    if isinstance(target,pandas.core.frame.DataFrame):
        x = True
        for b in target.all():
            x *= b
        return 'table',bool(x)

FileName = '4307_2024.png'
    
t_mae  = getImageTable_Azuru(PATH_IMAGE + 'mae/'+ FileName,lessFlag = False)
t_ato  = getImageTable_Azuru(PATH_IMAGE + 'ato/'+ FileName,lessFlag = False)
# vt_mae_image = visualTable(t_mae,FileName,BA_Flag='mae')
# vt_ato_image = visualTable(t_ato,FileName,BA_Flag='ato')
t_mae_cleansing = cleansing(t_mae)
t_ato_cleansing = cleansing(t_ato)

