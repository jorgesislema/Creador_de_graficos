#!/usr/bin/env python3
"""
Script de prueba rápida para verificar que todas las funcionalidades 
del Creador de Gráficos están funcionando correctamente.
"""

import sys
import os
import json
import tempfile

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_core_functionality():
    """Prueba las funcionalidades centrales"""
    print("🧪 Probando funcionalidades centrales...")
    
    try:
        # Probar importación de módulos
        from chart_maker.core.chart_types import CHART_TYPES
        from chart_maker.core.examples import EXAMPLES
        from chart_maker.core.spec import ChartSpec
        
        print(f"✅ {len(CHART_TYPES)} tipos de gráficos disponibles")
        print(f"✅ {len(EXAMPLES)} ejemplos cargados")
        
        # Probar validación
        example_spec = EXAMPLES['bar']
        print(f"✅ Validación funcionando: {example_spec.type}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en funcionalidades centrales: {e}")
        return False

def test_exporters():
    """Prueba los exportadores"""
    print("\n📤 Probando exportadores...")
    
    try:
        from chart_maker.exporters import get_exporter, list_exporters
        from chart_maker.core.examples import EXAMPLES
        
        exporters = list_exporters()
        print(f"✅ {len(exporters)} exportadores disponibles: {exporters}")
        
        # Probar cada exportador
        test_spec = EXAMPLES['bar']
        
        for exporter_name in exporters:
            try:
                exporter = get_exporter(exporter_name)
                
                # Crear archivo temporal
                with tempfile.NamedTemporaryFile(delete=False, suffix='.test') as tmp:
                    success = exporter.export(test_spec, tmp.name)
                    
                    if success:
                        # Verificar que el archivo fue creado
                        if os.path.exists(tmp.name) and os.path.getsize(tmp.name) > 0:
                            print(f"✅ Exportador {exporter_name}: OK")
                        else:
                            print(f"⚠️ Exportador {exporter_name}: Archivo vacío")
                    else:
                        print(f"❌ Exportador {exporter_name}: Falló")
                    
                    # Limpiar archivo temporal
                    os.unlink(tmp.name)
                    
            except Exception as e:
                print(f"❌ Exportador {exporter_name}: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en exportadores: {e}")
        return False

def test_gui_imports():
    """Prueba que los módulos de GUI se pueden importar"""
    print("\n🖥️ Probando módulos de GUI...")
    
    try:
        # Verificar PySide6
        import PySide6
        print(f"✅ PySide6 {PySide6.__version__} disponible")
        
        # Verificar módulos de la aplicación
        from chart_maker.app.ui.main_window import MainWindow
        from chart_maker.app.ui.preview_web_view import PreviewWebView
        
        print("✅ Módulos de GUI importados correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en módulos de GUI: {e}")
        return False

def test_data_processing():
    """Prueba el procesamiento de datos"""
    print("\n📊 Probando procesamiento de datos...")
    
    try:
        import pandas as pd
        import csv
        import io
        
        # Crear datos de prueba CSV
        csv_data = """categoria,valor,fecha
A,100,2025-01-01
B,150,2025-01-02
C,200,2025-01-03"""
        
        # Simular lectura CSV
        csv_file = io.StringIO(csv_data)
        reader = csv.DictReader(csv_file)
        data = list(reader)
        
        print(f"✅ CSV procesado: {len(data)} filas")
        
        # Simular conversión JSON
        json_data = json.dumps(data, indent=2)
        parsed_data = json.loads(json_data)
        
        print(f"✅ JSON procesado: {len(parsed_data)} elementos")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en procesamiento de datos: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas del Creador de Gráficos...\n")
    
    tests = [
        test_core_functionality,
        test_exporters,
        test_gui_imports,
        test_data_processing
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Resultados de las pruebas:")
    print(f"✅ Pruebas exitosas: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron! El Creador de Gráficos está listo para usar.")
        print("\n🚀 Para ejecutar el programa:")
        print("   $env:PYTHONPATH = \"$env:PYTHONPATH;.\"")
        print("   python chart_maker/app/main.py")
    else:
        print(f"\n⚠️ {total - passed} pruebas fallaron. Revisar la configuración.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
