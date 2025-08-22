# preview_webview.py
# Componente para previsualizar gráficos usando un WebView

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget, QVBoxLayout

class PreviewWebView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.webview = QWebEngineView()
        layout.addWidget(self.webview)
        self.setLayout(layout)

    def load_html(self, html: str):
        self.webview.setHtml(html)
