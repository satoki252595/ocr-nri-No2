import configparser
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import ComputerVisionOcrErrorException

import pyocr
from PIL import Image, ImageEnhance

import os,sys

config = configparser.ConfigParser()
config.read('config.ini')
key = config['setting']['ACCOUNT_KEY']
endpoint = config['setting']['END_POINT']
# image_path = "static/image/41372.png"  # ローカルの画像パス

def azuru_ocr(image_path):
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))
    local_image = open(image_path, "rb")
    try:
        recognize_results = computervision_client.read_in_stream(local_image, language="ja", raw=True)
    except ComputerVisionOcrErrorException as e:
        print("errors:", e.response)
        raise e
    # 結果を取得するための操作IDを取得
    operation_location_remote = recognize_results.headers["Operation-Location"]
    operation_id = operation_location_remote.split("/")[-1]

    # 結果が利用可能になるまで待つ
    while True:
        get_text_results = computervision_client.get_read_result(operation_id)
        if get_text_results.status not in ["notStarted", "running"]:
            break
        time.sleep(1)
        
    return get_text_results

#     # テキストの出力
#     if get_text_results.status == OperationStatusCodes.succeeded:
#         with open("output.txt", "w", encoding="utf-8") as f:
#             for text_result in get_text_results.analyze_result.read_results:
#                 for line in text_result.lines:
#                     f.write(line.text + "\n")

def python_ocr(image_file_name):
    
    #OCRエンジン取得
    tools = pyocr.get_available_tools()
    tool = tools[0]

    #OCRの設定 ※tesseract_layout=6が精度には重要。デフォルトは3
    builder = pyocr.builders.TextBuilder(tesseract_layout=6)

    #解析画像読み込み(雨ニモマケズ)
    img = Image.open(image_file_name) #他の拡張子でもOK

    #適当に画像処理(何もしないと結構制度悪いです・・)
    img_g = img.convert('L') #Gray変換
    enhancer= ImageEnhance.Contrast(img_g) #コントラストを上げる
    img_con = enhancer.enhance(2.0) #コントラストを上げる

    #画像からOCRで日本語を読んで、文字列として取り出す
    txt_pyocr = tool.image_to_string(img , lang='jpn', builder=builder)

    #半角スペースを消す ※読みやすくするため
    txt_pyocr = txt_pyocr.replace(' ', '')

    return txt_pyocr


if __name__ == "__main__":
    result = python_ocr("mae.png")
    print(result)