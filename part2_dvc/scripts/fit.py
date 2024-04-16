# scripts/fit.py

import os
import yaml
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder


# обучение модели
def fit_model():
    # Подгружаем гиперпараметры и другие настройки:
    with open('params.yaml', 'r') as fd:
         params = yaml.safe_load(fd)
        
    data = pd.read_csv('data/initial_data.csv')

    # разделяем столбцы по типам данных. Категориальные задаются вручную в params.yaml, так как из типов данных неясно, какие признаки категориальные
    col_types = data.dtypes
    binary_cols = col_types[col_types == 'bool'].index.tolist()
    num_cols = col_types[(col_types == 'int64') | (col_types == 'float64')].index.tolist()
    # убираем лишние и категориальные столбцы из числовых, также убираем целевой признак:  
    num_cols = list(
        set(num_cols)
        - set(params['cat_cols'])
        - set(params['drop_cols'])
        - set([params['target_col']])
    )

   # Создаём пайплан из процессов предобработки данных и обучения модели:
    preprocessor = ColumnTransformer(
        [
            ('binary', OneHotEncoder(drop=params['one_hot_drop']['binary']), binary_cols),
            ('cat', OneHotEncoder(drop=params['one_hot_drop']['categorical']), params['cat_cols']),
            ('num', StandardScaler(), num_cols)
        ],
        remainder='drop',
        verbose_feature_names_out=False
    )

    model = LinearRegression()

    pipeline = Pipeline(
        [
            ('preprocessor', preprocessor),
            ('model', model)
        ]
    )
    pipeline.fit(data, data[params['target_col']])

	#  Сохраняем обученную модель в models/fitted_model.pkl
    os.makedirs('models', exist_ok=True) # создание директории, если её ещё нет
    with open('models/fitted_model.pkl', 'wb') as fd:
        joblib.dump(pipeline, fd) 

if __name__ == '__main__':
	fit_model()