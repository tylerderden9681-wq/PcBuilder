import os
from datetime import datetime
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QGridLayout,
    QSplitter,
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QUrl
from PyQt6.QtGui import QDesktopServices
import qtawesome as qta

from qt_widgets.gradient_label import GradientLabel


class StatCard(QFrame):
    """Карточка со статистикой"""

    def __init__(self, title, value, icon_name, color="#0078d7", parent=None):
        super().__init__(parent)
        self.setObjectName("StatCard")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(12)

        icon_label = QLabel()
        icon_label.setPixmap(
            qta.icon(icon_name, color=color).pixmap(QSize(28, 28))
        )
        icon_label.setFixedSize(28, 28)
        layout.addWidget(icon_label)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        text_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel(title)
        title_label.setObjectName("StatTitle")
        text_layout.addWidget(title_label)

        value_label = QLabel(str(value))
        value_label.setObjectName("StatValue")
        text_layout.addWidget(value_label)

        layout.addLayout(text_layout, stretch=1)


class LinkCard(QFrame):
    """Карточка со ссылкой"""

    clicked = pyqtSignal(str)

    def __init__(self, title, url, icon_name, parent=None):
        super().__init__(parent)
        self.url = url
        self.setObjectName("LinkCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(10)

        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(
            icon_name, color="#0078d7").pixmap(QSize(20, 20))
        )
        layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setObjectName("LinkTitle")
        layout.addWidget(title_label)

        layout.addStretch()

        arrow = QLabel("→")
        arrow.setObjectName("LinkArrow")
        layout.addWidget(arrow)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.url)
        super().mousePressEvent(event)


class ProjectCardMini(QFrame):
    """Мини-карточка проекта для дашборда"""

    open_project = pyqtSignal(str)

    def __init__(self, project_id, name, price, parent=None):
        super().__init__(parent)
        self.project_id = project_id
        self.setObjectName("ProjectCardMini")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)

        name_label = QLabel(name)
        name_label.setObjectName("MiniProjectName")
        name_label.setWordWrap(True)
        layout.addWidget(name_label)

        price_label = QLabel(f"{int(price):,}₽".replace(",", " "))
        price_label.setObjectName("MiniProjectPrice")
        layout.addWidget(price_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.open_project.emit(self.project_id)
        super().mousePressEvent(event)


class FooterLink(QFrame):
    """Кликабельная ссылка в футере"""

    def __init__(self, text, url, icon_name, parent=None):
        super().__init__(parent)
        self.url = url
        self.setObjectName("FooterLink")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(url)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)

        icon_label = QLabel()
        icon_label.setPixmap(
            qta.icon(icon_name, color="#8a8d91").pixmap(QSize(20, 20))
        )
        layout.addWidget(icon_label)

        text_label = QLabel(text)
        text_label.setObjectName("FooterLinkText")
        layout.addWidget(text_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            QDesktopServices.openUrl(QUrl(self.url))
        super().mousePressEvent(event)


class DashboardPage(QWidget):
    """Главная страница с дашбордом"""

    open_project = pyqtSignal(str)
    create_project = pyqtSignal()
    view_all_projects = pyqtSignal()
    show_info = pyqtSignal()

    def __init__(self, project_manager, parent=None):
        super().__init__(parent)
        self.project_manager = project_manager
        self.setObjectName("DashboardPage")
        self._build_ui()

    def _build_ui(self):
        """Создаёт или очищает layout и заполняет его виджетами"""
        layout = self.layout()
        if layout is None:
            layout = QVBoxLayout(self)
            layout.setContentsMargins(30, 30, 30, 30)
            layout.setSpacing(25)
        else:
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

        welcome_section = self._build_welcome_section()
        layout.addWidget(welcome_section)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(25)

        left_layout.addWidget(self._build_stats_section())
        left_layout.addWidget(self._build_projects_section())
        left_layout.addStretch()

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(25)

        right_layout.addWidget(self._build_actions_section())
        right_layout.addWidget(self._build_links_section())
        right_layout.addStretch()

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 65)
        splitter.setStretchFactor(1, 35)

        splitter.setHandleWidth(5)

        layout.addWidget(splitter)
        layout.addStretch()

        footer_section = self._build_footer_section()
        layout.addWidget(footer_section)

    def _build_welcome_section(self):
        frame = QFrame()
        frame.setObjectName("WelcomeFrame")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(25, 20, 25, 20)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(8)

        try:
            username = os.getlogin().capitalize()
        except Exception:
            username = Path.home().name.capitalize()

        hour = datetime.now().hour
        if 6 <= hour < 12:
            greeting = "Доброе утро"
        elif 12 <= hour < 18:
            greeting = "Добрый день"
        elif 18 <= hour < 23:
            greeting = "Добрый вечер"
        else:
            greeting = "Доброй ночи"

        greeting_label = QLabel(f"{greeting}, {username}!")
        greeting_label.setObjectName("GreetingLabel")
        text_layout.addWidget(greeting_label)

        date_str = datetime.now().strftime("%d %B %Y").lower()
        date_label = QLabel(f"Сегодня {date_str}")
        date_label.setObjectName("DateLabel")
        text_layout.addWidget(date_label)

        desc_label = QLabel("Готов собрать новый ПК?")
        desc_label.setObjectName("WelcomeDesc")
        text_layout.addWidget(desc_label)

        layout.addLayout(text_layout, stretch=1)

        icon_label = QLabel()
        icon_label.setPixmap(
            qta.icon("fa6s.desktop", color="#0078d7").pixmap(QSize(80, 80))
        )
        icon_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(icon_label)

        return frame

    def _build_stats_section(self):
        frame = QFrame()
        frame.setObjectName("SectionFrame")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        header = QLabel("Статистика")
        header.setObjectName("SectionHeader")
        layout.addWidget(header)

        stats_layout = QGridLayout()
        stats_layout.setSpacing(12)

        projects = self.project_manager.get_all_projects()
        total_projects = len(projects)

        prices = []
        for p in projects.values():
            try:
                price = int(p.get("price", 0))
                prices.append(price)
            except (ValueError, TypeError):
                pass

        avg_price = sum(prices) // len(prices) if prices else 0
        max_price = max(prices) if prices else 0

        stats_layout.addWidget(
            StatCard(
                "Всего проектов",
                total_projects,
                "fa6s.folder-open",
                "#0078d7",
            ),
            0,
            0,
        )
        stats_layout.addWidget(
            StatCard(
                "Средняя цена",
                f"{avg_price:,}₽".replace(",", " "),
                "fa6s.chart-line",
                "#2e7d32",
            ),
            0,
            1,
        )
        stats_layout.addWidget(
            StatCard(
                "Макс. цена",
                f"{max_price:,}₽".replace(",", " "),
                "fa6s.trophy",
                "#ff9800",
            ),
            1,
            0,
        )
        stats_layout.addWidget(
            StatCard(
                "Последний проект",
                "Создан недавно" if total_projects > 0 else "Нет проектов",
                "fa6s.clock",
                "#9c27b0",
            ),
            1,
            1,
        )

        layout.addLayout(stats_layout)
        return frame

    def _build_actions_section(self):
        frame = QFrame()
        frame.setObjectName("SectionFrame")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        header = QLabel("Быстрые действия")
        header.setObjectName("SectionHeader")
        layout.addWidget(header)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)

        create_btn = QPushButton("Создать новый проект")
        create_btn.setObjectName("ActionButton")
        create_btn.setIcon(qta.icon("fa6s.plus", color="white"))
        create_btn.setIconSize(QSize(16, 16))
        create_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        create_btn.clicked.connect(self.create_project.emit)
        buttons_layout.addWidget(create_btn)

        projects = self.project_manager.get_all_projects()
        if projects:
            last_id = max(projects.keys(), key=lambda x: int(x))
            last_btn = QPushButton("Открыть последний проект")
            last_btn.setObjectName("ActionButtonSecondary")
            last_btn.setIcon(qta.icon("fa6s.folder-open", color="white"))
            last_btn.setIconSize(QSize(16, 16))
            last_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            last_btn.clicked.connect(lambda: self.open_project.emit(last_id))
            buttons_layout.addWidget(last_btn)

        layout.addLayout(buttons_layout)
        return frame

    def _build_links_section(self):
        frame = QFrame()
        frame.setObjectName("SectionFrame")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        header = QLabel("Полезные ссылки")
        header.setObjectName("SectionHeader")
        layout.addWidget(header)

        links_layout = QGridLayout()
        links_layout.setSpacing(10)

        links = [
            ("DNS Shop", "https://www.dns-shop.ru", "fa6s.bag-shopping"),
            ("Ситилинк", "https://www.citilink.ru", "fa6s.shop"),
            ("Regard", "https://www.regard.ru", "fa6s.microchip"),
            ("Overclockers.ru", "https://overclockers.ru", "fa6s.newspaper"),
            ("Видео обзоры", "https://youtube.com", "fa6s.play"),
            ("PCPartPicker", "https://pcpartpicker.com", "fa6s.building"),
        ]

        for i, (title, url, icon) in enumerate(links):
            row = i // 3
            col = i % 3
            link_card = LinkCard(title, url, icon)
            link_card.clicked.connect(
                lambda u: QDesktopServices.openUrl(QUrl(u))
            )
            links_layout.addWidget(link_card, row, col)

        layout.addLayout(links_layout)
        return frame

    def _build_projects_section(self):
        frame = QFrame()
        frame.setObjectName("SectionFrame")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        header = QLabel("Мои проекты")
        header.setObjectName("SectionHeader")
        header_layout.addWidget(header)

        header_layout.addStretch()

        view_all_btn = QPushButton("Смотреть все  →")
        view_all_btn.setObjectName("ViewAllButton")
        view_all_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        view_all_btn.clicked.connect(self.view_all_projects.emit)
        header_layout.addWidget(view_all_btn)

        layout.addLayout(header_layout)

        projects = self.project_manager.get_all_projects()

        if not projects:
            empty_label = QLabel("У вас пока нет проектов. Создайте первый!")
            empty_label.setObjectName("EmptyProjectsLabel")
            layout.addWidget(empty_label)
        else:
            projects_layout = QGridLayout()
            projects_layout.setSpacing(12)

            sorted_projects = sorted(
                projects.items(), key=lambda x: int(x[0]), reverse=True
            )[:6]

            for i, (pid, pdata) in enumerate(sorted_projects):
                full_name = pdata["name"]

                if len(full_name) > 11:
                    project_name = f"{full_name[:11]}..."
                else:
                    project_name = full_name

                row = i // 3
                col = i % 3
                card = ProjectCardMini(
                    pid,
                    project_name,
                    pdata.get("price", "0")
                )
                card.open_project.connect(self.open_project.emit)
                projects_layout.addWidget(card, row, col)

            layout.addLayout(projects_layout)

        return frame

    def refresh(self):
        """Обновляет данные на дашборде"""
        while self.layout().count():
            item = self.layout().takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._build_ui()

    def _build_footer_section(self):
        """Футер с информацией о проекте и ссылками"""
        frame = QFrame()
        frame.setObjectName("FooterFrame")
        main_layout = QHBoxLayout(frame)
        main_layout.setContentsMargins(25, 15, 25, 15)
        main_layout.setSpacing(20)

        logo_label = GradientLabel(
            text="PCBuilder",
            gradient_colors=["#0041a8", "#0080ff", "#4dc8ff", "#80ecff"],
            font_size=18,
            font_weight=600,
            font_family="JetBrains Mono",
        )
        main_layout.addWidget(
            logo_label,
            alignment=Qt.AlignmentFlag.AlignVCenter,
        )

        main_layout.addStretch()

        center_layout = QHBoxLayout()
        center_layout.setSpacing(15)

        github_link = self._create_footer_link(
            "GitHub", "https://github.com/tylerderden9681-wq/PcBulder",
            "fa6b.github",
        )
        readme_link = self._create_footer_link(
            "О проекте",
            "https://github.com/tylerderden9681-wq/PcBulder"
            "/blob/main/README.md",
            "fa6s.file-lines",
        )

        center_layout.addWidget(github_link)
        center_layout.addWidget(readme_link)

        main_layout.addLayout(center_layout)

        main_layout.addStretch()

        info_layout = QHBoxLayout()
        info_layout.setSpacing(12)

        version_label = QLabel("v1.0.1")
        version_label.setObjectName("FooterVersion")
        info_layout.addWidget(version_label)

        dot1 = QLabel("•")
        dot1.setObjectName("FooterDot")
        info_layout.addWidget(dot1)

        author_label = QLabel("TheKrimDev")
        author_label.setObjectName("FooterAuthor")
        info_layout.addWidget(author_label)

        dot2 = QLabel("•")
        dot2.setObjectName("FooterDot")
        info_layout.addWidget(dot2)

        year_label = QLabel("2026")
        year_label.setObjectName("FooterYear")
        info_layout.addWidget(year_label)

        main_layout.addLayout(info_layout)

        return frame

    def _create_footer_link(self, text, url, icon_name):
        return FooterLink(text, url, icon_name)
