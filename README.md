# microservice_architecture
Система мониторинга ML модели с использованием микросервисной архитектуры. Проект демонстрирует работу распределенной системы для оценки качества модели машинного обучения в режиме реального времени.

## Структура




## Требования

* Docker
* Docker Compose
* Python 3.8+
* Свободный порт 5672 (RabbitMQ)
* Свободный порт 15672 (RabbitMQ Management)

### Установка и запуск
Клонируйте репозиторий:
```bash
git clone https://github.com/L-Gaysina/microservice_architecture
```
```bash
cd microservice_architecture  
```
Запустите систему с помощью Docker Compose:

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
  
