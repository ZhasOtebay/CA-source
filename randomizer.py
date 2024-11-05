import pandas as pd
import numpy as np
import os

# Данные для сохранения
data = [
    [5.209669, 3.64369528, 1.48810188],
    [5.41758753, 3.8928642, 1.47679846],
    [5.59950279, 4.11716823, 1.45928376],
    [5.06589295, 3.52059945, 1.43633999],
    [4.70609314, 3.14318607, 1.39079522],
    [4.91378649, 3.30015887, 1.49080998],
    [5.07399817, 3.52574808, 1.4414263],
    [4.81053654, 3.20280621, 1.46447963],
    [5.01964852, 3.41424261, 1.50053027],
    [4.77120389, 3.13933053, 1.48640216],
    [5.07399817, 3.52574808, 1.4414263],
    [4.77930911, 3.14447916, 1.49148846],
    [5.06589295, 3.52059945, 1.43633999],
    [4.81053654, 3.20280621, 1.46447963],
    [5.07399817, 3.52574808, 1.4414263],
    [4.99936357, 3.46999139, 1.40469718],
    [4.6517435, 3.0316806, 1.44989919],
    [5.209669, 3.64369528, 1.48810188],
    [5.14863276, 3.58150477, 1.47815542],
    [4.69107615, 3.09515628, 1.42797667],
    [5.06589295, 3.52059945, 1.43633999],
    [4.81053654, 3.20280621, 1.46447963],
    [5.07399817, 3.52574808, 1.4414263],
    [5.01964852, 3.41424261, 1.50053027],
    [4.70609314, 3.14318607, 1.39079522],
    [5.07399817, 3.52574808, 1.4414263],
    [4.7645173, 3.18864549, 1.41735173],
    [5.06589295, 3.52059945, 1.43633999],
    [4.81053654, 3.20280621, 1.46447963],
    [5.07399817, 3.52574808, 1.4414263],
    [5.34414638, 3.79937499, 1.48742339],
    [4.69107615, 3.09515628, 1.42797667],
    [5.06589295, 3.52059945, 1.43633999],
    [4.81053654, 3.20280621, 1.46447963],
    [5.07399817, 3.52574808, 1.4414263],
    [4.99936357, 3.46999139, 1.40469718],
    [4.6517435, 3.0316806, 1.44989919]
]

# Создание DataFrame
df = pd.DataFrame(data, columns=['Column1', 'Column2', 'Column3'])

# Указание пути к папке и имени файла
output_folder = 'csvconvert'
output_file = os.path.join(output_folder, 'random_data.csv')

# Создание папки, если она не существует
os.makedirs(output_folder, exist_ok=True)

# Сохранение DataFrame в CSV файл
df.to_csv(output_file, index=False)

print(f"Данные сохранены в файл: {output_file}")
