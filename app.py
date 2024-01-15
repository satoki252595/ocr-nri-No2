from flask import Flask, render_template, request, url_for, redirect
import os
import ocr

app = Flask(__name__)

PATH = './static/image'

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # URLでhttp://127.0.0.1:5000/uploadを指定したときはGETリクエストとなるのでこっち
    if request.method == 'GET':
        return render_template('upload.html')
    # formでsubmitボタンが押されるとPOSTリクエストとなるのでこっち
    elif request.method == 'POST':
        file = request.files['example']
        file.save(os.path.join(PATH, file.filename))
        return redirect(url_for('uploaded_file', filename=file.filename))


@app.route('/uploaded_file/<string:filename>')
def uploaded_file(filename):
    result = ocr.ocr(PATH + '/' + filename)
    ocr_text = ''
    for line in result.analyze_result.read_results[0].lines:
        ocr_text = ocr_text + line.text + '|'
    return render_template('uploaded_file.html', text=ocr_text)

if __name__ == '__main__':
    app.run(debug=True)