# dags/clean_real_estate.py

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

def clean_real_estate_dataset():
    import pandas as pd
    from airflow.providers.postgres.hooks.postgres import PostgresHook

    def remove_duplicates(data):
        feature_cols = data.columns.drop('flat_id').tolist()
        is_duplicated_features = data.duplicated(subset=feature_cols, keep='first')
        data = data[~is_duplicated_features].reset_index(drop=True)
        return data
    
    def fill_missing_values(data):
        cols_with_nans = data.isnull().sum()
        cols_with_nans = cols_with_nans[cols_with_nans > 0].index

        if len(cols_with_nans) != 0:
            for col in cols_with_nans:
                if data[col].dtype in [float, int]:
                    fill_value = data[col].mean()
                elif data[col].dtype == 'object':
                    fill_value = data[col].mode().iloc[0]
                data[col] = data[col].fillna(fill_value)

        return data
    
    def remove_outliers(data):
        num_cols = data.select_dtypes(['float', 'int']).columns
        threshold = 1.5
        potential_outliers = pd.DataFrame()

        for col in num_cols:
            Q1 = data[col].quantile(q=0.25, interpolation='linear')
            Q3 = data[col].quantile(q=0.75, interpolation='linear')
            IQR = Q3 - Q1 
            margin = threshold*IQR
            lower = Q1 - margin
            upper = Q3 + margin
            potential_outliers[col] = ~data[col].between(lower, upper)

        outliers = potential_outliers.any(axis=1)
        return data.loc[~outliers, :]

    @task()
    def create_table():
        from sqlalchemy import Table, MetaData, Column, Integer, Float, BigInteger, Boolean, UniqueConstraint, inspect # дополните импорты необходимых типов колонок

        hook = PostgresHook('destination_db')
        conn = hook.get_sqlalchemy_engine()
        metadata = MetaData()
        real_estate_table = Table(
            'real_estate_clean',
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
            UniqueConstraint('flat_id', name='unique_flat_constraint_clean')
            )
        
        if not inspect(conn).has_table(real_estate_table.name): 
            metadata.create_all(conn)

    @task()
    def extract(**kwargs):

        hook = PostgresHook('destination_db')
        conn = hook.get_conn()
        sql = f"""
            SELECT
                flat_id,                 
                floor,              
                is_apartment,       
                kitchen_area,       
                living_area,        
                rooms,              
                studio,             
                total_area,         
                price,              
                building_id,          
                build_year,         
                building_type_int,  
                latitude,           
                longitude,          
                ceiling_height,     
                flats_count,        
                floors_total,       
                has_elevator   
            FROM real_estate
        """
        data = pd.read_sql(sql, conn)
        conn.close()
        return data

    @task()
    def transform(data: pd.DataFrame):
        data = remove_duplicates(data)
        data = fill_missing_values(data)
        data = remove_outliers(data)
        return data

    @task()
    def load(data: pd.DataFrame):
        hook = PostgresHook('destination_db')
        hook.insert_rows(
            table="real_estate_clean",
            replace=True,
            target_fields=data.columns.tolist(),
            replace_index=['flat_id'],
            rows=data.values.tolist()
    )

    create_table()
    data = extract()
    transformed_data = transform(data)
    load(transformed_data)
clean_real_estate_dataset()