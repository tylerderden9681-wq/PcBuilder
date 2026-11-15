import csv
from datetime import datetime
import qtawesome as qta
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton,
    QScrollArea, QFileDialog, QMessageBox,
    QDialog,
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize


class ComponentCard(QFrame):
    """Карточка компонента в конфигурации проекта"""

    open_detail = pyqtSignal(str, str)

    def __init__(
            self, component_type, component_name,
            price, icon_name, parent=None,
    ):
        super().__init__(parent)
        self.component_type = component_type
        self.component_name = component_name
        self.setObjectName("ComponentCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._build_ui(component_type, component_name, price, icon_name)

    def _build_ui(self, component_type, component_name, price, icon_name):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        icon = QLabel()
        icon.setPixmap(
            qta.icon(icon_name, color="#0078d7").pixmap(QSize(32, 32))
        )
        icon.setFixedSize(32, 32)
        layout.addWidget(icon)

        type_names = {
            "cpu": "Процессор",
            "gpu": "Видеокарта",
            "mat": "Материнская плата",
            "ram": "Оперативная память",
            "ssd": "Накопитель (SSD)",
            "pb": "Блок питания",
            "case": "Корпус",
            "cooling": "Охлаждение",
        }
        type_label = QLabel(
            f"{type_names.get(component_type, component_type)}:"
        )
        type_label.setObjectName("ComponentCardType")
        type_label.setMinimumWidth(140)
        layout.addWidget(type_label)

        name_label = QLabel(component_name)
        name_label.setObjectName("ComponentCardName")
        name_label.setWordWrap(True)
        layout.addWidget(name_label, stretch=1)

        try:
            price_formatted = f"{int(price):,}₽".replace(",", " ")
        except Exception:
            price_formatted = price

        price_label = QLabel(price_formatted)
        price_label.setObjectName("ComponentCardPrice")
        layout.addWidget(price_label)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.open_detail.emit(self.component_type, self.component_name)
        super().mouseDoubleClickEvent(event)


class ProjectPage(QWidget):
    """Страница проекта с конфигурацией"""

    go_back = pyqtSignal()

    def __init__(self, project_manager, component_manager, parent=None):
        super().__init__(parent)
        self.project_manager = project_manager
        self.component_manager = component_manager
        self.setObjectName("ProjectPage")
        self.current_project = None
        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        top_panel = self._build_top_panel()
        main_layout.addWidget(top_panel)

        self.title_label = QLabel()
        self.title_label.setObjectName("ProjectPageTitle")
        self.title_label.setWordWrap(True)
        main_layout.addWidget(self.title_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setObjectName("ProjectScroll")

        content = QWidget()
        content.setObjectName("ProjectContent")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setSpacing(15)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        scroll.setWidget(content)
        main_layout.addWidget(scroll, stretch=1)

    def _build_top_panel(self):
        panel = QFrame()
        panel.setObjectName("TopPanel")
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        back_button = QPushButton()
        back_button.setIcon(qta.icon("fa6s.arrow-left", color="white"))
        back_button.setIconSize(QSize(20, 20))
        back_button.setObjectName("BackButton")
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        back_button.setFixedSize(44, 44)
        back_button.clicked.connect(self.go_back.emit)
        layout.addWidget(back_button)

        layout.addStretch()

        export_csv_btn = QPushButton()
        export_csv_btn.setIcon(qta.icon("fa6s.file-csv", color="white"))
        export_csv_btn.setIconSize(QSize(20, 20))
        export_csv_btn.setObjectName("ExportButton")
        export_csv_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_csv_btn.setFixedSize(44, 44)
        export_csv_btn.setToolTip("Экспорт в CSV")
        export_csv_btn.clicked.connect(self.export_to_csv)
        layout.addWidget(export_csv_btn)

        export_txt_btn = QPushButton()
        export_txt_btn.setIcon(qta.icon("fa6s.file-lines", color="white"))
        export_txt_btn.setIconSize(QSize(20, 20))
        export_txt_btn.setObjectName("ExportButton")
        export_txt_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_txt_btn.setFixedSize(44, 44)
        export_txt_btn.setToolTip("Экспорт в TXT")
        export_txt_btn.clicked.connect(self.export_to_txt)
        layout.addWidget(export_txt_btn)

        edit_btn = QPushButton("Редактировать конфигурацию")
        edit_btn.setObjectName("ActionButton")
        edit_btn.setIcon(qta.icon("fa6s.pen", color="white"))
        edit_btn.setIconSize(QSize(20, 20))
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.clicked.connect(self.edit_the_project_config)
        layout.addWidget(edit_btn)

        return panel

    def load_project(self, project_data):
        """Загружает данные проекта на страницу"""
        self.current_project = project_data
        self.title_label.setText(f"Проект «{project_data['name']}»")

        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        section_header = QLabel("Конфигурация")
        section_header.setObjectName("SectionHeader")
        self.content_layout.addWidget(section_header)

        config = project_data.get("config", {})
        components = [
            ("cpu", config.get("cpu", "Не указано"), "fa6s.microchip"),
            ("gpu", config.get("gpu", "Не указано"), "fa6s.display"),
            ("mat", config.get("mat", "Не указано"), "fa6s.server"),
            ("ram", config.get("ram", "Не указано"), "fa6s.memory"),
            ("ssd", config.get("ssd", "Не указано"), "fa6s.hard-drive"),
            ("pb", config.get("pb", "Не указано"), "fa6s.bolt"),
            ("case", config.get("case", "Не указано"), "fa6s.box"),
            ("cooling", config.get("cooling", "Не указано"), "fa6s.fan"),
        ]

        for comp_type, comp_name, icon_name in components:
            if comp_name and comp_name != "Не указано":
                price = self._get_component_price(comp_type, comp_name)

                card = ComponentCard(comp_type, comp_name, price, icon_name)
                card.open_detail.connect(self._show_component_detail)
                self.content_layout.addWidget(card)
            else:
                empty_card = QLabel(f"{comp_type.upper()}: Не выбрано")
                empty_card.setObjectName("EmptyComponentLabel")
                self.content_layout.addWidget(empty_card)

        total_price = project_data.get("price", "0")
        try:
            price_formatted = f"{int(total_price):,}₽".replace(",", " ")
        except Exception:
            price_formatted = total_price

        price_block = QFrame()
        price_block.setObjectName("PriceBlock")
        price_layout = QHBoxLayout(price_block)
        price_layout.setContentsMargins(20, 20, 20, 20)

        label = QLabel("Итоговая стоимость:")
        label.setObjectName("PriceBlockHeader")
        price_layout.addWidget(label)

        price_layout.addStretch()

        price_label = QLabel(price_formatted)
        price_label.setObjectName("BigPrice")
        price_layout.addWidget(price_label)

        self.content_layout.addWidget(price_block)
        self.content_layout.addStretch()

    def _get_component_price(self, component_type, component_name):
        """Ищет цену компонента в БД по названию"""
        try:
            components = self.component_manager.get_all(component_type)
            for cid, comp in components.items():
                if comp["name"] == component_name:
                    return comp.get("price", "0")
        except Exception:
            pass
        return "0"

    def _show_component_detail(self, component_type, component_name):
        """Открывает диалог с характеристиками компонента"""
        # Ищем компонент в БД
        try:
            components = self.component_manager.get_all(component_type)
            comp_data = None
            for cid, comp in components.items():
                if comp["name"] == component_name:
                    comp_data = comp
                    break

            if comp_data:
                from qt_widgets.component_detail_dialog import (
                    ComponentDetailDialog
                )

                dialog = ComponentDetailDialog(
                    component_data=comp_data,
                    component_type=component_type,
                    component_manager=self.component_manager,
                    parent=self
                )
                dialog.exec()
            else:
                QMessageBox.warning(
                    self,
                    "Внимание",
                    f"Компонент '{component_name}' не найден в базе данных."
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось открыть характеристики:\n{e}"
            )

    def edit_the_project_config(self):
        """Открывает диалог редактирования конфигурации"""
        if not self.current_project:
            return

        from qt_widgets.config_dialog import ConfigDialog

        config_dialog = ConfigDialog(
            project_name=self.current_project["name"],
            component_manager=self.component_manager,
            initial_data=self.current_project.get("config", {}),
            parent=self
        )

        if config_dialog.exec() == QDialog.DialogCode.Accepted:
            new_config_data = config_dialog.get_config_data()

            project_id = self.current_project["id"]
            self.project_manager.update_project(
                project_id,
                {
                    "config": {
                        "cpu": new_config_data["cpu"],
                        "mat": new_config_data["mat"],
                        "pb": new_config_data["pb"],
                        "gpu": new_config_data["gpu"],
                        "ram": new_config_data["ram"],
                        "ssd": new_config_data["ssd"],
                        "case": new_config_data["case"],
                        "cooling": new_config_data["cooling"],
                    },
                    "price": new_config_data.get("price", "0")
                }
            )

            self.current_project["config"] = new_config_data
            self.current_project["price"] = new_config_data.get("price", "0")

            self.load_project(self.current_project)
            QMessageBox.information(self, "Успех", "Конфигурация обновлена!")

    def export_to_csv(self):
        """Экспорт конфигурации в CSV"""
        if not self.current_project:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить в CSV",
            f"{self.current_project['name']}.csv",
            "CSV файлы (*.csv)"
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f, delimiter=";")

                # Заголовки
                writer.writerow(["Параметр", "Значение"])

                # Основные данные
                writer.writerow(
                    ["Название проекта", self.current_project["name"]]
                )
                writer.writerow(
                    ["Описание", self.current_project.get("description", "")]
                )
                writer.writerow(
                    ["Итоговая цена", self.current_project.get("price", "0")]
                )
                writer.writerow([])

                writer.writerow(["Компонент", "Модель"])
                config = self.current_project.get("config", {})

                component_names = {
                    "cpu": "Процессор",
                    "gpu": "Видеокарта",
                    "mat": "Материнская плата",
                    "ram": "Оперативная память",
                    "ssd": "Накопитель (SSD)",
                    "pb": "Блок питания",
                    "case": "Корпус",
                    "cooling": "Охлаждение",
                }

                for key, name in component_names.items():
                    value = config.get(key, "Не указано")
                    writer.writerow([name, value])

            QMessageBox.information(
                self,
                "Успех",
                f"Конфигурация сохранена в:\n{file_path}"
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось сохранить файл:\n{e}"
            )

    def export_to_txt(self):
        """Экспорт конфигурации в TXT"""
        if not self.current_project:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить в TXT",
            f"{self.current_project['name']}.txt",
            "TXT файлы (*.txt)"
        )

        if not file_path:
            return

        try:
            p = self.current_project
            config = p.get("config", {})

            content = f"""=== Проект: {p['name']} ===

    Описание:
    {p.get('description', 'Не указано')}

    Конфигурация:
    • Процессор: {config.get('cpu', 'Не указано')}
    • Видеокарта: {config.get('gpu', 'Не указано')}
    • Материнская плата: {config.get('mat', 'Не указано')}
    • Оперативная память: {config.get('ram', 'Не указано')}
    • Накопитель (SSD): {config.get('ssd', 'Не указано')}
    • Блок питания: {config.get('pb', 'Не указано')}
    • Корпус: {config.get('case', 'Не указано')}
    • Охлаждение: {config.get('cooling', 'Не указано')}

    Итоговая стоимость: {p.get('price', '0')} руб.

    Дата экспорта: {datetime.now().strftime('%d.%m.%Y %H:%M')}
    """

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            QMessageBox.information(
                self,
                "Успех",
                f"Конфигурация сохранена в:\n{file_path}"
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось сохранить файл:\n{e}"
            )
