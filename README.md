# microservice_architecture
Система мониторинга ML модели с использованием микросервисной архитектуры. Проект реализует распределенную систему для оценки качества модели машинного обучения в режиме реального времени с использованием Docker и RabbitMQ.

## Структура проекта
```
MICROSERVICE_ARCHITECTURE/
├── docker-compose.yml        # Конфигурация Docker Compose
├── README.md                 # Документация проекта
├── features/                 # Сервис генерации признаков
│   ├── src/
│   │   └── features.py       # Генерация и отправка данных
│   ├── Dockerfile          
│   └── requirements.txt     
├── model/                    # Сервис ML модели
│   ├── src/
│   │   ├── model.py          # Обработка и предсказания
│   │   └── myfile.pkl        # Сохраненная модель
│   ├── Dockerfile
│   └── requirements.txt
├── metric/                   # Сервис расчета метрик
│   ├── src/
│   │   └── metric.py         # Расчет и сохранение метрик
│   ├── Dockerfile
│   └── requirements.txt
├── plot/                     # Сервис визуализации
│   ├── src/
│   │   └── plot.py           # Генерация визуализаций
│   ├── Dockerfile
│   └── requirements.txt
└── logs/                     # Директория для логов и результатов
    ├── error_distribution.png
    └── metric_log.csv
```
## Описание сервисов
### Features Service

* Генерирует тестовые данные из датасета о диабете
* Отправляет вектор признаков в очередь 'features'
* Отправляет истинные значения в очередь 'y_true'
* Каждому сообщению присваивается уникальный ID

### Model Service

* Получает векторы признаков из очереди 'features'
* Использует предобученную модель для предсказаний
* Отправляет результаты в очередь 'y_pred'
* Сохраняет идентификатор сообщения

### Metric Service

* Получает истинные значения из очереди 'y_true'
* Получает предсказания из очереди 'y_pred'
* Сопоставляет данные по ID
* Рассчитывает метрики качества
* Сохраняет результаты в CSV файл

### Plot Service

* Читает метрики из CSV файла
* Генерирует визуализации распределения ошибок
* Обновляет графики в реальном времени
* Сохраняет результаты в PNG файл


## Требования

* Docker
* Docker Compose
* Python 3.8+
* Свободный порт 5672 (RabbitMQ)
* Свободный порт 15672 (RabbitMQ Management)

## Установка и запуск
1. Клонируйте репозиторий:
```bash
git clone https://github.com/L-Gaysina/microservice_architecture
```
```bash
cd microservice_architecture  
```
2. Запустите систему с помощью Docker Compose:

```bash
docker-compose up --build
```
### Мониторинг

RabbitMQ Management UI:

* URL: http://localhost:15672
* Login: guest
* Password: guest

### Просмотр логов:

```bash
docker-compose logs -f
```
### Метрики и визуализации:

* CSV файл с метриками: ./logs/metric_log.csv
* График распределения ошибок: ./logs/error_distribution.png

### Остановка всех сервисов
```bash
docker-compose down
```

### Если контейнеры не запускаются
```
# Остановка и удаление всех контейнеров
docker-compose down

# Удаление всех образов
docker-compose down --rmi all

# Очистка volumes
docker-compose down -v

# Перезапуск
docker-compose up --build
 ``` 
