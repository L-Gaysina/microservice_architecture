import pika
import pickle
import numpy as np
import json

# Читаем файл с сериализованной моделью
with open('myfile.pkl', 'rb') as pkl_file:
    regressor = pickle.load(pkl_file)

try:
    # Создаём подключение по адресу rabbitmq:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Объявляем очереди
    channel.queue_declare(queue='features')
    channel.queue_declare(queue='y_pred')

    # Создаём функцию callback для обработки данных из очереди
    def callback(ch, method, properties, body):
        try:
            # Парсим входящее сообщение
            message = json.loads(body)
            message_id = message['id']
            features = message['body']
            
            print(f'Получен вектор признаков (ID: {message_id}): {features}')
            
            # Делаем предсказание
            pred = regressor.predict(np.array(features).reshape(1, -1))
            
            # Формируем сообщение с предсказанием
            prediction_message = {
                'id': message_id,
                'body': float(pred[0])  # Преобразуем в float для корректной сериализации
            }
            
            # Отправляем предсказание
            channel.basic_publish(
                exchange='',
                routing_key='y_pred',
                body=json.dumps(prediction_message)
            )
            
            print(f'Предсказание {pred[0]} отправлено в очередь y_pred (ID: {message_id})')
            
        except Exception as e:
            print(f'Ошибка при обработке сообщения: {e}')

    # Извлекаем сообщение из очереди features
    channel.basic_consume(
        queue='features',
        on_message_callback=callback,
        auto_ack=True
    )
    
    print('...Ожидание сообщений, для выхода нажмите CTRL+C')
    channel.start_consuming()
    
except KeyboardInterrupt:
    print("\nПрограмма остановлена пользователем")
except Exception as e:
    print(f'Не удалось подключиться к очереди: {e}')
finally:
    if 'connection' in locals() and connection.is_open:
        connection.close()