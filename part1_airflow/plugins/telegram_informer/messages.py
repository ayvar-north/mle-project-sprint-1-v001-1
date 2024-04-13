# plugins/steps/messages.py
import os
from dotenv import load_dotenv
from airflow.providers.telegram.hooks.telegram import TelegramHook


def send_telegram_success_message(context): # на вход принимаем словарь со контекстными переменными
    
    #Получаем Telegram credentials:
    load_dotenv()
    telegram_conn_id = os.getenv('TG_CONN_ID')
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    hook = TelegramHook(telegram_conn_id=telegram_conn_id,
                        token=token,
                        chat_id=chat_id)
    
    dag = context['dag']
    run_id = context['run_id']

    message = f'Исполнение DAG {dag} с id={run_id} прошло успешно!' # определение текста сообщения
    hook.send_message({
        'chat_id': chat_id,
        'text': message,
        'parse_mode': None
    }) # отправление сообщения 

def send_telegram_failure_message(context):

    #Получаем Telegram credentials:
    load_dotenv()
    telegram_conn_id = os.getenv('TG_CONN_ID')
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    hook = TelegramHook(telegram_conn_id=telegram_conn_id,
                        token=token,
                        chat_id=chat_id)
    
    run_id = context['run_id']
    task_instance_key_str = context['task_instance_key_str']
    
    message = f'WARNING: Не удалось запустить исполнение DAG {task_instance_key_str} с id={run_id}!' # определение текста сообщения
    hook.send_message({
        'chat_id': chat_id,
        'text': message
    }) # отправление сообщения 