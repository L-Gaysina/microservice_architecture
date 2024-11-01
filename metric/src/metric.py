import pika
import json
import pandas as pd
from pathlib import Path

# Создаем папку logs если её нет
Path('./logs').mkdir(parents=True, exist_ok=True)

# Инициализируем CSV файл с заголовками если он не существует
if not Path('./logs/metric_log.csv').exists():
    with open('./logs/metric_log.csv', 'w') as f:
        f.write('id,y_true,y_pred,absolute_error\n')

# Создаем словари для хранения временных данных
y_true_dict = {}
y_pred_dict = {}

def calculate_and_log_metrics(message_id):
    """Вычисляет абсолютную ошибку и записывает результаты в CSV"""
    try:
        y_true = float(y_true_dict[message_id])
        y_pred = float(y_pred_dict[message_id])
        absolute_error = abs(y_true - y_pred)
        
        # Записываем метрики в CSV
        with open('./logs/metric_log.csv', 'a') as f:
            f.write(f"{message_id},{y_true},{y_pred},{absolute_error}\n")
            f.flush()  # Принудительно записываем буфер в файл
        
        # Логируем результат
        print(f"Записаны метрики для ID {message_id}:")
        print(f"y_true: {y_true}, y_pred: {y_pred}, absolute_error: {absolute_error}")
        
        # Удаляем обработанные данные из словарей
        del y_true_dict[message_id]
        del y_pred_dict[message_id]
        
    except Exception as e:
        print(f"Ошибка при записи метрик: {e}")

def process_message(ch, method, properties, body):
    """Обработка сообщений из очередей y_true и y_pred"""
    try:
        # Парсим сообщение
        message = json.loads(body)
        message_id = str(message['id'])  # Преобразуем id в строку для единообразия
        value = message['body']
        queue_name = method.routing_key
        
        # Логируем получение сообщения
        print(f"Получено сообщение из очереди {queue_name}: ID={message_id}, value={value}")
        
        # Сохраняем значение в соответствующий словарь
        if queue_name == 'y_true':
            y_true_dict[message_id] = value
        else:
            y_pred_dict[message_id] = value
        
        # Проверяем, есть ли парное значение
        if message_id in y_true_dict and message_id in y_pred_dict:
            calculate_and_log_metrics(message_id)
            
    except Exception as e:
        print(f"Ошибка при обработке сообщения: {e}")

try:
    # Подключаемся к RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    
    # Объявляем очереди
    channel.queue_declare(queue='y_true')
    channel.queue_declare(queue='y_pred')
    
    # Подписываемся на обе очереди
    channel.basic_consume(
        queue='y_true',
        on_message_callback=process_message,
        auto_ack=True
    )
    
    channel.basic_consume(
        queue='y_pred',
        on_message_callback=process_message,
        auto_ack=True
    )
    
    print('Ожидание сообщений... Для выхода нажмите CTRL+C')
    channel.start_consuming()
    
except KeyboardInterrupt:
    print("\nПрограмма остановлена пользователем")
except Exception as e:
    print(f"Ошибка: {e}")
finally:
    if 'connection' in locals() and connection.is_open:
        connection.close()