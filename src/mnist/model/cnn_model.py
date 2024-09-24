import numpy as np
from PIL import Image
from keras.models import load_model
import os

def get_model_path():
    #path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.dirname(__file__)
    model_path = path + "/" + "mnist240924.keras"
    return model_path

# 모델 로드
model = load_model(get_model_path())  # 학습된 모델 파일 경로

# 사용자 이미지 불러오기 및 전처리
def preprocess_image(image_path):
    img = Image.open(image_path).convert('L')  # 흑백 이미지로 변환
    img = img.resize((28, 28))  # 크기 조정

    # 흑백 반전
    #img = 255 - np.array(img)  # 흑백 반전
    
    img = np.array(img)
    img = img.reshape(1, 28, 28, 1)  # 모델 입력 형태에 맞게 변형
    img = img / 255.0  # 정규화
    return img

# 예측
def predict_digit(image_path):
    img = preprocess_image(image_path)
    prediction = model.predict(img)
    digit = np.argmax(prediction) # 예측한 값 중 가장 높은 값인 애를 정답으로 데려 옴
    return digit
