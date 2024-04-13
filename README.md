# Проект 1 спринта

Добро пожаловать в репозиторий-шаблон Практикума для проекта 1 спринта. Цель проекта — создать базовое решение для предсказания стоимости квартир Яндекс Недвижимости.

Полное описание проекта хранится в уроке «Проект. Разработка пайплайнов подготовки данных и обучения модели» на учебной платформе.

Здесь укажите имя вашего бакета:<br> 
**s3-student-mle-20240325-312c609c6b**

## Файлы проекта:

### EDA и проверка функций очистки данных:
[view_data.ipynb](part1_airflow/notebooks/view_data.ipynb)<br>

### DAGS:
[Создание первичной таблицы](part1_airflow/dags/real_estate.py)<br>
[Создание очищенной таблицы](part1_airflow/dags/clean_real_estate.py)<br>

**Функции подготовки данных:**<br>
[functions.ipynb](part1_airflow/notebooks/functions.ipynb)<br>

**fill_missing_values()** заполняет пустые значения;<br>
**remove_duplicates()** убирает дубликаты;<br>
**remove_outliers()** убирает выбросы;<br>

### DVC:
Команда ля запуска DVC из корневого каталога:
```
$ dvc repro part2_dvc/dvc.yaml
```

[Jupyter Notebook с тестированием базовой модели](part2_dvc/notebooks/run_regression.ipynb)

**Файлы с этапами и параметрами:**<br>
[dvc.yaml](part2_dvc/dvc.yaml)<br>
[params.yaml](part2_dvc/params.yaml)<br>
[dvc.lock](part2_dvc/dvc.lock)<br>

**Этапы DVC:**<br>
[1. Загрузка данных](part2_dvc/scripts/data.py)<br>
[2. Настройка модели](part2_dvc/scripts/fit.py)<br>
[3. Оценка модели](part2_dvc/scripts/evaluate.py)<br>

