import pandas as pd
import os

# Папки для исходных и сохраненных файлов
input_folder = 'csvconvert'
output_folder = 'source'

# Убедимся, что выходная папка существует
os.makedirs(output_folder, exist_ok=True)

# Функция для переименования колонок
def rename_columns_to_latin(df):
    df.columns = [f'Column{i + 1}' for i in range(len(df.columns))]
    return df

# Обработка всех Excel файлов в папке
for filename in os.listdir(input_folder):
    if filename.endswith('.xlsx') or filename.endswith('.xls'):
        file_path = os.path.join(input_folder, filename)
        
        # Чтение Excel файла
        df = pd.read_excel(file_path)
        
        # Удаление пустых колонок
        df.dropna(axis=1, how='all', inplace=True)
        
        # Переименование колонок
        df = rename_columns_to_latin(df)
        
        # Сохранение в CSV
        output_file_path = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}.csv')
        df.to_csv(output_file_path, index=False, encoding='utf-8')
        
        print(f'Конвертирован: {filename} -> {os.path.basename(output_file_path)}')
