import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from openpyxl import load_workbook
from openpyxl.drawing.image import Image

def plot_heatmap(data, title, filename):
    plt.figure(figsize=(10, 8))
    sns.heatmap(data, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar_kws={"shrink": .8})
    plt.title(title)
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

def plot_scatter(F, filename):
    plt.figure(figsize=(12, 8))
    noise = np.random.normal(0, 0.05, F.shape)  # Небольшое случайное смещение
    F_noisy = F + noise
    plt.scatter(F_noisy[:, 0], F_noisy[:, 1], marker='o', alpha=0.7)
    
    for i in range(len(F)):
        plt.annotate(i, (F_noisy[i, 0], F_noisy[i, 1]), fontsize=8, ha='center', va='center')

    plt.title("Облако точек главных компонент")
    plt.xlabel("ГК1")
    plt.ylabel("ГК2")
    plt.grid()
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

def run_analysis(source_path, num_columns):
    try:
        # Загрузка данных из CSV
        X = pd.read_csv(source_path, encoding='ISO-8859-1', header=None)

        # Установка названий колонок
        X.columns = [f'Column{i+1}' for i in range(num_columns)]
        X = X.apply(pd.to_numeric, errors='coerce')
        X.dropna(inplace=True)
        
        # Нормирование
        Y = (X - X.mean()) / X.std(ddof=0)
        R = Y.corr()
        heatmap_file = 'correlation_heatmap.png'
        plot_heatmap(R, "Матрица коэффициентов корреляции R", heatmap_file)

        # Собственные значения и векторы
        eigenvalues, eigenvectors = np.linalg.eig(R.values)
        D = np.diag(eigenvalues)

        # Упорядочение
        indices = np.argsort(eigenvalues)[::-1]
        sorted_eigenvalues = eigenvalues[indices]
        sorted_eigenvectors = eigenvectors[:, indices]

        q = np.sum(sorted_eigenvalues > 1) or 1
        A = sorted_eigenvectors[:, :q] * np.sqrt(sorted_eigenvalues[indices[:q]])
        F = Y.values @ A

        # Визуализация
        scatter_file = 'scatter_plot.png'
        plot_scatter(F, scatter_file)

        # Сохранение результатов
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join('output', f'результаты_компонентного_анализа_{current_time}.xlsx')
        
        with pd.ExcelWriter(output_file) as writer:
            X.to_excel(writer, sheet_name='Исходные данные')
            Y.to_excel(writer, sheet_name='Нормированные данные')
            pd.DataFrame(R).to_excel(writer, sheet_name='Корреляционная матрица')
            pd.DataFrame(D).to_excel(writer, sheet_name='Собственные значения')
            pd.DataFrame(A).to_excel(writer, sheet_name='Матрица нагрузок')
            pd.DataFrame(F).to_excel(writer, sheet_name='Значения ГК')

        # Вставка изображений в Excel
        wb = load_workbook(output_file)
        correlation_sheet = wb['Корреляционная матрица']
        img1 = Image(heatmap_file)
        correlation_sheet.add_image(img1, 'A10')

        scatter_sheet = wb['Значения ГК']
        img2 = Image(scatter_file)
        scatter_sheet.add_image(img2, 'A10')
        
        wb.save(output_file)

        messagebox.showinfo("Успех", f"Результаты сохранены в файл: {output_file}")
        
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def upload_file():
    source_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if source_path:
        num_columns = simpledialog.askinteger("Количество колонок", "Введите количество колонок:")
        if num_columns:
            run_analysis(source_path, num_columns)

def show_developer_info():
    messagebox.showinfo("Информация о разработчике", "Разработано: Zhas Otebay\nzhas.otebay@gmail.com\nhttps://github.com/ZhasOtebay/CA-source")

# Создание интерфейса
root = tk.Tk()
root.title("Анализ главных компонент")
root.geometry("400x300")
root.resizable(False, False)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

title_label = tk.Label(frame, text="Анализ главных компонент", font=("Helvetica", 16, "bold"))
title_label.pack(pady=(0, 20))

upload_button = tk.Button(frame, text="Загрузить CSV файл", command=upload_file, width=25)
upload_button.pack(pady=10)

developer_button = tk.Button(frame, text="Информация о разработчике", command=show_developer_info, width=25)
developer_button.pack(pady=10)

exit_button = tk.Button(frame, text="Выход", command=root.quit, width=25)
exit_button.pack(pady=(10, 0))

root.mainloop()
