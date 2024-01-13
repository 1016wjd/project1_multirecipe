import pandas as pd
from sqlalchemy import create_engine

# MySQL 연결 정보 설정
db_connection_str = '보안상삭제'
db_connection = create_engine(db_connection_str)

# CSV 파일 경로
csv_file_path = '/home/ubuntu/web/posts_ingred.csv'

# CSV 파일을 DataFrame으로 읽기
df = pd.read_csv(csv_file_path)

# DataFrame을 MySQL 테이블에 삽입
df.to_sql(name='posts_ingred', con=db_connection, if_exists='append', index=False)
