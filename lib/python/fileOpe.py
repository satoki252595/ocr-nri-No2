
import os
import glob

def get_file_list(image_folder_pass:str):

    mae_png_img_name_list =[]
    ato_png_img_name_list =[]

    for f in glob.glob(image_folder_pass + 'mae/*'):
        mae_png_img_name_list.append(os.path.split(f)[1])
        mae_png_img_name_set = set(mae_png_img_name_list)
    for f in glob.glob(image_folder_pass + 'ato/*'):
        ato_png_img_name_list.append(os.path.split(f)[1])
        ato_png_img_name_set = set(ato_png_img_name_list)
        
    and_list = list(mae_png_img_name_set & ato_png_img_name_set)
    diff_list = list(mae_png_img_name_set ^ ato_png_img_name_set)
    
    return and_list,diff_list