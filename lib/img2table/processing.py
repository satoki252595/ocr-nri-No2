## OCRのAPIの使用により、空白検出は気まぐれのため、OCRの読み取り後に空白や改行コード削除処理を行う。

## ★制約として、現新比較する場合に空白を検知できないので、そこを見分ける必要がある。　
## ★制約として、表のフッダー部分は差分を検知できない。

import pandas as pd
from img2table.document import Image
from img2table.ocr import AzureOCR
import cv2
from PIL import Image as PILImage

import configparser

def setOCRSetting(ocr_model):  
    
    match ocr_model:
        case 'Azure':
            config = configparser.ConfigParser()
            config.read('config.ini')
            key = config['setting']['ACCOUNT_KEY']
            endpoint = config['setting']['END_POINT']
        case _:
            key = endpoint = ''
            
    return key,endpoint

def check_true(target):
    
    if isinstance(target,bool):
        return 'title',target
    if isinstance(target,pd.core.frame.DataFrame):
        x = True
        for b in target.all():
            x *= b
        return 'table',bool(x)

class imagetable(object):
    
    def __init__(self,image_folder_pass:str,png_img_name:str):
        self.image_folder_pass = image_folder_pass
        self.png_img_name = png_img_name
        
    def getImageTable_Azure(self,MA_Flag:str,lessFlag= False):
        
        if MA_Flag == 'mae':
            png_image_pass = self.image_folder_pass + 'mae/' + self.png_img_name
        elif MA_Flag == 'ato':
            png_image_pass = self.image_folder_pass + 'ato/' + self.png_img_name
        else:
            png_image_pass = None
        
        key,endpoint = setOCRSetting('Azeru')
        # Instantiation of OCR
        ocr = AzureOCR(endpoint=endpoint,subscription_key=key)

        # Instantiation of document, either an image or a PDF
        doc = Image(src = png_image_pass)

        
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

    def visualFrameTable(self,extracted_tables,MA_Flag:str):

        if MA_Flag == 'mae':
            
            # Display extracted tables
            table_img = cv2.imread(self.image_folder_pass +'mae/'+self.png_img_name)

        if MA_Flag == 'ato':
            # Display extracted tables
            table_img = cv2.imread(self.image_folder_pass +'ato/'+self.png_img_name)
            

        for table in extracted_tables:
            for row in table.content.values():
                for cell in row:
                    cv2.rectangle(table_img, (cell.bbox.x1, cell.bbox.y1), (cell.bbox.x2, cell.bbox.y2), (255, 0, 0), 2)
                    
        return table_img

    def cleansing(self,extracted_tables):
        
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
        
    def diff_draw(self,t_mae_cleansing,t_ato_cleansing,mae_img,ato_img,t_mae,t_ato):

        for idx,(mae,ato) in enumerate(zip(t_mae_cleansing,t_ato_cleansing)):
            for jdx,(m,a) in enumerate(zip(mae,ato)):
                diff = m == a
                info,result = check_true(diff)
        
                ##ここで差分がある場合はImageに赤線などをつける処理を入れる。
                if result == False:
        
                    ##タイトルに差分がある箇所を描画
                    if info == 'title':
                        cv2.line(mae_img,(int(t_mae[idx].bbox.x1), int(t_mae[idx].bbox.y1)), (int(t_mae[idx].bbox.x2), int(t_mae[idx].bbox.y1)), (0, 255, 255), thickness=5, lineType=cv2.LINE_AA)
                        cv2.line(ato_img,(int(t_ato[idx].bbox.x1), int(t_ato[idx].bbox.y1)), (int(t_ato[idx].bbox.x2), int(t_ato[idx].bbox.y1)), (0, 255, 255), thickness=5, lineType=cv2.LINE_AA)
        
                    #セル（表）に差分がある箇所を描画
                    else:
                        for i in range(diff.shape[0]):
                            for j in range(diff.shape[1]):
                                if diff.iloc[i,j] == False:
                                    for ii,row in enumerate(t_mae[idx].content.values()):
                                        for jj,cell in enumerate(row):
                                            if i==ii and j==jj:
                                                cv2.rectangle(mae_img, (cell.bbox.x1, cell.bbox.y1), (cell.bbox.x2, cell.bbox.y2), (255, 0, 0), 2)
                                    for ii,row in enumerate(t_ato[idx].content.values()):
                                        for jj,cell in enumerate(row):
                                            if i==ii and j==jj:
                                                cv2.rectangle(ato_img, (cell.bbox.x1, cell.bbox.y1), (cell.bbox.x2, cell.bbox.y2), (255, 0, 0), 2)
        
        ##そもそも表対象外の部分を表示
        
        if len(t_ato) - len(t_mae) < 0:
            for i,mae in enumerate(t_mae):
                if i > len(t_ato) -1:
                    cv2.rectangle(mae_img, (mae.bbox.x1, mae.bbox.y1), (mae.bbox.x2, mae.bbox.y2), (255, 0, 0), 2)
        elif len(t_ato) - len(t_mae) > 0:
            for i,ato in enumerate(t_ato):
                if i > len(t_mae) -1:
                    cv2.rectangle(ato_img, (ato.bbox.x1, ato.bbox.y1), (ato.bbox.x2, ato.bbox.y2), (255, 0, 0), 2)

        return mae_img,ato_img
