from pathlib import Path
import json
import sys


def get_app_dir() -> Path:
    """
    Возвращает путь к папке приложения в домашней директории пользователя.
    Создаёт папку, если её нет.
    """
    home = Path.home()
    app_dir = home / ".pcbuilder"
    app_dir.mkdir(exist_ok=True)
    return app_dir


def get_projects_path() -> Path:
    """
    Путь к файлу projects.json.
    При разработке — из папки data/ проекта.
    При запуске из .exe — из домашней директории пользователя.
    """
    if getattr(sys, 'frozen', False):
        return get_app_dir() / "projects.json"
    else:
        return Path(__file__).parent / "data" / "projects.json"


def get_db_path() -> Path:
    """
    Путь к БД комплектующих.
    При запуске из .exe — берём из временной папки PyInstaller.
    При запуске как скрипт — из папки data/ проекта.
    """
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent

    return base_path / "data" / "dependencies.db"


def ensure_projects_file() -> Path:
    """Создаёт projects.json, если его нет, и возвращает путь"""
    path = get_projects_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        with open(path, "w", encoding="utf8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)

    return path
