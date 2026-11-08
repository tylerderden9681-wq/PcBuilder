import qtawesome as qta
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QWidget, QFrame, QMessageBox,
    QListWidget, QListWidgetItem, QTabWidget,
    QAbstractItemView,
)
from PyQt6.QtGui import QKeySequence, QShortcut, QAction
from PyQt6.QtCore import Qt, QSize


class ComponentItemWidget(QWidget):
    """Кастомный виджет для отображения компонента в списке"""

    def __init__(self, name, price, specs=None, parent=None):
        super().__init__(parent)
        self.setObjectName("ComponentItem")

        self.setFixedHeight(60)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        info_layout.setContentsMargins(0, 0, 0, 0)

        name_label = QLabel(name)
        name_label.setObjectName("ComponentName")
        name_label.setWordWrap(True)
        info_layout.addWidget(name_label)

        if specs:
            specs_label = QLabel(specs)
            specs_label.setObjectName("ComponentSpecs")
            specs_label.setWordWrap(True)
            info_layout.addWidget(specs_label)

        layout.addLayout(info_layout, stretch=1)

        price_label = QLabel(f"{price}₽")
        price_label.setObjectName("ComponentPrice")
        price_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(price_label)


# Формат: (ключ_в_БД, суффикс_для_отображения)
SPECS_FIELDS = {
    "cpu": [
        ("socket", " сокет"),
        ("cores", " ядер"),
        ("tdp", " В потребления"),
        ("threads", " потоков"),
        ("base_clock", " базовой частоты"),
    ],
    "gpu": [("video_memory", ""), ("memory_bus", ""), ("interface", "")],
    "mat": [("socket", ""), ("form_factor", ""), ("memory_slots", "")],
    "ram": [("memory_type", ""), ("memory_capacity", ""), ("frequency", "")],
    "ssd": [("type", ""), ("storage_capacity", ""), ("TBW", "")],
    "pb": [("power", "W"), ("sertification", "")],
    "case": [("form-factors", ""), ("size_type", "")],
    "cooling": [("type", ""), ("sockets", ""), ("power", "")],
}


class ConfigDialog(QDialog):
    """
    Диалоговое окно для настройки конфигурации проекта.
    Полноэкранное, с вкладками и панелью итоговой цены.
    """

    def __init__(
            self, project_name, component_manager,
            initial_data=None, parent=None
    ):
        super().__init__(parent)
        self.project_name = project_name
        self.component_manager = component_manager
        self.initial_data = initial_data or {}
        self.setWindowTitle(f"Конфигурация: {project_name}")

        self.setMinimumSize(1000, 700)
        self.setWindowState(Qt.WindowState.WindowMaximized)
        self.setObjectName("ConfigDialog")

        self.selected_components = {}
        self.selected_data = {}
        self.inputs = {}

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        title_label = QLabel(f"Настройка сборки «{self.project_name}»")
        title_label.setObjectName("ConfigDialogTitle")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        hint_label = QLabel(
            "Выберите компоненты из списка. Используйте поиск "
            "для быстрой навигации."
        )
        hint_label.setObjectName("ConfigDialogHint")
        hint_label.setWordWrap(True)
        layout.addWidget(hint_label)

        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("ConfigTabs")
        self.tab_widget.currentChanged.connect(self._on_tab_changed)

        tabs = [
            ("cpu", "Процессор"),
            ("gpu", "Видеокарта"),
            ("mat", "Мат. плата"),
            ("ram", "ОЗУ"),
            ("ssd", "SSD"),
            ("pb", "Блок питания"),
            ("case", "Корпус"),
            ("cooling", "Охлаждение"),
            ("price", "Итог"),
        ]

        for key, tab_name in tabs:
            if key == "price":
                tab_widget = self._create_price_tab()
            else:
                tab_widget = self._create_component_tab(key, tab_name)

            self.tab_widget.addTab(tab_widget, tab_name)

        layout.addWidget(self.tab_widget, stretch=1)

        self.summary_panel = self._create_summary_panel()
        layout.addWidget(self.summary_panel)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        skip_btn = QPushButton("Пропустить")
        skip_btn.setObjectName("DialogButtonSecondary")
        skip_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        skip_btn.setMinimumWidth(120)
        skip_btn.setMinimumHeight(40)
        skip_btn.clicked.connect(self.accept)

        save_btn = QPushButton("Сохранить")
        save_btn.setObjectName("DialogButtonPrimary")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setMinimumWidth(140)
        save_btn.setMinimumHeight(40)
        save_btn.clicked.connect(self.validate_and_accept)

        btn_layout.addWidget(skip_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

        QShortcut(QKeySequence("Ctrl+Return"), self).activated.connect(
            self.validate_and_accept
        )
        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(
            self.validate_and_accept
        )
        QShortcut(QKeySequence("Escape"), self).activated.connect(self.accept)

        self._select_initial_components()
        self._update_summary()

    def _create_summary_panel(self):
        """Панель с итоговой ценой внизу диалога"""
        panel = QFrame()
        panel.setObjectName("SummaryPanel")

        panel_layout = QHBoxLayout(panel)
        panel_layout.setContentsMargins(20, 12, 20, 12)

        total_label = QLabel("Итого:")
        total_label.setObjectName("SummaryLabel")
        panel_layout.addWidget(total_label)

        panel_layout.addStretch()

        self.total_price_label = QLabel("0₽")
        self.total_price_label.setObjectName("TotalPriceLabel")
        self.total_price_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        panel_layout.addWidget(self.total_price_label)

        return panel

    def _create_component_tab(self, component_type, tab_name):
        """Вкладка с поиском и списком компонентов"""
        tab = QWidget()
        tab.setObjectName("ConfigTab")
        tab_layout = QVBoxLayout(tab)
        tab_layout.setSpacing(12)
        tab_layout.setContentsMargins(20, 20, 20, 20)

        header = QLabel(f"Выберите: {tab_name}")
        header.setObjectName("TabHeader")
        tab_layout.addWidget(header)

        search_input = QLineEdit()
        search_input.setObjectName("ConfigSearchInput")
        search_input.setPlaceholderText(f"Поиск: {tab_name.lower()}...")
        search_input.setClearButtonEnabled(True)
        search_input.setMinimumHeight(36)

        search_icon = qta.icon("fa5s.search", color="#8a8d91")
        search_action = QAction(search_icon, "", search_input)
        search_input.addAction(
            search_action, QLineEdit.ActionPosition.LeadingPosition
        )
        tab_layout.addWidget(search_input)

        list_widget = QListWidget()
        list_widget.setObjectName("ComponentList")
        list_widget.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        list_widget.setVerticalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        list_widget.setAlternatingRowColors(True)
        list_widget.itemDoubleClicked.connect(
            lambda item: self._show_component_detail(item, component_type)
        )

        components = self.component_manager.get_all(component_type)
        selected_item = None

        if not components:
            empty_item = QListWidgetItem(
                "Компоненты не найдены. Видимо разработчик их не добавил :)"
            )
            empty_item.setFlags(Qt.ItemFlag.NoItemFlags)
            list_widget.addItem(empty_item)
        else:
            for cid, comp in components.items():
                specs_parts = []
                for field_key, suffix in SPECS_FIELDS.get(component_type, []):
                    if field_key in comp and comp[field_key] not in (
                        None,
                        "",
                        "Не указано",
                    ):
                        value = comp[field_key]
                        if suffix:
                            specs_parts.append(f"{value}{suffix}")
                        else:
                            specs_parts.append(str(value))

                specs = " • ".join(specs_parts[:5]) if specs_parts else None

                item_widget = ComponentItemWidget(
                    name=comp["name"], price=comp["price"], specs=specs
                )

                item = QListWidgetItem()
                item.setData(Qt.ItemDataRole.UserRole, cid)
                item.setSizeHint(item_widget.sizeHint())

                list_widget.addItem(item)
                list_widget.setItemWidget(item, item_widget)

                if cid == self.selected_components.get(component_type):
                    selected_item = item

        if selected_item:
            list_widget.setCurrentItem(selected_item)

        list_widget.currentItemChanged.connect(
            lambda current, previous: self._on_item_selected(
                current, previous, component_type, list_widget
            )
        )

        search_input.textChanged.connect(
            lambda text: self._filter_list(list_widget, text)
        )

        tab_layout.addWidget(list_widget, stretch=1)

        self.selected_components[component_type] = None

        return tab

    def _show_component_detail(self, item, component_type):
        """Открывает диалог с детальной информацией о компоненте"""
        component_id = item.data(Qt.ItemDataRole.UserRole)
        if not component_id:
            return

        comp = self.component_manager.get_component(
            component_type, component_id
        )
        if not comp:
            return

        from qt_widgets.component_detail_dialog import ComponentDetailDialog

        dialog = ComponentDetailDialog(
            component_data=comp,
            component_type=component_type,
            component_manager=self.component_manager,
            parent=self,
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            for i in range(item.listWidget().count()):
                list_item = item.listWidget().item(i)
                if list_item.data(Qt.ItemDataRole.UserRole) == component_id:
                    item.listWidget().setCurrentItem(list_item)
                    break

    def _create_price_tab(self):
        """Вкладка с полной конфигурацией и итоговой ценой"""
        tab = QWidget()
        tab.setObjectName("ConfigTab")
        tab_layout = QVBoxLayout(tab)
        tab_layout.setSpacing(12)
        tab_layout.setContentsMargins(20, 20, 20, 20)

        header = QLabel("Ваша конфигурация")
        header.setObjectName("TabHeader")
        tab_layout.addWidget(header)

        desc = QLabel(
            "Здесь отображаются все выбранные вами компоненты и итоговая "
            "стоимость сборки."
        )
        desc.setObjectName("TabDescription")
        desc.setWordWrap(True)
        tab_layout.addWidget(desc)

        self.config_list_container = QFrame()
        self.config_list_container.setObjectName("ConfigListContainer")
        self.config_list_layout = QVBoxLayout(self.config_list_container)
        self.config_list_layout.setSpacing(8)
        self.config_list_layout.setContentsMargins(15, 15, 15, 15)

        self.empty_config_label = QLabel(
            "Пока не выбрано ни одного компонента. "
            "Перейдите на вкладки выше, чтобы добавить комплектующие."
        )
        self.empty_config_label.setObjectName("EmptyConfigLabel")
        self.empty_config_label.setWordWrap(True)
        self.empty_config_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.config_list_layout.addWidget(self.empty_config_label)

        tab_layout.addWidget(self.config_list_container, stretch=1)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setObjectName("ConfigSeparator")
        tab_layout.addWidget(separator)

        total_row = QHBoxLayout()
        total_label = QLabel("Итоговая стоимость:")
        total_label.setObjectName("ConfigTotalLabel")
        total_row.addWidget(total_label)

        total_row.addStretch()

        self.tab_total_price_label = QLabel("0₽")
        self.tab_total_price_label.setObjectName("TabTotalPriceLabel")
        total_row.addWidget(self.tab_total_price_label)
        tab_layout.addLayout(total_row)

        return tab

    def _on_item_selected(
        self, current_item, previous_item, component_type, list_widget
    ):
        """Обработчик выбора элемента"""
        if current_item:
            component_id = current_item.data(Qt.ItemDataRole.UserRole)
            self.selected_components[component_type] = component_id
            comp = self.component_manager.get_component(
                component_type, component_id
            )
            self.selected_data[component_type] = comp
        else:
            self.selected_components[component_type] = None
            self.selected_data.pop(component_type, None)

        self._update_summary()

    def _on_tab_changed(self, index):
        """При переключении на вкладку 'Итог'"""
        if index == 8:
            self._update_config_list()

    def _update_summary(self):
        """Пересчитывает итоговую цену"""
        total = 0
        for comp_data in self.selected_data.values():
            if comp_data and "price" in comp_data:
                try:
                    total += int(comp_data["price"])
                except (ValueError, TypeError):
                    pass

        formatted = f"{total:,}₽".replace(",", " ")
        self.total_price_label.setText(formatted)
        self.tab_total_price_label.setText(formatted)

    def _update_config_list(self):
        """Обновляет список на вкладке 'Итог'"""
        while self.config_list_layout.count():
            item = self.config_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                item.layout().deleteLater()

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

        has_any = False
        total = 0
        order = ["cpu", "mat", "gpu", "ram", "ssd", "pb", "cooling", "case"]

        for key in order:
            comp_data = self.selected_data.get(key)
            if comp_data:
                has_any = True
                price = 0
                try:
                    price = int(comp_data.get("price", 0))
                except (ValueError, TypeError):
                    pass
                total += price

                row_widget = QWidget()
                row_widget.setObjectName("ConfigRowWidget")
                row_layout = QHBoxLayout(row_widget)
                row_layout.setContentsMargins(12, 10, 12, 10)
                row_layout.setSpacing(12)

                icon_label = QLabel()
                icon_label.setPixmap(
                    qta.icon(
                        type_icons.get(key, "fa6s.circle"), color="#0078d7"
                    ).pixmap(QSize(20, 20))
                )
                icon_label.setFixedSize(20, 20)
                row_layout.addWidget(icon_label)

                type_label = QLabel(f"{type_names.get(key, key)}:")
                type_label.setObjectName("ConfigRowType")
                type_label.setMinimumWidth(140)
                row_layout.addWidget(type_label)

                name_label = QLabel(comp_data.get("name", "Не указано"))
                name_label.setObjectName("ConfigRowName")
                name_label.setWordWrap(True)
                row_layout.addWidget(name_label, stretch=1)

                price_label = QLabel(f"{price:,}₽".replace(",", " "))
                price_label.setObjectName("ConfigRowPrice")
                price_label.setMinimumWidth(100)
                price_label.setAlignment(Qt.AlignmentFlag.AlignRight)
                row_layout.addWidget(price_label)

                self.config_list_layout.addWidget(row_widget)

        if not has_any:
            self.empty_config_label = QLabel(
                "Пока не выбрано ни одного компонента. "
                "Перейдите на вкладки выше, чтобы добавить комплектующие."
            )
            self.empty_config_label.setObjectName("EmptyConfigLabel")
            self.empty_config_label.setWordWrap(True)
            self.empty_config_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.config_list_layout.addWidget(self.empty_config_label)

        formatted = f"{total:,}₽".replace(",", " ")
        self.tab_total_price_label.setText(formatted)

    def _filter_list(self, list_widget, search_text):
        """Фильтрует элементы списка"""
        search_text = search_text.lower().strip()

        for i in range(list_widget.count()):
            item = list_widget.item(i)
            widget = list_widget.itemWidget(item)

            if widget is None:
                continue

            name_label = widget.findChild(QLabel, "ComponentName")
            if name_label:
                item_name = name_label.text().lower()
                item.setHidden(
                    bool(search_text) and search_text not in item_name
                )

    def validate_and_accept(self):
        """Проверяет данные перед сохранением"""
        if not any(self.selected_components.values()):
            QMessageBox.warning(
                self,
                "Внимание",
                "Не выбрано ни одного компонента. Сборка будет пустой.",
            )
        self.accept()

    def get_config_data(self):
        """Возвращает словарь с введёнными данными"""
        data = {}

        for key, component_id in self.selected_components.items():
            if component_id:
                comp = self.component_manager.get_component(key, component_id)
                data[key] = comp["name"]
                data[f"{key}_id"] = component_id
            else:
                data[key] = "Не указано"
                data[f"{key}_id"] = None

        total = 0
        for comp_data in self.selected_data.values():
            if comp_data and "price" in comp_data:
                try:
                    total += int(comp_data["price"])
                except (ValueError, TypeError):
                    pass
        data["price"] = str(total)

        return data

    def _select_initial_components(self):
        """Предвыбирает компоненты из initial_data"""
        for component_type, component_name in self.initial_data.items():
            if component_type in [
                "cpu", "gpu", "mat", "ram", "ssd", "pb", "case", "cooling"
            ]:
                if component_name and component_name != "Не указано":
                    components = self.component_manager.get_all(component_type)
                    for cid, comp in components.items():
                        if comp["name"] == component_name:
                            self.selected_components[component_type] = cid
                            self.selected_data[component_type] = comp
                            break
