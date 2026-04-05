import requests
import logging
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
            response = requests.get(self.base_url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            count = data.get("metadata", {}).get("count", 0)
            logger.info(f"Se encontraron {count} eventos sismicos")
            return data
        
        except Exception as e:
            logger.error(f"Error critico en extraccion {e}")
            return None