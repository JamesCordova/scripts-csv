"""
Script para descarga masiva de datos de todos los departamentos del Perú.
"""
import os
import argparse
from download_xls import download_mef_data
from xlsx_to_csv import xlsx_to_csv


# Códigos de departamentos del Perú (nuevo formato de la API)
DEPARTMENTS = {
    "1": "Amazonas",
    "2": "Áncash",
    "3": "Apurímac",
    "4": "Arequipa",
    "5": "Ayacucho",
    "6": "Cajamarca",
    "7": "Callao",
    "8": "Cusco",
    "9": "Huancavelica",
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


def download_all(output_dir: str = "data", convert_to_csv: bool = True):
    """
    Descarga datos de todos los departamentos.
    
    Args:
        output_dir: Directorio base de salida
        convert_to_csv: Si True, convierte automáticamente a CSV (default: True)
    """
    os.makedirs(output_dir, exist_ok=True)
    
    successful = 0
    failed = 0
    csv_converted = 0
    
    print(f"\n{'='*60}")
    print(f"Descargando datos de {len(DEPARTMENTS)} departamentos")
    print(f"Conversión a CSV: {'✅ Activada' if convert_to_csv else '❌ Desactivada'}")
    print(f"{'='*60}")
    
    for code, name in DEPARTMENTS.items():
        print(f"\n[{code}/25] Descargando {name}...")
        
        dept_dir = os.path.join(output_dir, name.lower().replace(" ", "_"))
        xlsx_path = download_mef_data(code, dept_dir)
        
        if xlsx_path:
            successful += 1
            
            if convert_to_csv:
                csv_path = os.path.join(dept_dir, f"inversiones_{name.lower().replace(' ', '_')}.csv")
                print(f"   Convirtiendo a CSV (limpiando metadata)...")
                if xlsx_to_csv(xlsx_path, csv_path, auto_clean=True):
                    csv_converted += 1
                    print(f"   ✅ CSV listo: {csv_path}")
                else:
                    print(f"   ⚠️  Error al convertir a CSV")
        else:
            failed += 1
            print(f"   ❌ Error descargando {name}")
    
    print(f"\n{'='*60}")
    print(f"📊 RESUMEN:")
    print(f"   ✅ Descargas exitosas: {successful}/{len(DEPARTMENTS)}")
    print(f"   ❌ Descargas fallidas: {failed}/{len(DEPARTMENTS)}")
    if convert_to_csv:
        print(f"   📄 Archivos CSV generados: {csv_converted}")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(
        description='Descargar datos de inversiones de todos los departamentos del Perú'
    )
    parser.add_argument('--output', '-o', default='data',
                       help='Directorio de salida (default: data)')
    parser.add_argument('--no-csv', action='store_true',
                       help='NO convertir a CSV (solo descargar XLSX)')
    
    args = parser.parse_args()
    
    # Por defecto convierte a CSV, a menos que se use --no-csv
    convert_csv = not args.no_csv
    
    download_all(args.output, convert_csv)


if __name__ == "__main__":
    main()
