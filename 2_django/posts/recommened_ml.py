import pandas as pd 
import warnings; warnings.filterwarnings('ignore')
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv('./posts/data/cate_clean.csv')

data = df['cate'].tolist()

tfidf = TfidfVectorizer()
cnt_vect = CountVectorizer()
cnt_vectors = cnt_vect.fit_transform(data).toarray()
base_data = cnt_vectors


# 추천함수 
def recommend_recipe(cate):
    food_choice = {
    '제육볶음': ['한식', '일상', '돼지고기'],
    '닭도리탕': ['한식', '술안주', '닭고기'],
    '된장찌개': ['한식', '원팬스피디', '콩견과류'],
    '비빔밥': ['한식', '다이어트', '채소'],
    '치킨커리': ['기타식', '일상', '닭고기'],
    '쌀국수': ['기타식', '일상', '면류'],
    '마라탕': ['기타식', '술안주', '채소'],
    '토마토파스타': ['양식', '원팬스피디', '면류'],
    '스테이크': ['양식', '일상', '소고기'],
    '초밥': ['일식', '일상', '해물'],
    }

    food_catelist = []
    for food in cate:
        food_catelist += food_choice[food]
        
    selected_category_vector = np.zeros(base_data.shape[1])
        
    for term in food_catelist:
        idx = cnt_vect.vocabulary_[term]
        selected_category_vector[idx] = (23 / np.exp(tfidf.idf_))[idx]
    
    sims = cosine_similarity(base_data, selected_category_vector.reshape(1, -1))
    recommended_index = sims.flatten().argsort()[::-1]
    
    return(recommended_index)


# print(recommend_recipe({'제육볶음', '초밥', '쌀국수'}))
# 제육볶음 치킨커리 쌀국수