import json
import pandas as pd 
from sqlalchemy import create_engine
import warnings; warnings.filterwarnings('ignore')

import json
import pandas as pd

def time_recommend(file_path, now):
    
    ## 실시간으로 데이터 불러와서 분석하도록 
    json_data_list = []

    with open(file_path, 'r') as json_file:
        for line in json_file:
            json_data = json.loads(line)
            json_data_list.append(json_data)

    df = pd.DataFrame(json_data_list)
    df = df[(df['postid'] <= 200) | (pd.to_datetime(df['asctime']) >= '2023-12-30')]
    ## 시간대 정보 생성
    df.asctime = pd.to_datetime(df.asctime)
    def assign_time_label(x):
        if 5 <= x < 10:
            return '아침'
        elif 10 <= x < 16:
            return '점심'
        elif 16 <= x < 23:
            return '저녁'
        else:
            return '새벽'

    df['time'] = df['asctime'].dt.hour.apply(assign_time_label)
    # print(df['time'])
    target = df[df.modulename == 'detail'][['asctime','time', 'postid']]
    recommended_index = target[target.time == now].postid.value_counts().index
    return recommended_index

def user_recommend2(age, sex):
    
    ## sql에서 데이터 받아오기
    db_connection_str = '보안상삭제'
    db_connection = create_engine(db_connection_str)
    query = '''
    SELECT *
    FROM recipe_db.userlog_detail;
    '''
    target = pd.read_sql(query, con=db_connection)
    dtarget = target[target.postid <= 200]
    ## 나이대변수 생성
    recommended_index = target[(target.age_group == age) & (target.sex == sex)].postid.value_counts().index
    return recommended_index



