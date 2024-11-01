import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import time
import numpy as np
from datetime import datetime

def plot_error_distribution(csv_path, plot_path):
    """
    Читает данные из CSV и создает гистограмму распределения ошибок
    """
    try:
        # Читаем данные из CSV
        df = pd.read_csv(csv_path)
        
        # Настраиваем стиль
        plt.style.use('bmh')  
        
        # Настраиваем общий вид графиков seaborn
        sns.set_theme(style="whitegrid")
        
        # Создаем фигуру 
        plt.figure(figsize=(14, 8))
        
        # Создаем основной график
        ax = plt.gca()
        
        # Строим гистограмму 
        sns.histplot(
            data=df,
            x='absolute_error',
            bins=15,
            color='#4FB6C9',  
            alpha=0.6,
            stat='count',
            edgecolor='white',
            linewidth=1
        )
        
        # Добавляем кривую плотности распределения
        sns.kdeplot(
            data=df,
            x='absolute_error',
            color='#2E5266',  # Темно-синий цвет
            linewidth=2,
            label='Density'
        )
        
        # Добавляем статистические показатели
        mean_error = df['absolute_error'].mean()
        median_error = df['absolute_error'].median()
        std_error = df['absolute_error'].std()
        
        # Добавляем вертикальные линии для среднего и медианы
        plt.axvline(mean_error, color='#D64933', linestyle='--', linewidth=2, label=f'Mean: {mean_error:.2f}')
        plt.axvline(median_error, color='#437F97', linestyle='--', linewidth=2, label=f'Median: {median_error:.2f}')
        
        # Настраиваем внешний вид
        plt.title('Distribution of Absolute Errors in Model Predictions', 
                 fontsize=16, 
                 pad=20)
        plt.xlabel('Absolute Error', fontsize=12, labelpad=10)
        plt.ylabel('Number of Predictions', fontsize=12, labelpad=10)
        
        # Добавляем аннотации со статистикой
        stats_text = (f'Statistics:\n'
                     f'Mean: {mean_error:.2f}\n'
                     f'Median: {median_error:.2f}\n'
                     f'Std Dev: {std_error:.2f}\n'
                     f'Sample Size: {len(df)}')
        
        # Добавляем текстовое поле со статистикой

        plt.text(0.99, 0.99, stats_text,
                transform=ax.transAxes,
                verticalalignment='top',
                horizontalalignment='right',
                bbox=dict(boxstyle='round,pad=0.5',
                         facecolor='white',
                         alpha=0.9))
        
        # Настраиваем легенду - размещаем её справа от графика
        plt.legend(bbox_to_anchor=(1.02, 0.5),
                  loc='center left',
                  fontsize=10,
                  frameon=True,
                  facecolor='white',
                  edgecolor='none',
                  bbox_transform=ax.transAxes)
        
        # Устанавливаем отступы
        plt.tight_layout()
        
        # Добавляем временную метку
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        plt.figtext(0.02, 0.02, f'Generated: {timestamp}', 
                   fontsize=8, alpha=0.7)
        
        # Сохраняем график
        plt.savefig(plot_path, 
                   dpi=200, 
                   bbox_inches='tight',
                   facecolor='white',
                   edgecolor='none')
        plt.close()
        
        print(f"График успешно обновлен: {plot_path} в {timestamp}")
        
    except Exception as e:
        print(f"Ошибка при создании графика: {e}")

def main():
    # Пути к файлам
    csv_path = './logs/metric_log.csv' 
    plot_path = './logs/error_distribution.png'
    
    # Создаем директорию logs если её нет
    Path('./logs').mkdir(parents=True, exist_ok=True)
    
    print("Запуск сервиса построения графиков...")
    
    while True:
        try:
            if Path(csv_path).exists() and Path(csv_path).stat().st_size > 0:
                plot_error_distribution(csv_path, plot_path)
            else:
                print(f"Файл {csv_path} не найден или пуст, ожидание...")
            
            # Пауза перед следующим обновлением
            time.sleep(10)
            
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()