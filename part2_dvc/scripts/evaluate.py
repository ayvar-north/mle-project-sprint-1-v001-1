# scripts/evaluate.py
import os
import yaml
import json
import joblib
import pandas as pd

from sklearn.model_selection import cross_validate

# оценка качества модели
def evaluate_model():
	# прочитайте файл с гиперпараметрами params.yaml
    with open('params.yaml', 'r') as fd:
        params = yaml.safe_load(fd)
    target_col = params['target_col']
    n_splits = params['n_splits']
    metrics = params['metrics']
    n_jobs = params['n_jobs']

	# загрузите результат прошлого шага: fitted_model.pkl
    with open('models/fitted_model.pkl', 'rb') as fd:
        model = joblib.load(fd)
   
    data = pd.read_csv('data/initial_data.csv')
    
	# реализуйте основную логику шага с использованием прочтённых гиперпараметров
    cv_res = cross_validate(
        model,
        data,
        data[target_col],
        cv=n_splits,
        n_jobs=n_jobs,
        scoring=metrics
        )
    
    for key, value in cv_res.items():
        cv_res[key] = round(value.mean(), 3) 
        
	# сохраните результата кросс-валидации в cv_res.json
    json_object = json.dumps(cv_res)
    os.makedirs('cv_results', exist_ok=True)
    with open('cv_results/cv_res.json', "w") as fres:
        fres.write(json_object)

if __name__ == '__main__':
	evaluate_model()