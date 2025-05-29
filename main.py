import sys
import json
import psutil
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLabel, QSizePolicy,
    QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QColor
from system_stats import get_system_stats


max_columns = 3
spacing = 8
padding = 10


class ClickableIconWidget(QWidget):
    def __init__(self, icon_path, command, tooltip_text="", size=(80, 80), parent=None):
        super().__init__(parent)
        self.command = command
        self.setFixedSize(*size)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip(tooltip_text)

        self.label = QLabel(self)
        self.label.setFixedSize(*size)
        self.label.setScaledContents(True)

        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            print(f"Warning: Failed to load image from {icon_path}")
        self.label.setPixmap(pixmap)

        self.apply_shadow()

    def apply_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(shadow)

    def mousePressEvent(self, event):
        if self.command:
            try:
                subprocess.Popen(self.command.split())
            except Exception as e:
                print(f"Failed to run command '{self.command}': {e}")
        super().mousePressEvent(event)


class WidgetDashboard(QWidget):
    def __init__(self, config_path):
        super().__init__()

        # Load external QSS for styling
        with open("/home/pluto/Desktop/py-widget/themes/glass.qs", "r") as f:
            self.setStyleSheet(f.read())

        # Load widgets config
        with open(config_path, "r") as f:
            self.config = json.load(f)

        self.amount_of_widgets = len(self.config)
        self.max_columns = max_columns
        self.spacing = spacing
        self.padding = padding

        self.calculate_grid_size()

        self.setWindowTitle("RiceDashboard")
        self.setFixedSize(self.window_width, self.window_height)
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.layout = QGridLayout()
        self.layout.setSpacing(self.spacing)
        self.layout.setContentsMargins(
            self.padding, self.padding, self.padding, self.padding)
        self.layout.setAlignment(Qt.AlignCenter)

        self.widgets = []
        self.create_widgets()

        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)
        self.update_stats()

        self.old_pos = None

    def calculate_grid_size(self):
        rows = (self.amount_of_widgets +
                self.max_columns - 1) // self.max_columns
        columns = min(self.amount_of_widgets, self.max_columns)

        self.max_col_widths = [0] * columns
        for col in range(columns):
            for row in range(rows):
                idx = row * self.max_columns + col
                if idx < self.amount_of_widgets:
                    w, h = self.config[idx]["size"]
                    if w > self.max_col_widths[col]:
                        self.max_col_widths[col] = w

        self.max_row_heights = [0] * rows
        for row in range(rows):
            for col in range(columns):
                idx = row * self.max_columns + col
                if idx < self.amount_of_widgets:
                    w, h = self.config[idx]["size"]
                    if h > self.max_row_heights[row]:
                        self.max_row_heights[row] = h

        self.window_width = sum(self.max_col_widths) + \
            self.spacing * (columns - 1) + self.padding * 2
        self.window_height = sum(self.max_row_heights) + \
            self.spacing * (rows - 1) + self.padding * 2

    def create_widgets(self):
        rows = (self.amount_of_widgets +
                self.max_columns - 1) // self.max_columns
        columns = min(self.amount_of_widgets, self.max_columns)

        for i, cfg in enumerate(self.config):
            row = i // self.max_columns
            col = i % self.max_columns

            w = self.max_col_widths[col]
            h = self.max_row_heights[row]

            if cfg["type"] == "icon":
                widget = ClickableIconWidget(
                    icon_path=cfg["icon_path"],
                    command=cfg.get("command", ""),
                    tooltip_text=cfg.get("tooltip", ""),
                    size=(w, h)
                )
            else:  # type "label"
                text = cfg.get("text", f"Widget {i+1}")
                widget = QLabel(text)
                widget.original_text = text
                widget.setMinimumSize(w, h)
                widget.setMaximumSize(w, h)
                widget.setAlignment(Qt.AlignCenter)
                widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

                # Drop shadow for labels too
                shadow = QGraphicsDropShadowEffect()
                shadow.setBlurRadius(20)
                shadow.setOffset(0, 6)
                shadow.setColor(QColor(0, 0, 0, 160))
                widget.setGraphicsEffect(shadow)

            self.layout.addWidget(widget, row, col, alignment=Qt.AlignCenter)
            self.widgets.append(widget)

    def update_stats(self):
        cpu, ram, battery_percent = get_system_stats()

        stats = [
            f"🧠 {cpu}%",
            f"📦 {ram}%",
            f"🔋 {battery_percent if battery_percent >= 0 else 'N/A'}%",
            "🌐 N/A",
            "💾 N/A",
        ]

        label_widgets = [w for w in self.widgets if isinstance(w, QLabel)]

        for i, widget in enumerate(label_widgets):
            if i < len(stats):
                widget.setText(stats[i])
            else:
                widget.setText(
                    getattr(widget, "original_text", f"Widget {i+1}"))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = WidgetDashboard("widgets_config.json")
    dashboard.show()
    sys.exit(app.exec_())
