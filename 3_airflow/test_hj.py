import json
from datetime import datetime 
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd 
import pandas as np
from sqlalchemy import create_engine

## 로직 
## log파일 데이터 로드하기 
## log파일 중 2주 정도의 데이터만 가져오기 
## target으로 DB화 하는 것이 목표!
## DB업그레이드 하도록 만들기  
## 이후에는 SQL로 조회하도록..?




## 데이터 로드 
def data_load():
    
    json_data_list = []
    with open('/home/ubuntu/web/recipe_web/logsfolder/json_log.log', 'r') as json_file:
        for line in json_file:
            json_data = json.loads(line)
            json_data_list.append(json_data)

    df = pd.DataFrame(json_data_list)
    df = df[(df['postid'] <= 200) | (pd.to_datetime(df['asctime']) >= '2023-12-30')]
    return df


## 데이터처리
def data_process():
    # 나이대변수생성
    df = data_load()
    
    df['age_group'] = df.age // 10 * 10
    target = df[df.modulename == 'detail'][['age_group','sex', 'postid']]
    
    return target


## 전처리된 로그 데이터를 DB에 업데이트하기 >> 이후 mysql에서 쿼리작성
def data_DB():
    # MySQL 연결 정보 설정
    db_connection_str = '보안상삭제'
    db_connection = create_engine(db_connection_str)
    
    target = data_process()
    target.to_sql(name='userlog_detail', con=db_connection, if_exists='replace', index=False) 
    # if_exists='append' 는 기존의 DB에 추가 if_exists='replace'는 기존의 DB 삭제 후 새로 저장  

###########################################################################################################


# 시작일 정의
default_args = {'start_date': datetime(2023, 12, 27),}

# DAG정의
with DAG(
    dag_id="user-recom-pipeline", # dag 이름 
    schedule_interval="@hourly",
    default_args=default_args, # dag 초기화 파라미터 생성
    tags=["recipe", "recommend"], # tag명 설정
    catchup=False ) as dag:
    
    # 1. 데이터 가져오기 
    load_data =  PythonOperator(
        task_id="load_data",
		python_callable= data_load # 실행 시킬 함수
    )
    
    # 2. 데이터 전처리
    
    process_data =  PythonOperator(
        task_id="process_data",
		python_callable= data_process # 실행 시킬 함수
    )
    
    # 3. 데이터 DB에 저장 
    
    DB_data = PythonOperator(
        task_id="DB_data",
		python_callable= data_DB # 실행 시킬 함수
    )

## 파이프라인화 하기 
load_data >>  process_data >> DB_data