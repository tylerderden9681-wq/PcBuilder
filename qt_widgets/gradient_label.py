from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import (
    QPainter,
    QLinearGradient,
    QFont,
    QColor,
    QPainterPath,
)
from PyQt6.QtCore import Qt


class GradientLabel(QLabel):
    """
    QLabel с настоящим градиентным текстом через QPainterPath.
    """

    def __init__(
        self,
        text: str,
        gradient_colors: list[str],
        font_size: int = 20,
        font_weight: int = 800,
        font_family: str = "Nunito",
        parent=None,
    ):
        super().__init__(text, parent)
        self._gradient_colors = [QColor(c) for c in gradient_colors]
        self._font_size = font_size
        self._font_weight = font_weight
        self._font_family = font_family

        self.setMinimumHeight(font_size + 15)
        self.setMinimumWidth(150)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        font = QFont(self._font_family)
        font.setPointSize(self._font_size)
        font.setWeight(self._font_weight)
        painter.setFont(font)

        path = QPainterPath()
        path.addText(0, 0, font, self.text())

        text_rect = path.boundingRect()
        text_width = text_rect.width()
        text_height = text_rect.height()

        x_offset = 0
        y_offset = (self.height() + text_height) / 2 - text_rect.bottom()

        path.translate(x_offset, y_offset)

        gradient = QLinearGradient(0, 0, text_width, 0)
        for i, color in enumerate(self._gradient_colors):
            position = i / max(len(self._gradient_colors) - 1, 1)
            gradient.setColorAt(position, color)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(gradient)
        painter.drawPath(path)

        painter.end()
