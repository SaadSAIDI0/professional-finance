BG = "#0F172A"
PANEL = "#111827"
CARD = "#1E293B"
TEXT = "#F8FAFC"
MUTED = "#94A3B8"
BLUE = "#3B82F6"
GREEN = "#22C55E"
RED = "#EF4444"
BORDER = "#334155"


APP_STYLESHEET = f"""
QWidget {{
    color: {TEXT};
    font-family: Segoe UI, Arial;
}}

QWidget#dashboard {{
    background-color: {BG};
}}

QLabel {{
    background-color: transparent;
}}

QFrame#sidePanel {{
    background-color: {BG};
}}

QFrame#authPanel {{
    background-color: {PANEL};
}}

QFrame#card {{
    background-color: {CARD};
    border: 1px solid {BORDER};
    border-radius: 22px;
}}

QFrame#topBar {{
    background-color: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 18px;
}}

QFrame#logoBadge {{
    background-color: {BLUE};
    border-radius: 14px;
}}

QFrame#settingsPanel {{
    background-color: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 18px;
}}

QFrame#sidebar {{
    background-color: {PANEL};
    border-right: 1px solid {BORDER};
}}

QFrame#contentPanel {{
    background-color: {BG};
}}

QFrame#dividerLine {{
    background-color: {BORDER};
}}

QLabel#heroTitle {{
    color: {TEXT};
    font-size: 42px;
    font-weight: 800;
}}

QLabel#screenTitle {{
    color: {TEXT};
    font-size: 30px;
    font-weight: 800;
}}

QLabel#muted {{
    color: {MUTED};
    font-size: 14px;
}}

QLabel#metricValue {{
    color: {TEXT};
    font-size: 28px;
    font-weight: 800;
}}

QLineEdit, QComboBox {{
    background-color: #0B1220;
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 11px 13px;
    color: {TEXT};
    font-size: 14px;
}}

QLineEdit:focus, QComboBox:focus {{
    border: 1px solid {BLUE};
}}

QPushButton#primaryButton {{
    background-color: {BLUE};
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px;
    font-size: 15px;
    font-weight: 700;
}}

QPushButton#primaryButton:hover {{
    background-color: #2563EB;
}}

QPushButton#primaryButton:pressed {{
    background-color: #1d4ed8;
}}

QPushButton#textButton {{
    background-color: transparent;
    color: {BLUE};
    border: none;
    font-size: 14px;
    font-weight: 700;
}}

QPushButton#textButton:hover {{
    color: #60a5fa;
}}

QPushButton#secondaryButton {{
    background-color: {CARD};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 10px;
    font-size: 14px;
    font-weight: 700;
}}

QPushButton#secondaryButton:hover {{
    background-color: #273449;
}}

QPushButton#navButton {{
    background-color: transparent;
    color: {MUTED};
    border: none;
    border-radius: 12px;
    padding: 12px;
    text-align: left;
    font-size: 14px;
    font-weight: 700;
}}

QPushButton#navButton:hover {{
    background-color: {CARD};
    color: {TEXT};
}}

QPushButton#dangerButton {{
    background-color: rgba(239, 68, 68, 0.1);
    color: {RED};
    border: 1px solid {RED};
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 13px;
    font-weight: 600;
}}

QPushButton#dangerButton:hover {{
    background-color: rgba(239, 68, 68, 0.2);
    border: 1px solid #dc2626;
}}

QPushButton#dangerButton:pressed {{
    background-color: rgba(239, 68, 68, 0.3);
}}

QCheckBox {{
    color: {MUTED};
    background-color: transparent;
    font-size: 13px;
}}

QTableWidget {{
    background-color: {CARD};
    border: 1px solid {BORDER};
    gridline-color: {BORDER};
    color: {TEXT};
}}

QTableWidget::item {{
    padding: 8px;
}}

QTableWidget::item:selected {{
    background-color: {BLUE};
}}

QHeaderView::section {{
    background-color: #273449;
    color: {TEXT};
    border: none;
    padding: 8px;
    font-weight: 600;
}}
"""
