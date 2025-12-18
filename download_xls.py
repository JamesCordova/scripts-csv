"""
Módulo base para descargar archivos desde la API del MEF Perú.

API Endpoint: https://ofi5.mef.gob.pe/inviertews/Ssi/expRepSSIDet
Método: POST con JSON payload

Parámetros del payload:
- plie: Código del departamento (1-25)
- dpto: Código de provincia (0 para todos)
- prov: Código de provincia (0 para todos)
- dist: Código de distrito (0 para todos)
- tipo: Tipo de gobierno ("GR" = Gobierno Regional)
- sect: Sector (vacío para todos)

Actualizado: Diciembre 2024
"""
import requests
import os
from typing import Optional


def download_mef_data(department_code: str, output_dir: str = "downloads", 
                      timeout: int = 90, max_retries: int = 3) -> Optional[str]:
    """
    Descarga datos de inversiones del MEF para un departamento específico.
    
    Args:
        department_code: Código del departamento (1-25, puede ser string o int)
                        Ejemplos: "4" = Arequipa, "15" = Lima
        output_dir: Directorio de salida donde guardar el archivo XLSX
        timeout: Timeout en segundos para la petición (default: 90)
        max_retries: Número máximo de reintentos en caso de fallo (default: 3)
        
    Returns:
        Ruta del archivo descargado o None si falla
        
    Raises:
        requests.RequestException: Si hay error en la petición HTTP después de reintentos
    """
    # Nueva API endpoint
    url = "https://ofi5.mef.gob.pe/inviertews/Ssi/expRepSSIDet"
    
    # Headers requeridos por la API
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'https://ofi5.mef.gob.pe',
        'Referer': 'https://ofi5.mef.gob.pe/ssi/Ssi/Index',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    # Body JSON con parámetros
    payload = {
        "sect": "",
        "plie": department_code,
        "dpto": 0,
        "prov": 0,
        "dist": 0,
        "tipo": "GR"
    }
    
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"inversiones_{department_code}.xlsx")
    
    # Intentar con reintentos
    for attempt in range(1, max_retries + 1):
        try:
            if attempt > 1:
                print(f"Reintento {attempt}/{max_retries}...")
            
            print(f"Descargando datos... (esto puede tardar 30-60 segundos)")
            
            # Realizar petición POST con timeout aumentado
            response = requests.post(url, headers=headers, json=payload, timeout=timeout)
            response.raise_for_status()
            
            # Guardar el archivo
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            file_size_kb = len(response.content) / 1024
            print(f"Descarga exitosa: {output_path} ({file_size_kb:.2f} KB)")
            return output_path
            
        except requests.Timeout as e:
            print(f"⏱️  Timeout después de {timeout} segundos (intento {attempt}/{max_retries})")
            if attempt == max_retries:
                print(f"Error: El servidor tardó más de {timeout} segundos en responder después de {max_retries} intentos")
                print("Sugerencia: El servidor del MEF puede estar sobrecargado. Intenta más tarde.")
                return None
                
        except requests.RequestException as e:
            print(f"Error de red (intento {attempt}/{max_retries}): {e}")
            if attempt == max_retries:
                print(f"Error al descargar datos del departamento {department_code}: {e}")
                return None
                
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None
    
    return None


if __name__ == "__main__":
    print("Módulo de descarga MEF - Perú")
    print("Usar con download_arequipa.py o download_all_departments.py")
