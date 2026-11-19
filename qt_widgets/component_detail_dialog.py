import qtawesome as qta
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QScrollArea,
    QWidget,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl

FIELD_INFO = {
    "id": ("ID", "fa6s.hashtag"),
    "name": ("Название", "fa6s.tag"),
    "brand": ("Бренд", "fa6s.copyright"),
    "socket": ("Сокет", "fa6s.microchip"),
    "cores": ("Ядра", "fa6s.layer-group"),
    "threads": ("Потоки", "fa6s.network-wired"),
    "base_clock": ("Базовая частота", "fa6s.gauge"),
    "boost_clock": ("Максимальная частота", "fa6s.gauge-high"),
    "tdp": ("TDP", "fa6s.bolt"),
    "generation": ("Поколение", "fa6s.timeline"),
    "integrated_graphics": ("Встроенная графика", "fa6s.display"),
    "ram_type": ("Тип памяти", "fa6s.memory"),
    "interface": ("Интерфейс", "fa6s.plug"),
    "vram_gb": ("Видеопамять (ГБ)", "fa6s.memory"),
    "vram_type": ("Тип видеопамяти", "fa6s.memory"),
    "video_memory": ("Видеопамять", "fa6s.memory"),
    "memory_bus": ("Шина памяти", "fa6s.route"),
    "memory_bus_bit": ("Шина памяти (бит)", "fa6s.route"),
    "chipset": ("Чипсет", "fa6s.cpu"),
    "form_factor": ("Форм-фактор", "fa6s.ruler-combined"),
    "form-factors": ("Поддерживаемые форм-факторы", "fa6s.ruler-combined"),
    "memory_slots": ("Слоты памяти", "fa6s.memory"),
    "memory_type": ("Тип памяти", "fa6s.memory"),
    "memory_capacity": ("Объём памяти", "fa6s.database"),
    "capacity_gb": ("Объём (ГБ)", "fa6s.database"),
    "storage_capacity": ("Объём хранилища", "fa6s.database"),
    "frequency": ("Частота", "fa6s.wave-square"),
    "frequency_mhz": ("Частота (МГц)", "fa6s.wave-square"),
    "timings": ("Тайминги", "fa6s.clock"),
    "type": ("Тип", "fa6s.hard-drive"),
    "NVMe": ("NVMe", "fa6s.bolt"),
    "DWPD": ("DWPD", "fa6s.sync"),
    "TBW": ("TBW (ресурс)", "fa6s.rotate"),
    "power": ("Мощность", "fa6s.bolt"),
    "wattage_w": ("Мощность (Вт)", "fa6s.bolt"),
    "efficiency_rating": ("Сертификат", "fa6s.certificate"),
    "sertification": ("Сертификат", "fa6s.certificate"),
    "modular": ("Модульность", "fa6s.puzzle-piece"),
    "size_type": ("Типоразмер", "fa6s.box"),
    "expansion_slots": ("Слоты расширения", "fa6s.grid"),
    "included_fans": ("Вентиляторы", "fa6s.fan"),
    "ventilators": ("Вентиляторы", "fa6s.fan"),
    "color": ("Цвет", "fa6s.palette"),
    "weight": ("Вес", "fa6s.weight-hanging"),
    "size_ventilator": ("Размер вентилятора", "fa6s.fan"),
    "sockets": ("Поддержка сокетов", "fa6s.microchip"),
    "tdp_rating_w": ("Рассеиваемая мощность (Вт)", "fa6s.bolt"),
    "video_ports": ("Видеовыходы", "fa6s.tv"),
    "dns_url": ("Ссылка на ДНС", "fa6s.link"),
    "price": ("Цена", "fa6s.ruble-sign"),
}


class ComponentDetailDialog(QDialog):
    """
    Модальное окно с полной информацией о комплектующем.
    Открывается по двойному клику на карточку компонента.
    """

    def __init__(
            self, component_data, component_type,
            component_manager, parent=None
    ):
        super().__init__(parent)
        self.component_data = component_data
        self.component_type = component_type
        self.component_manager = component_manager

        self.setWindowTitle(
            f"Характеристики: {component_data.get('name', 'Компонент')}"
        )
        self.setBaseSize(600, 500)
        self.setMinimumSize(600, 500)
        self.setObjectName("ComponentDetailDialog")

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)

        header_container = QFrame()
        header_container.setObjectName("DetailHeader")
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(20, 20, 20, 20)

        type_icons = {
            "cpu": "fa6s.microchip",
            "gpu": "fa6s.display",
            "mat": "fa6s.server",
            "ram": "fa6s.memory",
            "ssd": "fa6s.hard-drive",
            "pb": "fa6s.bolt",
            "case": "fa6s.box",
            "cooling": "fa6s.fan",
        }
        icon_label = QLabel()
        icon_label.setPixmap(
            qta.icon(
                type_icons.get(self.component_type, "fa6s.circle"),
                color="#0078d7"
            ).pixmap(QSize(48, 48))
        )
        header_layout.addWidget(icon_label)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)

        name_label = QLabel(self.component_data.get("name", "Неизвестно"))
        name_label.setObjectName("DetailName")
        name_label.setWordWrap(True)
        info_layout.addWidget(name_label)

        price = self.component_data.get("price", 0)
        price_label = QLabel(f"{int(price):,}₽".replace(",", " "))
        price_label.setObjectName("DetailPrice")
        info_layout.addWidget(price_label)

        header_layout.addLayout(info_layout, stretch=1)
        layout.addWidget(header_container)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setObjectName("DetailScroll")

        content = QWidget()
        content.setObjectName("DetailContent")
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(12)
        content_layout.setContentsMargins(0, 0, 0, 0)

        groups = self._group_fields()

        for group_name, fields in groups.items():
            if not fields:
                continue

            group_frame = QFrame()
            group_frame.setObjectName("DetailGroup")
            group_layout = QVBoxLayout(group_frame)
            group_layout.setSpacing(8)
            group_layout.setContentsMargins(15, 15, 15, 15)

            group_header = QLabel(group_name)
            group_header.setObjectName("DetailGroupHeader")
            group_layout.addWidget(group_header)

            for field_key in fields:
                if field_key in self.component_data and (
                    self.component_data[field_key] not in (
                        None, "", "Не указано"
                    )
                ):
                    row = self._create_field_row(
                        field_key, self.component_data[field_key]
                    )
                    group_layout.addWidget(row)

            content_layout.addWidget(group_frame)

        scroll.setWidget(content)
        layout.addWidget(scroll, stretch=1)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        dns_url = self.component_data.get("dns_url", "")
        if dns_url:
            dns_btn = QPushButton("Открыть в ДНС")
            dns_btn.setObjectName("DetailButtonSecondary")
            dns_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            dns_btn.setMinimumWidth(140)
            dns_btn.setMinimumHeight(40)
            dns_btn.setIcon(qta.icon(
                "fa6s.arrow-up-right-from-square", color="white")
            )
            dns_btn.clicked.connect(
                lambda: QDesktopServices.openUrl(QUrl(dns_url))
            )
            btn_layout.addWidget(dns_btn)

        select_btn = QPushButton("Выбрать")
        select_btn.setObjectName("DetailButtonPrimary")
        select_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        select_btn.setMinimumWidth(140)
        select_btn.setMinimumHeight(40)
        select_btn.setIcon(qta.icon("fa6s.check", color="white"))
        select_btn.clicked.connect(self.accept)

        btn_layout.addWidget(select_btn)
        layout.addLayout(btn_layout)

    def _group_fields(self):
        """Группирует поля по категориям для красивого отображения"""
        groups = {
            "Основные характеристики": [],
            "Производительность": [],
            "Память и хранилище": [],
            "Физические параметры": [],
            "Поддержка и совместимость": [],
            "Дополнительно": [],
        }

        for key in [
            "brand", "generation", "chipset",
            "type", "size_type", "color",
        ]:
            if key in self.component_data:
                groups["Основные характеристики"].append(key)

        for key in [
            "cores",
            "threads",
            "base_clock",
            "boost_clock",
            "frequency",
            "frequency_mhz",
            "timings",
            "tdp",
            "power",
            "wattage_w",
            "tdp_rating_w",
            "expansion_slots",
        ]:
            if key in self.component_data:
                groups["Производительность"].append(key)

        for key in [
            "ram_type",
            "memory_type",
            "memory_slots",
            "memory_capacity",
            "capacity_gb",
            "storage_capacity",
            "vram_gb",
            "vram_type",
            "video_memory",
            "memory_bus",
            "memory_bus_bit",
            "interface",
            "NVMe",
            "DWPD",
            "TBW",
        ]:
            if key in self.component_data:
                groups["Память и хранилище"].append(key)

        for key in [
            "form_factor",
            "form-factors",
            "weight",
            "size_ventilator",
            "included_fans",
            "ventilators",
            "video_ports",
        ]:
            if key in self.component_data:
                groups["Физические параметры"].append(key)

        for key in [
            "socket",
            "sockets",
            "modular",
            "efficiency_rating",
            "sertification",
        ]:
            if key in self.component_data:
                groups["Поддержка и совместимость"].append(key)

        for key in self.component_data.keys():
            if key not in ["id", "name", "price", "dns_url"]:
                already_added = any(key in g for g in groups.values())
                if not already_added:
                    groups["Дополнительно"].append(key)

        return {k: v for k, v in groups.items() if v}

    def _create_field_row(self, field_key, value):
        """Создаёт строку с иконкой, названием поля и значением"""
        row = QFrame()
        row.setObjectName("DetailFieldRow")
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(10, 8, 10, 8)
        row_layout.setSpacing(12)

        field_label = field_key
        icon_name = "fa6s.circle"

        if field_key in FIELD_INFO:
            field_label, icon_name = FIELD_INFO[field_key]
        else:
            field_label = field_key.replace("_", " ").title()

        icon_label = QLabel()
        try:
            icon_label.setPixmap(
                qta.icon(icon_name, color="#8a8d91").pixmap(QSize(16, 16))
            )
        except Exception:
            try:
                icon_label.setPixmap(
                    qta.icon(
                        "fa6s.circle", color="#8a8d91").pixmap(QSize(16, 16))
                )
            except Exception:
                pass

        row_layout.addWidget(icon_label)

        label = QLabel(f"{field_label}:")
        label.setObjectName("DetailFieldLabel")
        row_layout.addWidget(label)

        row_layout.addStretch()

        value_str = str(value)

        if isinstance(value, (int, float)) and value in (0, 1):
            if field_key in ["integrated_graphics", "NVMe"]:
                value_str = "Да" if value else "Нет"

        value_label = QLabel(value_str)
        value_label.setObjectName("DetailFieldValue")
        value_label.setWordWrap(True)
        row_layout.addWidget(value_label, stretch=1)

        return row
