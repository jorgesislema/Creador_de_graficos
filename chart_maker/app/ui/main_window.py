"""
Ventana principal de la aplicación Chart Maker
"""

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QComboBox, QTextEdit, QPushButton, 
                               QSplitter, QFrame, QScrollArea, QFormLayout,
                               QSpinBox, QCheckBox, QLineEdit, QMessageBox,
                               QFileDialog, QTabWidget, QGroupBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QIcon
import json
import csv
import io
from typing import Dict, Any, Optional

from ...core.chart_types import CHART_TYPES
from ...core.examples_new import EXAMPLES
from ...core.spec import ChartSpec
from ...core.vegalite_mapper import chartspec_to_vegalite
from ...exporters import get_exporter, list_exporters
from .preview_web_view_local import PreviewWebView


class MainWindow(QMainWindow):
    """Ventana principal del creador de gráficos"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Creador de Gráficos - Chart Maker")
        self.setGeometry(100, 100, 1400, 900)
        
        # Variables de estado
        self.current_spec = None
        self.auto_update_timer = QTimer()
        self.auto_update_timer.timeout.connect(self.update_preview)
        self.auto_update_timer.setSingleShot(True)
        
        self.init_ui()
        self.load_example_chart()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal - splitter horizontal
        main_splitter = QSplitter(Qt.Horizontal)
        central_widget_layout = QVBoxLayout()
        central_widget_layout.addWidget(main_splitter)
        central_widget.setLayout(central_widget_layout)
        
        # Panel izquierdo - controles
        self.create_controls_panel(main_splitter)
        
        # Panel derecho - vista previa
        self.create_preview_panel(main_splitter)
        
        # Configurar proporciones del splitter
        main_splitter.setSizes([400, 1000])
        
        # Barra de estado
        self.statusBar().showMessage("Listo para crear gráficos")
    
    def create_controls_panel(self, parent_splitter):
        """Crea el panel de controles"""
        controls_widget = QWidget()
        controls_layout = QVBoxLayout()
        
        # Scroll area para los controles
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        
        # Pestañas para organizar controles
        tab_widget = QTabWidget()
        
        # Pestaña de configuración básica
        basic_tab = self.create_basic_tab()
        tab_widget.addTab(basic_tab, "Básico")
        
        # Pestaña de datos
        data_tab = self.create_data_tab()
        tab_widget.addTab(data_tab, "Datos")
        
        # Pestaña de estilo
        style_tab = self.create_style_tab()
        tab_widget.addTab(style_tab, "Estilo")
        
        scroll_layout.addWidget(tab_widget)
        
        # Botones de acción
        buttons_layout = self.create_action_buttons()
        scroll_layout.addLayout(buttons_layout)
        
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        
        controls_layout.addWidget(scroll_area)
        controls_widget.setLayout(controls_layout)
        
        parent_splitter.addWidget(controls_widget)
    
    def create_basic_tab(self):
        """Crea la pestaña de configuración básica"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Tipo de gráfico
        chart_group = QGroupBox("Tipo de Gráfico")
        chart_layout = QFormLayout()
        
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(CHART_TYPES)
        self.chart_type_combo.currentTextChanged.connect(self.on_chart_type_changed)
        chart_layout.addRow("Tipo:", self.chart_type_combo)
        
        chart_group.setLayout(chart_layout)
        layout.addWidget(chart_group)
        
        # Dimensiones
        dimensions_group = QGroupBox("Dimensiones")
        dimensions_layout = QFormLayout()
        
        self.width_spin = QSpinBox()
        self.width_spin.setRange(100, 2000)
        self.width_spin.setValue(400)
        self.width_spin.valueChanged.connect(self.on_dimension_changed)
        dimensions_layout.addRow("Ancho:", self.width_spin)
        
        self.height_spin = QSpinBox()
        self.height_spin.setRange(100, 2000)
        self.height_spin.setValue(300)
        self.height_spin.valueChanged.connect(self.on_dimension_changed)
        dimensions_layout.addRow("Alto:", self.height_spin)
        
        dimensions_group.setLayout(dimensions_layout)
        layout.addWidget(dimensions_group)
        
        # Opciones generales
        options_group = QGroupBox("Opciones")
        options_layout = QFormLayout()
        
        self.title_edit = QLineEdit()
        self.title_edit.textChanged.connect(self.on_title_changed)
        options_layout.addRow("Título:", self.title_edit)
        
        self.description_edit = QLineEdit()
        self.description_edit.textChanged.connect(self.on_description_changed)
        options_layout.addRow("Descripción:", self.description_edit)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_data_tab(self):
        """Crea la pestaña de datos"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Pestañas para JSON y CSV
        data_tab_widget = QTabWidget()
        
        # Pestaña JSON
        json_tab = QWidget()
        json_layout = QVBoxLayout()
        
        # Editor de datos JSON
        data_group = QGroupBox("Datos (JSON)")
        data_layout = QVBoxLayout()
        
        # Botones de datos de ejemplo
        example_buttons_layout = QHBoxLayout()
        
        load_example_btn = QPushButton("Cargar Ejemplo")
        load_example_btn.clicked.connect(self.load_example_data)
        example_buttons_layout.addWidget(load_example_btn)
        
        load_file_btn = QPushButton("Cargar Archivo JSON")
        load_file_btn.clicked.connect(self.load_data_file)
        example_buttons_layout.addWidget(load_file_btn)
        
        data_layout.addLayout(example_buttons_layout)
        
        # Editor de texto para JSON
        self.data_editor = QTextEdit()
        self.data_editor.setFont(QFont("Courier", 10))
        self.data_editor.textChanged.connect(self.on_data_changed)
        data_layout.addWidget(self.data_editor)
        
        data_group.setLayout(data_layout)
        json_layout.addWidget(data_group)
        json_tab.setLayout(json_layout)
        
        # Pestaña CSV
        csv_tab = QWidget()
        csv_layout = QVBoxLayout()
        
        # Importar CSV
        csv_group = QGroupBox("Importar CSV")
        csv_group_layout = QVBoxLayout()
        
        # Botones para CSV
        csv_buttons_layout = QHBoxLayout()
        
        load_csv_btn = QPushButton("Cargar Archivo CSV")
        load_csv_btn.clicked.connect(self.load_csv_file)
        csv_buttons_layout.addWidget(load_csv_btn)
        
        csv_group_layout.addLayout(csv_buttons_layout)
        
        # Información del CSV cargado
        self.csv_info_label = QLabel("No hay archivo CSV cargado")
        csv_group_layout.addWidget(self.csv_info_label)
        
        # Vista previa del CSV
        self.csv_preview = QTextEdit()
        self.csv_preview.setFont(QFont("Courier", 9))
        self.csv_preview.setReadOnly(True)
        self.csv_preview.setMaximumHeight(200)
        csv_group_layout.addWidget(self.csv_preview)
        
        csv_group.setLayout(csv_group_layout)
        csv_layout.addWidget(csv_group)
        csv_tab.setLayout(csv_layout)
        
        # Agregar pestañas
        data_tab_widget.addTab(json_tab, "JSON")
        data_tab_widget.addTab(csv_tab, "CSV")
        
        layout.addWidget(data_tab_widget)
        tab.setLayout(layout)
        return tab
    
    def create_style_tab(self):
        """Crea la pestaña de estilo"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Colores
        color_group = QGroupBox("Colores")
        color_layout = QFormLayout()
        
        self.color_scheme_combo = QComboBox()
        self.color_scheme_combo.addItems([
            "category10", "category20", "tableau10", "tableau20",
            "blues", "greens", "greys", "reds", "viridis", "plasma"
        ])
        self.color_scheme_combo.currentTextChanged.connect(self.on_style_changed)
        color_layout.addRow("Esquema:", self.color_scheme_combo)
        
        color_group.setLayout(color_layout)
        layout.addWidget(color_group)
        
        # Tema
        theme_group = QGroupBox("Tema")
        theme_layout = QFormLayout()
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([
            "default", "dark", "excel", "fivethirtyeight", 
            "ggplot2", "googlecharts", "latimes", "quartz", "vox"
        ])
        self.theme_combo.currentTextChanged.connect(self.on_style_changed)
        theme_layout.addRow("Tema:", self.theme_combo)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_action_buttons(self):
        """Crea los botones de acción"""
        layout = QVBoxLayout()
        
        # Botones de vista previa
        preview_group = QGroupBox("Vista Previa")
        preview_layout = QVBoxLayout()
        
        update_btn = QPushButton("Actualizar Vista Previa")
        update_btn.clicked.connect(self.update_preview)
        preview_layout.addWidget(update_btn)
        
        clear_btn = QPushButton("Limpiar Vista Previa")
        clear_btn.clicked.connect(self.clear_preview)
        preview_layout.addWidget(clear_btn)
        
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)
        
        # Botones de exportación
        export_group = QGroupBox("Exportar")
        export_layout = QVBoxLayout()
        
        export_json_btn = QPushButton("Exportar JSON")
        export_json_btn.clicked.connect(self.export_json)
        export_layout.addWidget(export_json_btn)
        
        # Separador
        export_layout.addWidget(QLabel("--- Plataformas ---"))
        
        # Power BI
        export_powerbi_btn = QPushButton("Exportar para Power BI (.pbiviz)")
        export_powerbi_btn.clicked.connect(lambda: self.export_to_platform('powerbi_python'))
        export_layout.addWidget(export_powerbi_btn)
        
        # Tableau
        export_tableau_btn = QPushButton("Exportar para Tableau (.twb)")
        export_tableau_btn.clicked.connect(lambda: self.export_to_platform('tableau'))
        export_layout.addWidget(export_tableau_btn)
        
        # Tableau con datos
        export_tableau_twbx_btn = QPushButton("Exportar para Tableau (.twbx)")
        export_tableau_twbx_btn.clicked.connect(lambda: self.export_to_platform_with_extension('tableau', '.twbx'))
        export_layout.addWidget(export_tableau_twbx_btn)
        
        # Looker
        export_looker_btn = QPushButton("Exportar para Looker")
        export_looker_btn.clicked.connect(lambda: self.export_to_platform('looker'))
        export_layout.addWidget(export_looker_btn)
        
        # Looker Studio
        export_looker_studio_btn = QPushButton("Exportar para Looker Studio")
        export_looker_studio_btn.clicked.connect(lambda: self.export_to_platform('looker_studio'))
        export_layout.addWidget(export_looker_studio_btn)
        
        export_group.setLayout(export_layout)
        layout.addWidget(export_group)
        
        return layout
    
    def create_preview_panel(self, parent_splitter):
        """Crea el panel de vista previa"""
        preview_widget = QWidget()
        preview_layout = QVBoxLayout()
        
        # Encabezado
        header_layout = QHBoxLayout()
        header_label = QLabel("Vista Previa")
        header_label.setFont(QFont("Arial", 12, QFont.Bold))
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        
        preview_layout.addLayout(header_layout)
        
        # Vista web para el gráfico
        self.preview_web_view = PreviewWebView()
        preview_layout.addWidget(self.preview_web_view)
        
        preview_widget.setLayout(preview_layout)
        parent_splitter.addWidget(preview_widget)
    
    def load_example_chart(self):
        """Carga un gráfico de ejemplo al iniciar"""
        example_type = "bar"
        if example_type in EXAMPLES:
            example_spec = EXAMPLES[example_type]
            self.load_chart_spec(example_spec)
    
    def load_chart_spec(self, spec: ChartSpec):
        """Carga una especificación de gráfico en los controles"""
        try:
            # Actualizar controles con la especificación
            if spec.type in CHART_TYPES:
                self.chart_type_combo.setCurrentText(spec.type)
            
            if spec.title:
                self.title_edit.setText(spec.title)
            
            if spec.description:
                self.description_edit.setText(spec.description)
            
            if spec.width:
                self.width_spin.setValue(spec.width)
            
            if spec.height:
                self.height_spin.setValue(spec.height)
            
            # Cargar datos en el editor
            if spec.data:
                data_json = json.dumps(spec.data, indent=2, ensure_ascii=False)
                self.data_editor.setPlainText(data_json)
            
            self.current_spec = spec
            self.update_preview()
            
        except Exception as e:
            self.show_error(f"Error al cargar la especificación: {e}")
    
    def on_chart_type_changed(self):
        """Maneja el cambio de tipo de gráfico"""
        chart_type = self.chart_type_combo.currentText()
        
        # Cargar ejemplo del nuevo tipo
        if chart_type in EXAMPLES:
            example_spec = EXAMPLES[chart_type]
            self.load_chart_spec(example_spec)
        else:
            self.schedule_update()
    
    def on_dimension_changed(self):
        """Maneja el cambio de dimensiones"""
        self.schedule_update()
    
    def on_title_changed(self):
        """Maneja el cambio de título"""
        self.schedule_update()
    
    def on_description_changed(self):
        """Maneja el cambio de descripción"""
        self.schedule_update()
    
    def on_data_changed(self):
        """Maneja el cambio de datos"""
        self.schedule_update()
    
    def on_style_changed(self):
        """Maneja el cambio de estilo"""
        self.schedule_update()
    
    def schedule_update(self):
        """Programa una actualización de la vista previa"""
        self.auto_update_timer.stop()
        self.auto_update_timer.start(500)  # Actualizar después de 500ms de inactividad
    
    def update_preview(self):
        """Actualiza la vista previa del gráfico"""
        try:
            # Construir especificación actual
            spec = self.build_current_spec()
            
            if spec:
                # Mapear ChartSpec canónico → Vega-Lite para la vista previa
                vega_spec = chartspec_to_vegalite(spec)
                # Actualizar vista previa con Vega-Lite
                self.preview_web_view.update_chart(vega_spec)
                # Guardar la especificación canónica como estado actual
                self.current_spec = ChartSpec(**spec)
                self.statusBar().showMessage("Vista previa actualizada")
            
        except Exception as e:
            self.show_error(f"Error al actualizar vista previa: {e}")
            self.statusBar().showMessage(f"Error: {e}")
    
    def build_current_spec(self) -> Optional[Dict[str, Any]]:
        """Construye la especificación ChartSpec canónica basada en los controles"""
        try:
            # Especificación canónica base
            spec: Dict[str, Any] = {
                "type": self.chart_type_combo.currentText(),
                "width": self.width_spin.value(),
                "height": self.height_spin.value(),
                "encoding": {},
                "options": {}
            }
            
            # Título y descripción
            title = self.title_edit.text().strip()
            if title:
                spec["title"] = title
            
            description = self.description_edit.text().strip()
            if description:
                spec["description"] = description
            
            # Datos
            try:
                data_text = self.data_editor.toPlainText().strip()
                if data_text:
                    data = json.loads(data_text)
                    # Aceptar tanto lista de dicts como dict (e.g., {"values": [...]}, {"url": "..."})
                    spec["data"] = data
                else:
                    # Datos de ejemplo por defecto
                    spec["data"] = [
                        {"x": "A", "y": 10},
                        {"x": "B", "y": 20},
                        {"x": "C", "y": 15}
                    ]
            except json.JSONDecodeError as e:
                raise ValueError(f"JSON de datos inválido: {e}")
            
            # Encoding básico por defecto (canónico)
            if not spec.get("encoding"):
                spec["encoding"] = {
                    "x": {"field": "x", "type": "nominal"},
                    "y": {"field": "y", "type": "quantitative"}
                }
            
            # Opciones de estilo (canónicas)
            options: Dict[str, Any] = {}
            theme = self.theme_combo.currentText()
            if theme and theme != "default":
                options["theme"] = theme
            color_scheme = self.color_scheme_combo.currentText()
            if color_scheme:
                options["colorScheme"] = color_scheme
            if options:
                spec["options"] = options
            
            return spec
            
        except Exception as e:
            raise ValueError(f"Error al construir especificación: {e}")
    
    def clear_preview(self):
        """Limpia la vista previa"""
        self.preview_web_view.clear_preview()
        self.statusBar().showMessage("Vista previa limpiada")
    
    def load_example_data(self):
        """Carga datos de ejemplo"""
        example_data = {
            "values": [
                {"category": "A", "value": 28, "group": "X"},
                {"category": "B", "value": 55, "group": "Y"},
                {"category": "C", "value": 43, "group": "X"},
                {"category": "D", "value": 91, "group": "Y"},
                {"category": "E", "value": 81, "group": "X"},
                {"category": "F", "value": 53, "group": "Y"}
            ]
        }
        
        data_json = json.dumps(example_data, indent=2, ensure_ascii=False)
        self.data_editor.setPlainText(data_json)
    
    def load_data_file(self):
        """Carga datos desde un archivo"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Cargar Datos", 
            "", 
            "JSON Files (*.json);;CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    if file_path.endswith('.json'):
                        data = json.load(file)
                        data_json = json.dumps(data, indent=2, ensure_ascii=False)
                        self.data_editor.setPlainText(data_json)
                    elif file_path.endswith('.csv'):
                        # TODO: Implementar carga de CSV
                        self.show_info("Carga de CSV no implementada aún")
                    
                self.statusBar().showMessage(f"Datos cargados desde: {file_path}")
                
            except Exception as e:
                self.show_error(f"Error al cargar archivo: {e}")
    
    def load_csv_file(self):
        """Carga datos desde un archivo CSV"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Cargar CSV", 
            "", 
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            try:
                # Leer el CSV
                with open(file_path, 'r', encoding='utf-8') as file:
                    # Detectar el dialecto del CSV
                    sample = file.read(1024)
                    file.seek(0)
                    sniffer = csv.Sniffer()
                    dialect = sniffer.sniff(sample)
                    
                    # Leer los datos
                    reader = csv.DictReader(file, dialect=dialect)
                    data = []
                    
                    for row in reader:
                        # Convertir valores numéricos
                        converted_row = {}
                        for key, value in row.items():
                            # Intentar convertir a número
                            try:
                                if '.' in value:
                                    converted_row[key] = float(value)
                                else:
                                    converted_row[key] = int(value)
                            except ValueError:
                                # Mantener como string
                                converted_row[key] = value
                        data.append(converted_row)
                
                # Actualizar la información del CSV
                num_rows = len(data)
                num_cols = len(data[0].keys()) if data else 0
                self.csv_info_label.setText(f"CSV cargado: {num_rows} filas, {num_cols} columnas")
                
                # Mostrar vista previa
                preview_text = self._generate_csv_preview(data)
                self.csv_preview.setPlainText(preview_text)
                
                # Convertir a JSON y actualizar el editor
                data_json = json.dumps(data, indent=2, ensure_ascii=False)
                self.data_editor.setPlainText(data_json)
                
                self.statusBar().showMessage(f"CSV cargado desde: {file_path}")
                self.show_info(f"CSV cargado exitosamente:\n{num_rows} filas, {num_cols} columnas")
                
            except Exception as e:
                self.show_error(f"Error al cargar CSV: {e}")
    
    def _generate_csv_preview(self, data):
        """Genera una vista previa del CSV"""
        if not data:
            return "No hay datos para mostrar"
        
        # Mostrar las primeras 5 filas
        preview_data = data[:5]
        
        # Crear tabla de texto
        output = io.StringIO()
        
        # Headers
        headers = list(preview_data[0].keys())
        header_line = " | ".join(f"{h:>12}" for h in headers)
        output.write(header_line + "\n")
        output.write("-" * len(header_line) + "\n")
        
        # Filas
        for row in preview_data:
            values = [str(row.get(h, ""))[:12] for h in headers]
            row_line = " | ".join(f"{v:>12}" for v in values)
            output.write(row_line + "\n")
        
        if len(data) > 5:
            output.write(f"\n... y {len(data) - 5} filas más")
        
        return output.getvalue()
    
    def export_json(self):
        """Exporta la especificación actual como JSON"""
        try:
            spec = self.build_current_spec()
            if not spec:
                self.show_error("No hay especificación válida para exportar")
                return
            
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Exportar JSON",
                "chart_spec.json",
                "JSON Files (*.json);;All Files (*)"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(spec, file, indent=2, ensure_ascii=False)
                
                self.statusBar().showMessage(f"JSON exportado a: {file_path}")
                self.show_info(f"Especificación exportada exitosamente a:\n{file_path}")
                
        except Exception as e:
            self.show_error(f"Error al exportar JSON: {e}")
    
    def export_to_platform(self, platform: str):
        """Exporta el gráfico a una plataforma específica"""
        try:
            spec = self.build_current_spec()
            if not spec:
                self.show_error("No hay especificación válida para exportar")
                return
            
            # Determinar extensión de archivo según la plataforma
            extensions = {
                'powerbi_python': ('.pbiviz', 'Power BI Visual (*.pbiviz)'),
                'tableau': ('.twb', 'Tableau Workbook (*.twb)'),
                'looker': ('.lkml', 'LookML Files (*.lkml)'),
                'looker_studio': ('.json', 'Looker Studio Config (*.json)')
            }
            
            if platform not in extensions:
                self.show_error(f"Plataforma no soportada: {platform}")
                return
            
            ext, filter_text = extensions[platform]
            
            # Obtener nombre de archivo sugerido
            platform_names = {
                'powerbi_python': 'power_bi_visual',
                'tableau': 'tableau_workbook',
                'looker': 'looker_model',
                'looker_studio': 'looker_studio_config'
            }
            
            suggested_name = f"{platform_names[platform]}{ext}"
            
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                f"Exportar para {platform.replace('_', ' ').title()}",
                suggested_name,
                f"{filter_text};;All Files (*)"
            )
            
            if file_path:
                # Obtener el exportador
                exporter = get_exporter(platform)
                
                # Crear ChartSpec object
                chart_spec = ChartSpec(**spec)
                
                # Exportar
                success = exporter.export(chart_spec, file_path)
                
                if success:
                    self.statusBar().showMessage(f"Exportado para {platform} a: {file_path}")
                    self.show_info(f"Gráfico exportado exitosamente para {platform.replace('_', ' ').title()}:\n{file_path}")
                else:
                    self.show_error(f"Error al exportar para {platform}")
                
        except Exception as e:
            self.show_error(f"Error al exportar para {platform}: {e}")
    
    def export_to_platform_with_extension(self, platform: str, extension: str):
        """Exporta el gráfico a una plataforma específica con extensión personalizada"""
        try:
            spec = self.build_current_spec()
            if not spec:
                self.show_error("No hay especificación válida para exportar")
                return
            
            # Nombres de archivos según extensión
            if extension == '.twbx':
                filter_text = 'Tableau Packaged Workbook (*.twbx)'
                suggested_name = 'tableau_packaged_workbook.twbx'
            else:
                return self.export_to_platform(platform)
            
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                f"Exportar para {platform.replace('_', ' ').title()} ({extension})",
                suggested_name,
                f"{filter_text};;All Files (*)"
            )
            
            if file_path:
                # Asegurar que termine con la extensión correcta
                if not file_path.endswith(extension):
                    file_path += extension
                    
                # Obtener el exportador
                exporter = get_exporter(platform)
                
                # Crear ChartSpec object
                chart_spec = ChartSpec(**spec)
                
                # Exportar
                success = exporter.export(chart_spec, file_path)
                
                if success:
                    self.statusBar().showMessage(f"Exportado para {platform} a: {file_path}")
                    self.show_info(f"Gráfico exportado exitosamente para {platform.replace('_', ' ').title()}:\\n{file_path}")
                else:
                    self.show_error(f"Error al exportar para {platform}")
                
        except Exception as e:
            self.show_error(f"Error al exportar para {platform}: {e}")

    def show_error(self, message: str):
        """Muestra un mensaje de error"""
        QMessageBox.critical(self, "Error", message)
    
    def show_info(self, message: str):
        """Muestra un mensaje informativo"""
        QMessageBox.information(self, "Información", message)
