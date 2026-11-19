import sqlite3

from app_paths import get_db_path

TABLE_MAP = {
    "cpu": "processors",
    "gpu": "video_cards",
    "mat": "mat_plates",
    "ram": "ram_modules",
    "ssd": "ssd_drives",
    "pb": "power_supplies",
    "case": "cases",
    "cooling": "cooling_systems",
}


class ComponentManager:
    """Менеджер для работы с базой комплектующих (SQLite)"""

    def __init__(self, db_path=None):
        self.db_path = db_path or get_db_path()
        self.conn = None
        self._connect()

    def _connect(self):
        """Подключение к БД"""
        if not self.db_path.exists():
            raise FileNotFoundError(f"База данных не найдена: {self.db_path}")

        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def _get_table(self, component_type):
        """Получает реальное имя таблицы по внутреннему ключу"""
        table = TABLE_MAP.get(component_type)
        if not table:
            raise ValueError(f"Неизвестный тип компонента: {component_type}")
        return table

    def get_all(self, component_type):
        """Получает все компоненты определённого типа"""
        table = self._get_table(component_type)
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()

        return {str(row["id"]): dict(row) for row in rows}

    def get_component(self, component_type, component_id):
        """Получает конкретный компонент по типу и ID"""
        table = self._get_table(component_type)
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table} WHERE id = ?", (component_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def search(self, component_type, query):
        """Поиск компонентов по названию"""
        table = self._get_table(component_type)
        cursor = self.conn.cursor()
        cursor.execute(
            f"SELECT * FROM {table} WHERE name LIKE ?", (f"%{query}%",)
        )
        rows = cursor.fetchall()
        return {str(row["id"]): dict(row) for row in rows}

    def close(self):
        """Закрыть соединение"""
        if self.conn:
            self.conn.close()
