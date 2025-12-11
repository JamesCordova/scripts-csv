"""
Módulo base para descargar archivos desde la API del MEF Perú.
"""
import requests
import os
from typing import Optional


def download_file(url: str, output_path: str, headers: Optional[dict] = None) -> bool:
    """
    Descarga un archivo desde una URL.
    
    Args:
        url: URL del archivo a descargar
        output_path: Ruta donde guardar el archivo
        headers: Headers HTTP opcionales
        
    Returns:
        True si la descarga fue exitosa, False en caso contrario
    """
    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"Descarga exitosa: {output_path}")
        return True
        
    except requests.RequestException as e:
        print(f"Error al descargar {url}: {e}")
        return False


def download_mef_data(department_code: str, output_dir: str = "downloads") -> Optional[str]:
    """
    Descarga datos de inversiones del MEF para un departamento específico.
    
    Args:
        department_code: Código del departamento
        output_dir: Directorio de salida
        
    Returns:
        Ruta del archivo descargado o None si falla
    """
    base_url = "https://ofi5.mef.gob.pe/invierte/downloadFile"
    url = f"{base_url}?department={department_code}"
    
    output_path = os.path.join(output_dir, f"inversiones_{department_code}.xlsx")
    
    if download_file(url, output_path):
        return output_path
    return None


if __name__ == "__main__":
    print("Módulo de descarga MEF - Perú")
    print("Usar con download_arequipa.py o download_all_departments.py")
