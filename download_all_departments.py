"""
Script para descarga masiva de datos de todos los departamentos del Perú.
"""
import os
import argparse
from download_xls import download_mef_data
from xlsx_to_csv import xlsx_to_csv


# Códigos UBIGEO de departamentos del Perú
DEPARTMENTS = {
    "01": "Amazonas",
    "02": "Áncash",
    "03": "Apurímac",
    "04": "Arequipa",
    "05": "Ayacucho",
    "06": "Cajamarca",
    "07": "Callao",
    "08": "Cusco",
    "09": "Huancavelica",
    "10": "Huánuco",
    "11": "Ica",
    "12": "Junín",
    "13": "La Libertad",
    "14": "Lambayeque",
    "15": "Lima",
    "16": "Loreto",
    "17": "Madre de Dios",
    "18": "Moquegua",
    "19": "Pasco",
    "20": "Piura",
    "21": "Puno",
    "22": "San Martín",
    "23": "Tacna",
    "24": "Tumbes",
    "25": "Ucayali"
}


def download_all(output_dir: str = "data", convert_to_csv: bool = False):
    """
    Descarga datos de todos los departamentos.
    
    Args:
        output_dir: Directorio base de salida
        convert_to_csv: Si True, convierte automáticamente a CSV
    """
    os.makedirs(output_dir, exist_ok=True)
    
    successful = 0
    failed = 0
    
    for code, name in DEPARTMENTS.items():
        print(f"\n[{code}] Descargando {name}...")
        
        dept_dir = os.path.join(output_dir, name.lower().replace(" ", "_"))
        xlsx_path = download_mef_data(code, dept_dir)
        
        if xlsx_path:
            successful += 1
            
            if convert_to_csv:
                csv_path = os.path.join(dept_dir, f"inversiones_{name.lower()}.csv")
                xlsx_to_csv(xlsx_path, csv_path)
        else:
            failed += 1
            print(f"✗ Error descargando {name}")
    
    print(f"\n{'='*50}")
    print(f"Resumen: {successful} exitosos, {failed} fallidos")
    print(f"{'='*50}")


def main():
    parser = argparse.ArgumentParser(
        description='Descargar datos de inversiones de todos los departamentos del Perú'
    )
    parser.add_argument('--output', '-o', default='data',
                       help='Directorio de salida (default: data)')
    parser.add_argument('--csv', action='store_true',
                       help='Convertir automáticamente a CSV')
    
    args = parser.parse_args()
    
    download_all(args.output, args.csv)


if __name__ == "__main__":
    main()
