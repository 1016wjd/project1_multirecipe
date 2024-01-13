from flask import Flask, request, jsonify
import os
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D, Dropout, Dense, Input, Flatten

from tensorflow.keras.applications import ResNet50V2
import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
import cv2
import numpy as np
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine

def create_model():
  IMAGE_SIZE = 224

  input = Input(shape=(IMAGE_SIZE, IMAGE_SIZE, 3))

  # 전이학습 (Transfer Learning)
  base_model = ResNet50V2( input_tensor=input, include_top = False, weights='imagenet' )

  # Get Trained ResNet Feature Extraction Output Tensor
  bm_output = base_model.output

  # Customize Food Model
  x = GlobalAveragePooling2D()(bm_output) # Flatten

  # FCL
  x = Dense(128, activation='relu')(x)
  x = Dense(64, activation='relu')(x)

  # Output Layer
  output = Dense(40, activation='softmax')(x)

  model = Model(inputs=input, outputs=output)
  adam = Adam(0.0001)

  model.compile(
      optimizer=adam,
      loss='categorical_crossentropy',
      metrics=['acc']
  )

  return model

app = Flask(__name__)

@app.route('/cnn_classify', methods=['POST'])
def cnn_classfiy():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})
    
    
    # print(request.files)
    # print(request.files['image'])
    image_file = request.files['image']
    filename = os.path.join('uploads', image_file.filename)
    image_file.save(filename)
    
    
    
    model_loaded = create_model()
    model_loaded.load_weights('model/model_18-0.89.hdf5')
    
    categories = ["감바스", "김치전","김치찌개", "달걀말이","닭갈비", "돈까스", "동그랑땡", "된장국", "떡볶이", "라따뚜이", "리조또", "라멘", "라면","마제소바", "막국수", "멘보샤", "미역국","불고기", "사케동", "샐러드", "수제비","스테이크", "쌀국수", "야끼소바", "어묵볶음", "오코노미야키","월남쌈", "잔치국수", "짜글이", "짜장밥", "추어탕", "치즈등갈비", "칠리새우", "카레", "타코야키","탕수육", "탕후루","파스타", "피자", "허니브레드"]
    IMAGE_SIZE = 224
    image = cv2.imread(filename)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_224_224 = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE))
    img_tensor = image_224_224[np.newaxis, ...] / 255.0
    result = model_loaded.predict(img_tensor)
    result_idx = np.argsort(result, axis=1)[0, ::-1][:5]
    result = []
    for idx in result_idx:
        result.append(categories[idx])
        
    
    
    print({'result': result})
    
    
    return jsonify({'result': result})


@app.route('/cnn_post_create', methods=['POST'])
def cnn_post_create():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})
    
    
    # print(request.files)
    # print(request.files['image'])
    image_file = request.files['image']
    filename = os.path.join('uploads', image_file.filename)
    image_file.save(filename)
    
    model_loaded = create_model()
    model_loaded.load_weights('model/model_18-0.89.hdf5')
    
    categories = ["감바스", "김치전","김치찌개", "달걀말이","닭갈비", "돈까스", "동그랑땡", "된장국", "떡볶이", "라따뚜이", "리조또", "라멘", "라면","마제소바", "막국수", "멘보샤", "미역국","불고기", "사케동", "샐러드", "수제비","스테이크", "쌀국수", "야끼소바", "어묵볶음", "오코노미야키","월남쌈", "잔치국수", "짜글이", "짜장밥", "추어탕", "치즈등갈비", "칠리새우", "카레", "타코야키","탕수육", "탕후루","파스타", "피자", "허니브레드"]
    IMAGE_SIZE = 224
    image = cv2.imread(filename)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_224_224 = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE))
    img_tensor = image_224_224[np.newaxis, ...] / 255.0
    result = model_loaded.predict(img_tensor)
    result_idx = np.argsort(result, axis=1)[0, ::-1][:5]
    keyword = categories[result_idx[0]]
    
    username = "보안상삭제"
    password = "보안상삭제"
    host = "보안상삭제"
    database_name = "보안상삭제"

    db_connection_str = f'mysql+pymysql://{username}:{password}@{host}/{database_name}'
    db_connection = create_engine(db_connection_str)
    
    query = '''
    SELECT *
    FROM recipe_db.posts_rating;
    '''
    r_df = pd.read_sql(query, con=db_connection)
    # 'id'와 'user_id' 열 제거
    r_df.drop(['id', 'user_id'], axis=1, inplace=True)
    
    # 'post_id' 열을 기준으로 데이터프레임 정렬
    r_df.sort_values(by='post_id', inplace=True)
    # 'post_id'별 'score'의 합과 개수 계산
    post_id_summary = r_df.groupby('post_id')['score'].agg(['sum', 'count']).reset_index()
    
    # 'score'의 합을 'count'로 나누어 평균 계산
    post_id_summary['mean'] = post_id_summary['sum'] / post_id_summary['count']
    
    # 새로운 데이터프레임 생성
    mean_df = post_id_summary[['post_id', 'mean']]
    query2 = f'''
    SELECT id
    FROM recipe_db.posts_post
    WHERE INSTR(title, '{keyword}') > 0;
    '''
    e_df = pd.read_sql(query2, con=db_connection)
    id_list = e_df['id'].tolist()
    # id_list에 있는 각 post_id에 해당하는 평균값 추출
    id_means = mean_df[mean_df['post_id'].isin(id_list)]
    max_mean_post_id = id_means.loc[id_means['mean'].idxmax()]['post_id']

    query3 = '''
    SELECT C.ingred_name, A.post_id
    FROM recipe_db.posts_recipeingred A 
    LEFT JOIN recipe_db.posts_post B ON A.post_id = B.id
    LEFT JOIN recipe_db.posts_ingred C ON A.ingred_id = C.id;
    '''
    i_df = pd.read_sql(query3, con=db_connection)
    # post_id별 ingred_name 리스트로 모으기
    grouped_ingreds = i_df.groupby('post_id')['ingred_name'].apply(list).reset_index()
    result = grouped_ingreds[grouped_ingreds['post_id'] == max_mean_post_id]['ingred_name'].values[0]

    query4 = '''
    SELECT id, cate1, cate2, cate3
    FROM recipe_db.posts_post;
    '''
    cate_df = pd.read_sql(query4, con=db_connection)
    result2 = cate_df[cate_df['id'] == max_mean_post_id][['cate1', 'cate2', 'cate3']]
    result_list = result2.values.flatten().tolist()
    
    
    
    
        
    
    
    print({'ingred_create': result, 'cate_create': result_list})
    
    
    return jsonify({'ingred_create': result, 'cate_create': result_list})

if __name__ == '__main__':
    app.run('보안상삭제', port='보안상삭제', debug=True)