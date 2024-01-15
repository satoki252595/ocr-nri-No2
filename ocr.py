import configparser
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import ComputerVisionOcrErrorException

config = configparser.ConfigParser()
config.read('config.ini')
key = config['setting']['ACCOUNT_KEY']
endpoint = config['setting']['END_POINT']
# image_path = "static/image/41372.png"  # ローカルの画像パス

def ocr(image_path):
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


# print("Texts are written to output.txt")


if __name__ == "__main__":
    result = ocr(image_path)
    for line in result.analyze_result.read_results[0].lines:
        print(line.text)