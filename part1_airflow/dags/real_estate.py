# dags/real_estate.py

import pendulum
from airflow.decorators import dag, task
from telegram_informer.messages import send_telegram_success_message, send_telegram_failure_message

@dag(
    schedule='@once',
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    on_success_callback=send_telegram_success_message,
    on_failure_callback=send_telegram_failure_message,
    tags=["ETL"]
)
def prepare_real_estate_dataset():
    import pandas as pd
    from airflow.providers.postgres.hooks.postgres import PostgresHook

    @task()
    def create_table():
        from sqlalchemy import Table, MetaData, Column, Integer, Float, BigInteger, Boolean, UniqueConstraint, inspect # дополните импорты необходимых типов колонок

        hook = PostgresHook('destination_db')
        conn = hook.get_sqlalchemy_engine()
        metadata = MetaData()
        real_estate_table = Table(
            'real_estate',
            metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('flat_id', Integer),
            Column('floor', Integer),
            Column('is_apartment', Boolean),
            Column('kitchen_area', Float),
            Column('living_area', Float),
            Column('rooms', Integer),
            Column('studio', Boolean),
            Column('total_area', Float),
            Column('price', BigInteger),
            Column('building_id', Integer),
            Column('build_year', Integer),
            Column('building_type_int', Integer),
            Column('latitude', Float),
            Column('longitude', Float),
            Column('ceiling_height', Float),
            Column('flats_count', Integer),
            Column('floors_total', Integer),
            Column('has_elevator', Boolean),
            UniqueConstraint('flat_id', name='unique_flat_constraint')
            )
        
        if not inspect(conn).has_table(real_estate_table.name): 
            metadata.create_all(conn)

    @task()
    def extract(**kwargs):

        hook = PostgresHook('destination_db')
        conn = hook.get_conn()
        sql = f"""
            SELECT
                f.id AS flat_id,                 
                f.floor,              
                f.is_apartment,       
                f.kitchen_area,       
                f.living_area,        
                f.rooms,              
                f.studio,             
                f.total_area,         
                f.price,              
                f.building_id,          
                b.build_year,         
                b.building_type_int,  
                b.latitude,           
                b.longitude,          
                b.ceiling_height,     
                b.flats_count,        
                b.floors_total,       
                b.has_elevator   
            FROM flats AS f
            LEFT JOIN buildings AS b
            ON b.id = f.building_id
        """
        data = pd.read_sql(sql, conn)
        conn.close()
        return data

    @task()
    def transform(data: pd.DataFrame):
        """
        # здесь можно было бы преобразовать Boolean в SmallInt, но я оставил этот шаг до подготовки датасета 
        к загрузке в модель (для удобства фильтрации столбцов по типу данных)

        data['is_apartment'] = data['is_apartment'].astype(int)
        data['studio'] = data['studio'].astype(int)
        data['has_elevator'] = data['has_elevator'].astype(int)
        """ 
        return data

    @task()
    def load(data: pd.DataFrame):
        hook = PostgresHook('destination_db')
        hook.insert_rows(
            table="real_estate",
            replace=True,
            target_fields=data.columns.tolist(),
            replace_index=['flat_id'],
            rows=data.values.tolist()
    )

    # ваш код здесь #
    create_table()
    data = extract()
    transformed_data = transform(data)
    load(transformed_data)
prepare_real_estate_dataset()