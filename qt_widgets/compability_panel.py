import qtawesome as qta
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout
from PyQt6.QtCore import QSize


class CompatibilityPanel(QFrame):
    """Панель для отображения ошибок и предупреждений совместимости"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CompatibilityPanel")
        self.setVisible(False)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 12, 15, 12)
        self.main_layout.setSpacing(8)

        self.header = QLabel()
        self.header.setObjectName("CompatibilityHeader")
        self.main_layout.addWidget(self.header)

        self.issues_widget = QWidget()
        self.issues_layout = QVBoxLayout(self.issues_widget)
        self.issues_layout.setContentsMargins(0, 0, 0, 0)
        self.issues_layout.setSpacing(6)
        self.main_layout.addWidget(self.issues_widget)

    def update_issues(self, issues: list):
        """
        Принимает список проблем от CompatibilityChecker
        и отрисовывает их
        """
        while self.issues_layout.count():
            item = self.issues_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not issues:
            self.setVisible(False)
            return

        self.setVisible(True)
        has_errors = any(issue.get("type") == "error" for issue in issues)

        if has_errors:
            self.header.setText("⚠️ Обнаружены критические ошибки:")
            self.header.setProperty("status", "error")
        else:
            self.header.setText("⚠️ Есть предупреждения:")
            self.header.setProperty("status", "warning")

        self.header.style().unpolish(self.header)
        self.header.style().polish(self.header)

        for issue in issues:
            self.issues_layout.addWidget(self._create_issue_row(issue))

    def _create_issue_row(self, issue: dict) -> QFrame:
        """Создает одну строку с иконкой и текстом проблемы"""
        row = QFrame()
        is_error = issue.get("type") == "error"

        row.setObjectName("IssueError" if is_error else "IssueWarning")

        layout = QHBoxLayout(row)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(10)

        # Иконка
        icon = QLabel()
        icon_color = "#dc3545" if is_error else "#ff9800"
        icon_name = "fa6s.circle-xmark" if is_error else (
            "fa6s.triangle-exclamation"
        )
        icon.setPixmap(qta.icon(
            icon_name,
            color=icon_color
        ).pixmap(QSize(18, 18)))
        layout.addWidget(icon)

        text = QLabel(issue.get("message", "Неизвестная ошибка"))
        text.setObjectName("IssueText")
        text.setWordWrap(True)
        layout.addWidget(text, stretch=1)

        return row

    def has_critical_errors(self) -> bool:
        """
        Возвращает True, если есть критические ошибки (type='error')
        """
        for i in range(self.issues_layout.count()):
            item = self.issues_layout.itemAt(i)
            if item and item.widget():
                if item.widget().objectName() == "IssueError":
                    return True
        return False

    def has_any_issues(self) -> bool:
        """
        Возвращает True, если есть любые проблемы (ошибки или предупреждения)
        """
        return self.isVisible() and self.issues_layout.count() > 0
