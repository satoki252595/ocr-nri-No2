import os
import cv2
from PIL import Image as PILImage
import tqdm

from lib.python import processing as p
from lib.python import fileOpe

def diff_image_Azure(image_folder_pass,png_img_name):
    
    img_obj = p.imagetable(image_folder_pass,png_img_name)

    mae_extracted_tables = img_obj.getImageTable_Azure('mae')
    ato_extracted_tables = img_obj.getImageTable_Azure('ato')

    mae_cleansing_tables = img_obj.cleansing(mae_extracted_tables)
    ato_cleansing_tables = img_obj.cleansing(ato_extracted_tables)
    
    print('★★★★★★')
    print(len(mae_extracted_tables))

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
    
    #PWD = '/Users/satoki252595/work/20240114_nriocr2'
    PWD = os.getcwd()
    image_folder_pass = PWD + '/static/image/'
    image_folder_output_pass = PWD + '/static/output_image/'

    and_list,diff_list = fileOpe.get_file_list(image_folder_pass)
    
    if len(diff_list) != 0:
        print('以下のファイルは同一名のファイルではないので、現新比較対象外です')    
        print(diff_list)
        
    for png_img_name in tqdm.tqdm(and_list):
    
        mae_diff_img,ato_diff_img  = diff_image_Azure(image_folder_pass,png_img_name)
        mae_img = PILImage.fromarray(mae_diff_img)
        ato_img = PILImage.fromarray(ato_diff_img)
        mae_img.save(image_folder_output_pass + 'mae/' + png_img_name)
        ato_img.save(image_folder_output_pass + 'ato/' + png_img_name)
        
    print('現新比較が終了しました。') 
    