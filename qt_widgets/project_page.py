import csv
from datetime import datetime
import qtawesome as qta
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QScrollArea,
    QFileDialog,
    QMessageBox,
    QDialog,
    QLineEdit,
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize


class ComponentCard(QFrame):
    """Карточка компонента в конфигурации проекта"""

    open_detail = pyqtSignal(str, str)

    def __init__(
        self,
        component_type,
        component_name,
        price,
        icon_name,
        parent=None,
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


class EditableTitle(QWidget):
    """Заголовок проекта с возможностью inline-редактирования"""

    title_changed = pyqtSignal(str)

    def __init__(self, initial_title: str, parent=None):
        super().__init__(parent)
        self._title = initial_title
        self._is_editing = False
        self._build_ui()

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # Иконка проекта
        self.icon_label = QLabel()
        self.icon_label.setPixmap(
            qta.icon("fa6s.folder-open", color="#0078d7").pixmap(QSize(36, 36))
        )
        self.icon_label.setFixedSize(36, 36)
        layout.addWidget(self.icon_label)

        # Контейнер для заголовка
        self.title_container = QWidget()
        self.title_container_layout = QVBoxLayout(self.title_container)
        self.title_container_layout.setContentsMargins(0, 0, 0, 0)
        self.title_container_layout.setSpacing(0)

        # QLabel для отображения
        self.title_label = QLabel(f"Проект «{self._title}»")
        self.title_label.setObjectName("ProjectPageTitle")
        self.title_label.setWordWrap(True)
        self.title_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.title_label.setToolTip("Двойной клик для редактирования")
        self.title_label.mouseDoubleClickEvent = (
            lambda e: self._start_editing()
        )
        self.title_container_layout.addWidget(self.title_label)

        self.title_edit = QLineEdit(self._title)
        self.title_edit.setObjectName("ProjectTitleEdit")
        self.title_edit.setVisible(False)
        self.title_edit.returnPressed.connect(self._finish_editing)
        self.title_edit.installEventFilter(self)
        self.title_container_layout.addWidget(self.title_edit)

        layout.addWidget(self.title_container, stretch=1)

        self.edit_buttons = QWidget()
        self.edit_buttons_layout = QHBoxLayout(self.edit_buttons)
        self.edit_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.edit_buttons_layout.setSpacing(8)

        self.save_btn = QPushButton()
        self.save_btn.setIcon(qta.icon("fa6s.check", color="#2e7d32"))
        self.save_btn.setIconSize(QSize(18, 18))
        self.save_btn.setObjectName("TitleSaveButton")
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setFixedSize(36, 36)
        self.save_btn.setToolTip("Сохранить название")
        self.save_btn.clicked.connect(self._finish_editing)
        self.edit_buttons_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton()
        self.cancel_btn.setIcon(qta.icon("fa6s.xmark", color="#8a8d91"))
        self.cancel_btn.setIconSize(QSize(18, 18))
        self.cancel_btn.setObjectName("TitleCancelButton")
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.setFixedSize(36, 36)
        self.cancel_btn.setToolTip("Отменить редактирование")
        self.cancel_btn.clicked.connect(self._cancel_editing)
        self.edit_buttons_layout.addWidget(self.cancel_btn)

        self.edit_buttons.setVisible(False)
        layout.addWidget(self.edit_buttons)

        self.edit_btn = QPushButton()
        self.edit_btn.setIcon(qta.icon("fa6s.pen-to-square", color="#8a8d91"))
        self.edit_btn.setIconSize(QSize(20, 20))
        self.edit_btn.setObjectName("TitleEditButton")
        self.edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_btn.setFixedSize(36, 36)
        self.edit_btn.setToolTip("Редактировать название")
        self.edit_btn.clicked.connect(self._start_editing)
        layout.addWidget(self.edit_btn)

    def eventFilter(self, obj, event):
        """Перехватываем Escape для отмены редактирования"""
        if obj == self.title_edit and event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Escape:
                self._cancel_editing()
                return True
        return super().eventFilter(obj, event)

    def _start_editing(self):
        """Начинает редактирование названия"""
        if self._is_editing:
            return
        self._is_editing = True

        self.title_label.setVisible(False)
        self.title_edit.setVisible(True)
        self.title_edit.setText(self._title)
        self.title_edit.selectAll()
        self.title_edit.setFocus()

        # Показываем кнопки сохранения/отмены, скрываем карандаш
        self.edit_btn.setVisible(False)
        self.edit_buttons.setVisible(True)

    def _finish_editing(self):
        """Сохраняет новое название"""
        if not self._is_editing:
            return

        new_title = self.title_edit.text().strip()
        if new_title and new_title != self._title:
            self._title = new_title
            self.title_label.setText(f"Проект «{self._title}»")
            self.title_changed.emit(self._title)

        self._exit_editing_mode()

    def _cancel_editing(self):
        """Отменяет редактирование без сохранения"""
        if not self._is_editing:
            return
        self._exit_editing_mode()

    def _exit_editing_mode(self):
        """Возвращает UI в режим отображения"""
        self._is_editing = False
        self.title_edit.setVisible(False)
        self.title_label.setVisible(True)
        self.edit_buttons.setVisible(False)
        self.edit_btn.setVisible(True)

    def set_title(self, title: str):
        """Устанавливает новое название извне"""
        self._title = title
        self.title_label.setText(f"Проект «{self._title}»")


class ProjectPage(QWidget):
    """Страница проекта с конфигурацией"""

    go_back = pyqtSignal()
    project_deleted = pyqtSignal(str)  # id проекта
    project_renamed = pyqtSignal(str, str)  # id, новое название

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

        # Редактируемый заголовок
        self.editable_title = EditableTitle("")
        self.editable_title.title_changed.connect(self._on_title_changed)
        main_layout.addWidget(self.editable_title)

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

        # Кнопка "Назад"
        back_button = QPushButton()
        back_button.setIcon(qta.icon("fa6s.arrow-left", color="white"))
        back_button.setIconSize(QSize(20, 20))
        back_button.setObjectName("BackButton")
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        back_button.setFixedSize(44, 44)
        back_button.clicked.connect(self.go_back.emit)
        layout.addWidget(back_button)

        layout.addStretch()

        # Кнопка экспорта CSV
        export_csv_btn = QPushButton()
        export_csv_btn.setIcon(qta.icon("fa6s.file-csv", color="white"))
        export_csv_btn.setIconSize(QSize(20, 20))
        export_csv_btn.setObjectName("ExportButton")
        export_csv_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_csv_btn.setFixedSize(44, 44)
        export_csv_btn.setToolTip("Экспорт в CSV")
        export_csv_btn.clicked.connect(self.export_to_csv)
        layout.addWidget(export_csv_btn)

        # Кнопка экспорта TXT
        export_txt_btn = QPushButton()
        export_txt_btn.setIcon(qta.icon("fa6s.file-lines", color="white"))
        export_txt_btn.setIconSize(QSize(20, 20))
        export_txt_btn.setObjectName("ExportButton")
        export_txt_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_txt_btn.setFixedSize(44, 44)
        export_txt_btn.setToolTip("Экспорт в TXT")
        export_txt_btn.clicked.connect(self.export_to_txt)
        layout.addWidget(export_txt_btn)

        # Кнопка редактирования конфигурации
        edit_btn = QPushButton("Редактировать конфигурацию")
        edit_btn.setObjectName("ActionButton")
        edit_btn.setIcon(qta.icon("fa6s.pen", color="white"))
        edit_btn.setIconSize(QSize(20, 20))
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.clicked.connect(self.edit_the_project_config)
        layout.addWidget(edit_btn)

        # Кнопка удаления проекта
        delete_btn = QPushButton()
        delete_btn.setIcon(qta.icon("fa6s.trash-can", color="white"))
        delete_btn.setIconSize(QSize(20, 20))
        delete_btn.setObjectName("DeleteProjectButton")
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setFixedSize(44, 44)
        delete_btn.setToolTip("Удалить проект")
        delete_btn.clicked.connect(self._delete_project)
        layout.addWidget(delete_btn)

        return panel

    def load_project(self, project_data):
        """Загружает данные проекта на страницу"""
        self.current_project = project_data
        self.editable_title.set_title(project_data["name"])

        # Очищаем старый контент
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Заголовок секции
        section_header = QLabel("Конфигурация")
        section_header.setObjectName("SectionHeader")
        self.content_layout.addWidget(section_header)

        # Карточки компонентов
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

        # Итоговая цена
        total_price = project_data.get("price", "0")
        try:
            price_formatted = f"{int(total_price):,}₽".replace(",", " ")
        except Exception:
            price_formatted = total_price

        price_block = QFrame()
        price_block.setObjectName("PriceBlock")
        price_layout = QHBoxLayout(price_block)
        price_layout.setContentsMargins(20, 20, 20, 20)

        icon = QLabel()
        icon.setPixmap(
            qta.icon("fa6s.ruble-sign", color="#2e7d32").pixmap(QSize(32, 32))
        )
        price_layout.addWidget(icon)

        label = QLabel("Итоговая стоимость:")
        label.setObjectName("PriceBlockHeader")
        price_layout.addWidget(label)

        price_layout.addStretch()

        price_label = QLabel(price_formatted)
        price_label.setObjectName("BigPrice")
        price_layout.addWidget(price_label)

        self.content_layout.addWidget(price_block)
        self.content_layout.addStretch()

    def _on_title_changed(self, new_title: str):
        """Обработчик изменения названия проекта"""
        if not self.current_project:
            return

        old_title = self.current_project["name"]
        if new_title == old_title:
            return

        project_id = self.current_project["id"]
        self.project_manager.update_project(project_id, {"name": new_title})
        self.current_project["name"] = new_title
        self.project_renamed.emit(project_id, new_title)

        QMessageBox.information(
            self,
            "Успех",
            f"Название проекта изменено:\n«{old_title}» → «{new_title}»",
        )

    def _delete_project(self):
        """Удаляет текущий проект с подтверждением"""
        if not self.current_project:
            return

        project_name = self.current_project["name"]
        project_id = self.current_project["id"]

        reply = QMessageBox.warning(
            self,
            "Удаление проекта",
            f"Вы уверены, что хотите удалить проект «{project_name}»?\n\n"
            "Это действие нельзя отменить.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.project_manager.delete_project(project_id)
            self.project_deleted.emit(project_id)
            self.go_back.emit()

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
        try:
            components = self.component_manager.get_all(component_type)
            comp_data = None
            for cid, comp in components.items():
                if comp["name"] == component_name:
                    comp_data = comp
                    break

            if comp_data:
                from qt_widgets.component_detail_dialog import (
                    ComponentDetailDialog,
                )

                dialog = ComponentDetailDialog(
                    component_data=comp_data,
                    component_type=component_type,
                    component_manager=self.component_manager,
                    parent=self,
                )
                dialog.exec()
            else:
                QMessageBox.warning(
                    self,
                    "Внимание",
                    f"Компонент '{component_name}' не найден в базе данных.",
                )
        except Exception as e:
            QMessageBox.critical(
                self, "Ошибка", f"Не удалось открыть характеристики:\n{e}"
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
            parent=self,
        )

        result = config_dialog.exec()

        if result != QDialog.DialogCode.Accepted:
            return

        new_config_data = config_dialog.get_config_data()

        old_config = self.current_project.get("config", {})
        old_price = self.current_project.get("price", "0")

        config_changed = False
        for key in [
            "cpu", "mat", "pb",
            "gpu", "ram", "ssd",
            "case", "cooling",
        ]:
            if new_config_data.get(key) != old_config.get(key):
                config_changed = True
                break

        price_changed = new_config_data.get("price", "0") != old_price

        if not config_changed and not price_changed:
            QMessageBox.information(
                self,
                "Информация",
                "Конфигурация не изменилась. Сохранение не требуется."
            )
            return

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
                "price": new_config_data.get("price", "0"),
            },
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
            "CSV файлы (*.csv)",
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f, delimiter=";")

                writer.writerow(["Параметр", "Значение"])

                writer.writerow(
                    ["Название проекта",
                     self.current_project["name"]]
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
                self, "Успех", f"Конфигурация сохранена в:\n{file_path}"
            )

        except Exception as e:
            QMessageBox.critical(
                self, "Ошибка",
                f"Не удалось сохранить файл:\n{e}",
            )

    def export_to_txt(self):
        """Экспорт конфигурации в TXT"""
        if not self.current_project:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить в TXT",
            f"{self.current_project['name']}.txt",
            "TXT файлы (*.txt)",
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
                self, "Успех", f"Конфигурация сохранена в:\n{file_path}"
            )

        except Exception as e:
            QMessageBox.critical(
                self, "Ошибка", f"Не удалось сохранить файл:\n{e}",
            )
