import os
import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy import *
import threading

def convert_video_to_audio(video_file, audio_file):
    """Конвертирует видеофайл в аудиофайл."""
    video_clip = VideoFileClip(video_file)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_file)
    audio_clip.close()
    video_clip.close()

def select_video_file():
    """Открывает диалог для выбора видеофайла."""
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv")])
    if video_path:
        video_entry.delete(0, tk.END)
        video_entry.insert(0, video_path)

def animate_loading():
    """Анимирует метку загрузки с точками."""
    global loading_dots
    loading_dots = (loading_dots + 1) % 4  # Увеличиваем счетчик точек
    dots = '.' * loading_dots
    loading_label.config(text=f"Загрузка{dots}")
    loading_label.after(500, animate_loading)  # Обновляем каждые 500 мс

def convert():
    """Обрабатывает конвертацию видео в аудио."""
    video_path = video_entry.get()

    if not video_path:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите видеофайл.")
        return

    # Создаем папку converter и подкаталог audio, если они не существуют
    output_dir = os.path.join(os.getcwd(), 'Audio')
    os.makedirs(output_dir, exist_ok=True)

    # Имя выходного аудиофайла
    audio_file_name = os.path.splitext(os.path.basename(video_path))[0] + '.mp3'
    audio_path = os.path.join(output_dir, audio_file_name)

    # Запускаем анимацию загрузки
    global loading_dots
    loading_dots = 0
    loading_label.pack(pady=10)
    animate_loading()

    # Запускаем конвертацию в отдельном потоке
    threading.Thread(target=run_conversion, args=(video_path, audio_path)).start()

def run_conversion(video_path, audio_path):
    """Запускает процесс конвертации и завершает анимацию загрузки."""
    try:
        convert_video_to_audio(video_path, audio_path)
        messagebox.showinfo("Успех", f"Конвертация завершена! Аудиофайл сохранен как {audio_path}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
    finally:
        loading_label.pack_forget()  # Скрываем метку после завершения

# Создаем главное окно
root = tk.Tk()
root.title("Конвертер видео в аудио")

# Поле для выбора видеофайла
video_label = tk.Label(root, text="Выберите видеофайл:")
video_label.pack(pady=5)

video_entry = tk.Entry(root, width=50)
video_entry.pack(pady=5)

video_button = tk.Button(root, text="Обзор", command=select_video_file)
video_button.pack(pady=5)

# Метка для анимации загрузки
loading_label = tk.Label(root, text="")
loading_label.pack_forget()  # Скрываем метку изначально

# Кнопка для запуска конвертации
convert_button = tk.Button(root, text="Конвертировать", command=convert)
convert_button.pack(pady=20)

# Запускаем главный цикл приложения
root.mainloop()