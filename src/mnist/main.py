from typing import Annotated
from fastapi import FastAPI, File, UploadFile
import os

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # 파일 저장
    img = await file.read()
    file_name = file.filename
    file_ext = file.content_type.split('/')[-1]

    # 디렉토리가 없으면 오류, 코드에서 확인 및 만들기 추가
    upload_dir = "/home/manggee/code/mnist/img"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_full_path = os.path.join(upload_dir,
            f'{uuid.uuid4()}.{file_exec}')

    with open(file_full_path, "wb") as f:
        f.write(img)

    # 파일 저장 경로 DB INSERT
    # tablename : image_processing
    # 컬럼 정보 : num (초기 인서트, 자동 증가)
    # 컬럼 정보 : 파일이름, 파일경로, 요청시간(초기 인서트), 요청사용자(n00)
    # 컬럼 정보 : 예측모델, 예측결과, 예측시간(추후 업데이트)
    import pymysql.cursors
    sql = "INSERT INTO image_processing(file_name, file_path, request_time, request_user) VALUES(%s, %s, %s, %s)"
    conn = pymysql.connect(host='127.0.0.1', port = 53306,
                            user = 'mnist', password = '1234',
                            database = 'mnistdb',
                            cursorclass=pymysql.cursors.DictCursor)
    
    return {"filename": file.filename,
            "content_type": file.content_type,
            "file_full_path": file_full_path
            }
