# Проект 1 спринта

Добро пожаловать в репозиторий-шаблон Практикума для проекта 1 спринта. Цель проекта — создать базовое решение для предсказания стоимости квартир Яндекс Недвижимости.

Полное описание проекта хранится в уроке «Проект. Разработка пайплайнов подготовки данных и обучения модели» на учебной платформе.

Здесь укажите имя вашего бакета: s3-student-mle-20240325-312c609c6b

EDA и проверка функций очистки данных:
    part1_airflow/notebooks/view_data.ipynb

DAGS:
    part1_airflow/dags/real_estate.py           - создание первичной таблицы;
    part1_airflow/dags/clean_real_estate.py     - создание очищенной таблицы;

Функции подготовки данных:
    fill_missing_values()   - заполняет пустые значения
    remove_duplicates()     - убирает дубликаты;
    remove_outliers()       - убирает выбросы;


DVC:
Команда ля запуска DVC из корневого каталога:
~/mle_projects/mle-project-sprint-1-v001$ dvc repro part2_dvc/dvc.yaml
Тетрадка с тестированием базовой модели: 
part2_dvc/notebooks/run_regression.ipynb

Файлы с этапами и параметрами:
part2_dvc/dvc.yaml
part2_dvc/params.yaml
part2_dvc/dvc.lock

Этапы DVC:
1. Загрузка данных:     part2_dvc/scripts/data.py
2. Настройка модели:    part2_dvc/scripts/fit.py
3. Оценка модели:       part2_dvc/scripts/evaluate.py

