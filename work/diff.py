##説明

# 引数1：比較前のpng、引数2：比較後のpng
# アウトプットはtext配下のフォルダに差分HTMLを出力する。

##ライブラリimport

import diff_match_patch
import webbrowser

import ocr

import sys
import os

##　前処理

args = sys.argv

mae_image_file_name = str(args[1])
ato_image_file_name = str(args[2])

PWD = os.getcwd()

PATH_IMAGE = PWD + '/static/image/'
PATH_TEXT = PWD + '/static/text/'

##各種関数

def imageToText_Azuru(input_image_path,output_filename):
    # テキストの出力
    with open(PATH_TEXT + output_filename, "w", encoding="utf-8") as f:
        for text_result in ocr.azuru_ocr(input_image_path).analyze_result.read_results:
            for line in text_result.lines:
                f.write(line.text + "\n")
                
def imageToText_pythonOCR(input_image_path,output_filename):
    # テキストの出力
    with open(PATH_TEXT + output_filename, "w", encoding="utf-8") as f:
        f.write(ocr.python_ocr(input_image_path))

def diff_file_text(file_mae,file_ato):
    
    fl1 = PATH_TEXT + 'mae/' + file_mae
    fl2 = PATH_TEXT + 'ato/' + file_ato
    with open(fl1, 'r', encoding='utf-8') as file1, open(fl2, 'r', encoding='utf-8') as file2:
        text1 = file1.read()
        text2 = file2.read()

    # diff_match_patchオブジェクトを作成
    dmp = diff_match_patch.diff_match_patch()

    # テキストを比較して差分を計算
    diffs = dmp.diff_main(text1, text2) # 引数順に意味あり。text1が基準。text2が変更後。
    dmp.diff_cleanupSemantic(diffs)

    # 差分をHTMLで表示
    html = dmp.diff_prettyHtml(diffs)
    with open(PATH_TEXT + "diff_output.html", "w", encoding="utf-8") as html_file:
        html_file.write(html)

    ## デフォルトのウェブブラウザでHTMLファイルを開く
    #webbrowser.open("diff_output.html")
    
##テスト用の実行ふぁいる
    
if __name__ == '__main__':
    
    imageToText_pythonOCR(PATH_IMAGE+'mae/' + mae_image_file_name,'mae/mae.txt')
    imageToText_pythonOCR(PATH_IMAGE+'ato/' + ato_image_file_name,'ato/ato.txt')
    diff_file_text('mae.txt','ato.txt')