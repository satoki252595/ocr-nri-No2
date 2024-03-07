import os
import cv2
from PIL import Image as PILImage

import processing as p

def diff_image_Azure(image_folder_pass,png_img_name):
    
    img_obj = p.imagetable(image_folder_pass,png_img_name)

    mae_extracted_tables = img_obj.getImageTable_Azure('mae')
    ato_extracted_tables = img_obj.getImageTable_Azure('ato')
    
    print(len(mae_extracted_tables))

    mae_cleansing_tables = img_obj.cleansing(mae_extracted_tables)
    ato_cleansing_tables = img_obj.cleansing(ato_extracted_tables)

    mae_frame_img = img_obj.visualFrameTable(mae_extracted_tables,MA_Flag = 'mae')
    ato_frame_img = img_obj.visualFrameTable(ato_extracted_tables,MA_Flag = 'ato')

    mae_img = cv2.imread(image_folder_pass +'mae/'+png_img_name)
    ato_img = cv2.imread(image_folder_pass +'ato/'+png_img_name)

    mae_diff_img,ato_diff_img = img_obj.diff_draw(
        mae_cleansing_tables,ato_cleansing_tables,
        mae_img,ato_img,mae_extracted_tables,ato_extracted_tables  
    )
    
    return mae_diff_img,ato_diff_img

if __name__ == '__main__':
    
    PWD = '/Users/satoki252595/work/20240114_nriocr2'
    image_folder_pass = PWD + '/static/image/'
    png_img_name = '4307_2024.png'
    mae_diff_img,ato_diff_img  = diff_image_Azure(image_folder_pass,png_img_name)
    PILImage.fromarray(mae_diff_img)