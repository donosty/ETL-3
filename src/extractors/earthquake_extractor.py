import requests
import logging
import time
from datetime import datetime, timedelta
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class EarthquakeExtractor:
    def __init__(self):
        self.base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        
    def get_last_24h_earthquakes(self) -> Optional[Dict]:
        """
        Extrae sismos de magnitud > 1.0 en las ultimas 24 horas
        """
        
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        params = {
            "format": "geojson",
            "starttime" : yesterday,
            "minmagnitude": 1.0,
            "orderby": "time"
        }
        
        try:
            logger.info(f"Solicitando sismos desde {yesterday}")
            
            max_reintentos = 3
            timeout_segundos = 30
            
            for intento in range(max_reintentos):
                try:
                    response = requests.get(self.base_url, params=params, timeout=timeout_segundos)
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    count = data.get("metadata", {}).get("count", 0)
                    logger.info(f"Se encontraron {count} eventos sismicos")
                    return data
                
                except requests.exceptions.Timeout:
                    logger.warning(f"El servidor tardo mucho (Intento {intento + 1}/{max_reintentos}) Reintentando en 5 segundos")
                    time.sleep(5)
                    
                except requests.exceptions.RequestException as e:
                    logger.error(f"Error de conexion con la API: {e}")
                    break
            
            logger.error("Se agotaron los reintentos. La API esta caida")
            return None
            
        
        except Exception as e:
            logger.error(f"Error critico en extraccion {e}")
            return None