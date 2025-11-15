# Peru Investment Data Downloader

Scripts para descargar y procesar datos de inversiones del portal del Ministerio de Economía y Finanzas del Perú (MEF).

## Descripción

Este proyecto automatiza la descarga de datos de inversiones públicas desde el portal ofi5.mef.gob.pe y los convierte a formatos fáciles de analizar.

## Características

- Descarga de archivos XLSX desde la API del MEF
- Conversión automática de XLSX a CSV
- Auto-detección y limpieza de metadata
- Descarga masiva por departamentos
- Scripts especializados por región

## Instalación

```bash
pip install requests openpyxl
```

## Uso

### Descargar datos de Arequipa
```bash
python download_arequipa.py
```

### Descargar todos los departamentos del Perú
```bash
python download_all_departments.py --csv
```

### Convertir XLSX a CSV
```bash
python xlsx_to_csv.py archivo.xlsx -o salida.csv
```

## Estructura del Proyecto

- `download_xls.py` - Módulo base para descargas
- `xlsx_to_csv.py` - Conversor XLSX a CSV con limpieza automática
- `download_all_departments.py` - Descarga masiva de todos los departamentos
- `download_arequipa.py` - Script específico para Arequipa

## Licencia

MIT
