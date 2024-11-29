import os
import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy import VideoFileClip  # Убедитесь, что импортируете из moviepy.editor
import threading
from PIL import Image, ImageTk  # Импортируем Pillow для работы с изображениями

def convert_video_to_audio(video_file, audio_file):
    """Конвертирует видеофайл в аудиофайл."""
    try:
        print(f"Открываем видеофайл: {video_file}")  # Отладочное сообщение
        with VideoFileClip(video_file) as video_clip:
            print("Проверяем наличие аудиодорожки...")
            audio_clip = video_clip.audio
            if audio_clip is None:
                raise ValueError("Аудиодорожка не найдена в видеофайле.")
            print("Аудиодорожка найдена, начинаем запись...")
            audio_clip.write_audiofile(audio_file)
            print(f"Аудиофайл успешно сохранен как: {audio_file}")
    except Exception as e:
        print(f"Ошибка при конвертации: {e}")  # Отладочное сообщение
        raise RuntimeError(f"Ошибка при конвертации: {e}")

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
root.geometry("420x300")  # Устанавливаем размер окна
root.resizable(False, False)  # Запрещаем изменение размера окна

# Загружаем изображение для фона
background_image = Image.open("1480885740_OcIY8JbtAI4.jpg")  # Замените на путь к вашему изображению
background_image = background_image.resize((420, 300), Image.LANCZOS)  # Используем LANCZOS вместо ANTIALIAS
background_photo = ImageTk.PhotoImage(background_image)

# Создаем Label для фона
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)  # Заполняем весь экран

# Поле для выбора видеофайла
video_label = tk.Label(root, text="Выберите видеофайл:", bg='#5e14a8', fg='white', font=('Arial', 12))
video_label.pack(pady=5)

video_entry = tk.Entry(root, width=40, font=('Arial', 12))
video_entry.pack(pady=5)

# Кнопка "Обзор"
video_button = tk.Button(root, text="Обзор", command=select_video_file, font=('Arial', 12), 
                         bg='#5e14a8', fg='white', width=10)
video_button.pack(pady=5)

# Метка для анимации загрузки
loading_label = tk.Label(root, text="", bg='white', font=('Arial', 12))
loading_label.pack_forget()  # Скрываем метку изначально

# Кнопка для запуска конвертации
convert_button = tk.Button(root, text="Конвертировать", command=convert, font=('Arial', 12), 
                           bg='#5e14a8', fg='white', width=15)
convert_button.pack(pady=20)

# Запускаем главный цикл приложения
root.mainloop()
