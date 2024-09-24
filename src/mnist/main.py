from typing import Annotated
from fastapi import FastAPI, File, UploadFile
import os
import uuid
import pymysql.cursors
from datetime import datetime
from pytz import timezone
from mnist.db import get_connection

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
    
  
    # 현재 이곳에 들어오는 시간
    ts = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
    
    # 디렉토리가 없으면 오류, 코드에서 확인 및 만들기 추가
    upload_dir = os.getenv("UPLOAD_DIR", "./photo")
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_full_path = os.path.join(upload_dir,
            f'{uuid.uuid4()}.{file_ext}')

    with open(file_full_path, "wb") as f:
        f.write(img)

    # 파일 저장 경로 DB INSERT
    # tablename : image_processing
    # 컬럼 정보 : num (초기 인서트, 자동 증가)
    # 컬럼 정보 : 파일이름, 파일경로, 요청시간(초기 인서트), 요청사용자(n00)
    # 컬럼 정보 : 예측모델, 예측결과, 예측시간(추후 업데이트)
    import pymysql.cursors
    sql = "INSERT INTO image_processing(file_name, file_path, request_time, request_user) VALUES(%s, %s, %s, %s)"
    connection = get_connection() # db랑 연결 (db.py)

    with connection:
        with connection.cursor() as cursor:
            # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            # cursor.execute(sql, ('webmaster@python.org',))
            cursor.execute(sql,(file_name, file_full_path, ts, "n24"))
        connection.commit()

    return {"filename": file.filename,
            "content_type": file.content_type,
            "file_full_path": file_full_path
            }

@app.get("/all/")
def all():
    from mnist.db import select
    sql = "SELECT * FROM image_processing"
    result = select(query=sql, size=-1)
    return result
    # DB 연결 select all
    # 결과값 리턴

@app.get("/one/")
def one():
    from mnist.db import select
    sql = """SELECT * FROM image_processing
    WHERE prediction_time IS NULL ORDER BY num LIMIT 1"""
    result = select(query=sql, size=1)
    return result[0]
    # DB 연결 select 값 중 하나만 리턴
    # 결과값 리턴

@app.get("/many/")
def many(size: int = -1):

    sql = "SELECT * FROM image_processing WHERE prediction_time IS NULL ORDER BY num"
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchmany(size)

    return result


