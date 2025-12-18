"""
Script para descargar datos de inversiones de Arequipa.
"""
import os
from download_xls import download_mef_data
from xlsx_to_csv import xlsx_to_csv


# Código de departamento para Arequipa (nuevo formato de la API)
AREQUIPA_CODE = "4"


def main():
    """Descarga datos de inversiones de Arequipa."""
    print("Descargando datos de inversiones de Arequipa...")
    
    output_dir = "data/arequipa"
    os.makedirs(output_dir, exist_ok=True)
    
    # Descargar archivo XLSX
    xlsx_path = download_mef_data(AREQUIPA_CODE, output_dir)
    
    if xlsx_path:
        print(f"Archivo descargado: {xlsx_path}")
        
        # Convertir a CSV
        csv_path = os.path.join(output_dir, "inversiones_arequipa.csv")
        if xlsx_to_csv(xlsx_path, csv_path):
            print(f"Datos disponibles en: {csv_path}")
        else:
            print("Error al convertir a CSV")
    else:
        print("Error al descargar datos de Arequipa")


if __name__ == "__main__":
    main()
