# Peru Investment Data Downloader

Scripts para descargar y procesar datos de inversiones del portal del Ministerio de Economía y Finanzas del Perú (MEF).

## Descripción

Este proyecto automatiza la descarga de datos de inversiones públicas desde el portal ofi5.mef.gob.pe utilizando la API oficial del MEF y los convierte a formatos fáciles de analizar.

**Última actualización**: Diciembre 2024 - Actualizado a la nueva API del MEF

## Características

- Descarga de archivos XLSX desde la API del MEF
- Conversión automática de XLSX a CSV
- **Auto-detección y limpieza de metadata** (elimina filas antes del header "CUI")
- Descarga masiva por departamentos
- Scripts especializados por región
- CSV limpio listo para análisis (comienza directamente con los datos)

## Instalación

```bash
pip install -r requirements.txt
```

O instalar manualmente:
```bash
pip install requests openpyxl
```

## Uso

### Descargar datos de Arequipa
```bash
python download_arequipa.py
```
Crea la carpeta `data/arequipa/` con el archivo XLSX y CSV.

### Descargar todos los departamentos del Perú
```bash
# Solo XLSX
python download_all_departments.py

# XLSX + CSV
python download_all_departments.py --csv

# Especificar directorio de salida
python download_all_departments.py --output mi_carpeta --csv
```

### Convertir XLSX a CSV
```bash
python xlsx_to_csv.py archivo.xlsx -o salida.csv

# Sin limpieza automática de metadata
python xlsx_to_csv.py archivo.xlsx --no-clean
```

## Pruebas

Para verificar que todo funciona correctamente después de la actualización:

```bash
# Prueba completa automatizada (recomendado)
python tmp_rovodev_test_all.py

# Prueba rápida (solo Arequipa)
python tmp_rovodev_test_quick.py
```

Ver [TESTING.md](TESTING.md) para guía completa de pruebas.

## Estructura del Proyecto

### Scripts Principales
- `download_xls.py` - Módulo base para descargas desde la API del MEF
- `xlsx_to_csv.py` - Conversor XLSX a CSV con limpieza automática de metadata
- `download_all_departments.py` - Descarga masiva de todos los departamentos (25)
- `download_arequipa.py` - Script específico para Arequipa

### Archivos de Configuración
- `requirements.txt` - Dependencias del proyecto
- `README.md` - Documentación principal
- `TESTING.md` - Guía de pruebas

### Scripts de Prueba (temporales)
- `tmp_rovodev_test_all.py` - Suite de pruebas completa
- `tmp_rovodev_test_quick.py` - Prueba rápida de descarga

## API del MEF

**Endpoint actual**: `https://ofi5.mef.gob.pe/inviertews/Ssi/expRepSSIDet`  
**Método**: POST  
**Formato**: JSON

### Parámetros
```json
{
  "sect": "",           // Sector (vacío para todos)
  "plie": "4",         // Código de departamento (1-25)
  "dpto": 0,           // Filtro provincia (0 = todas)
  "prov": 0,           // Filtro provincia (0 = todas)
  "dist": 0,           // Filtro distrito (0 = todos)
  "tipo": "GR"         // Tipo de gobierno (GR = Gobierno Regional)
}
```

### Códigos de Departamentos
Ver tabla completa en [TESTING.md](TESTING.md#-códigos-de-departamentos)

## Licencia

MIT
