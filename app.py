from flask import Flask, render_template, request, jsonify
from datetime import datetime
import tensorflow as tf
import numpy as np
import os

# 학습시킨 모델 불러오기 (0이면 고양이, 1이면 강아지)
# 함수 밖에서 불러야 메모리 손실 방지
model = tf.keras.models.load_model('static/model/model.h5')
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # 받은데이터에서 .files로 ' '안의 이름가진 파일 꺼내담기
    file = request.files['file_give']
    title = request.form['title_give']
    extension = file.filename.split('.')[-1]    # 파일 확장자 추출

    #현재시간 담기
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'{mytime}'

    # 저장 경로에다가 현재시간과 확장자로 파일 이름만들어 저장
    save_to = f'static/img/catdog/{title}_{filename}.{extension}'
    file.save(save_to)  # 파일 저장

    return jsonify({'result':'success'})

@app.route('/search', methods=['POST'])
def search():
    title = request.form['title_give']
    filenames = os.listdir('static/img/catdog') # os.listdir : 경로에 있는 파일 리스트 가져오기
    # 유저가 작성한 이름과 일치하는 파일 경로를 저장한다.
    matched_files = ['static/img/catdog/'+filename for filename in filenames if title in filename]
    result_dict = []
    for index, matched_file in enumerate(matched_files):    # enumerate : index값이 있는 for문
        # .load_img로 경로에있는 파일 가져온다.
        image = tf.keras.preprocessing.image.load_img(matched_file, target_size=(256, 256))
        # 이미지형태의 데이터타입을 array로 만듬
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        # [] 로 배치형태 데이터로 만듬 => .predict 할수 있다.
        input_arr = np.array([input_arr])
        predictions = model.predict(input_arr)
        if predictions[0][0] > 0.5:
            result = '강아지'
        else:
            result = '고양이'
        # 파일인덱스번호, 파일경로, 예측결과를 담아서 반환
        result_dict.append({'index': index, 'path':matched_file, 'result':result})
    return jsonify({'predictions': result_dict})

if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)