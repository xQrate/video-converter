import sys
from cx_Freeze import setup, Executable

# Устанавливаем base для GUI-приложений
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Используется для GUI-приложений

setup(
    name="Audio_converter",
    version="1.0",
    description="Приложение для загрузки видео с YouTube",
    executables=[Executable("convert.py", base=base)],  # Указываем base здесь
    options={
        "build_exe": {
            "packages": ["os", "tkinter", "yt_dlp"],
            "includes": [""],
        }
    }
)