import pika
import numpy as np
import json
from sklearn.datasets import load_diabetes
import time
from datetime import datetime

# Загружаем датасет о диабете
X, y = load_diabetes(return_X_y=True)

# Подключение к серверу на локальном хосте:
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Создаём очередь y_true
channel.queue_declare(queue='y_true')
# Создаём очередь features
channel.queue_declare(queue='features')

try:
    while True:
        # Формируем случайный индекс строки
        random_row = np.random.randint(0, X.shape[0]-1)
        
        # Генерируем уникальный идентификатор на основе timestamp
        message_id = datetime.timestamp(datetime.now())
        
        # Формируем сообщения в виде словарей
        message_y_true = {
            'id': message_id,
            'body': float(y[random_row])  # Преобразуем в float для корректной сериализации
        }
        
        message_features = {
            'id': message_id,
            'body': list(X[random_row])  # Преобразуем в list для корректной сериализации
        }

        # Публикуем сообщение в очередь y_true
        channel.basic_publish(
            exchange='',
            routing_key='y_true',
            body=json.dumps(message_y_true)
        )
        print(f'Сообщение с правильным ответом отправлено в очередь (ID: {message_id})')

        # Публикуем сообщение в очередь features
        channel.basic_publish(
            exchange='',
            routing_key='features',
            body=json.dumps(message_features)
        )
        print(f'Сообщение с вектором признаков отправлено в очередь (ID: {message_id})')
        
        # Добавляем задержку в 10 секунд
        time.sleep(10)

except KeyboardInterrupt:
    print("\nПрограмма остановлена пользователем")
finally:
    # Закрываем подключение при выходе
    connection.close()