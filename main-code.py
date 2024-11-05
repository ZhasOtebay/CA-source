import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Создаем папку output, если она не существует
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)
print(f"Папка '{output_dir}' готова.")

# Шаг 1: Ввод исходной матрицы X[n×m]
source_path = os.path.join('source', 'data.csv')  # Укажите имя файла
try:
    X = pd.read_csv(source_path, encoding='ISO-8859-1')
    print("Исходная матрица X загружена.")
except Exception as e:
    print(f"Ошибка при загрузке файла: {e}")
    exit()

# Задаем новые имена колонок
X.columns = ['Column991', 'Column992', 'Column993']  # Укажите новые имена при необходимости

# Печать исходной матрицы
n, m = X.shape
print("Исходная матрица X:\n", X)

# Шаг 2: Нормирование исходной матрицы
Y = (X - X.mean()) / X.std(ddof=0)  # Используем ddof=0 для популяционной дисперсии
print("Нормированная матрица Y:\n", Y)

# Шаг 3: Вычисление матрицы коэффициентов корреляции
R = Y.corr()
print("Матрица коэффициентов корреляции R:\n", R)

# Визуализация хитмапа корреляционной матрицы
plt.figure(figsize=(10, 8))
sns.heatmap(R, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar_kws={"shrink": .8})
plt.title("Хитмап матрицы коэффициентов корреляции")
plt.show()

# Шаг 4: Вычисление собственных значений и собственных векторов
eigenvalues, eigenvectors = np.linalg.eig(R.values)  # Используем значения numpy массива
print("Собственные значения:\n", eigenvalues)
print("Собственные векторы:\n", eigenvectors)

# Шаг 5: Формирование матриц собственных значений и собственных векторов
D = np.diag(eigenvalues)
print("Матрица собственных значений D:\n", D)

# Упорядочение собственных значений и векторов
indices = np.argsort(eigenvalues)[::-1]
sorted_eigenvalues = eigenvalues[indices]
sorted_eigenvectors = eigenvectors[:, indices]

print("Упорядоченные собственные значения:\n", sorted_eigenvalues)
print("Упорядоченные собственные векторы:\n", sorted_eigenvectors)

# Шаг 6: Вычисление матрицы нагрузок главных компонент
q = np.sum(sorted_eigenvalues > 1)  # Выбор компонентов с собственными значениями > 1
if q == 0:
    print("Нет собственных значений больше 1.")
    q = 1  # Устанавливаем q=1 для минимизации ошибок, но это нужно учитывать в дальнейшем анализе
A = sorted_eigenvectors[:, :q] * np.sqrt(sorted_eigenvalues[indices[:q]])

print("Матрица нагрузок главных компонент A:\n", A)

# Шаг 7: Вычисление значений главных компонент
F = Y.values @ A  # Убираем инверсию, если A уже нормирован

print("Матрица значений главных компонент F:\n", F)

# Шаг 8: Визуализация облака точек главных компонент
plt.figure(figsize=(10, 6))
plt.scatter(F[:, 0], F[:, 1], marker='o')


# Добавление номеров объектов
for i in range(n):
    plt.annotate(i, (F[i, 0], F[i, 1]), fontsize=9)

plt.title("Облако точек главных компонент")
plt.xlabel("ГК1")
plt.ylabel("ГК2")
plt.grid()
plt.show()

# Шаг 9: Проверка точности
Y_vosst = F @ A.T  # Убираем инверсию здесь, если необходимо

# Визуальное сравнение
comparison = pd.DataFrame({
    'Исходные значения': Y.values.flatten(),
    'Восстановленные значения': Y_vosst.flatten()
})
print("Сравнение восстановленных и исходных значений:\n", comparison)

# Проверяем количество главных компонент
q = min(F.shape[1], A.shape[1], X.shape[1])

# Шаг 10: Перевод восстановленных данных в исходные единицы
restored_X = (F @ A.T) * X.std(axis=0).values + X.mean(axis=0).values  # Используем .values для явного преобразования в массивы
print("Восстановленные значения в исходных единицах:\n", restored_X)

# Форматируем дату и время для имени файла
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

# Сохранение результатов в Excel
output_file = os.path.join(output_dir, f'результаты_компонентного_анализа_{current_time}.xlsx')
try:
    with pd.ExcelWriter(output_file) as writer:
        X.to_excel(writer, sheet_name='Исходные данные')
        Y.to_excel(writer, sheet_name='Нормированные данные')
        pd.DataFrame(R).to_excel(writer, sheet_name='Корреляционная матрица')
        pd.DataFrame(D).to_excel(writer, sheet_name='Собственные значения')
        pd.DataFrame(A).to_excel(writer, sheet_name='Матрица нагрузок')
        pd.DataFrame(F).to_excel(writer, sheet_name='Значения ГК')
        pd.DataFrame(restored_X).to_excel(writer, sheet_name='Восстановленные данные')
    print(f"Результаты сохранены в файл: {output_file}")
except Exception as e:
    print(f"Ошибка при сохранении файла: {e}")
