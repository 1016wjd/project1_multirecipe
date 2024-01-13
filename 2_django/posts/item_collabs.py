import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import os
from sqlalchemy import create_engine

def load_user_recom2(user_id):
    ## sql에서 데이터 받아오기
    db_connection_str = '보안상삭제'
    db_connection = create_engine(db_connection_str)
    query_rating = '''
    SELECT *
    FROM recipe_db.rating_matrix;
    '''
    query_rating_pred = '''
    SELECT *
    FROM recipe_db.rating_pred_matrix;
    '''
    
    r_df = pd.read_sql(query_rating, con=db_connection, index_col='user_id')
    m_df = pd.read_sql(query_rating_pred, con=db_connection, index_col='user_id')
    m_df.fillna(0, inplace=True)

    if user_id not in m_df.index:
        return '별점 없음'  # 사용자 ID가 존재하지 않으면 '별점 없음' 반환

    user_rating = m_df.loc[user_id, :]

    # user_rating=0인 아직 안 본 레시피
    unseen_recipe_list = user_rating[user_rating == 0].index.tolist()

    # 모든 레시피를 list 객체로 만든다.
    recipes_list = m_df.columns.tolist()

    # 안 본 레시피 리스트 생성
    unseen_list = [recipe for recipe in recipes_list if recipe in unseen_recipe_list]
    top_n = 4
    recomm_recipes = r_df.loc[user_id, unseen_list].sort_values(ascending=False)[:top_n]
    recomm_recipes_list = list(map(int, recomm_recipes.index.tolist()))

    return recomm_recipes_list
